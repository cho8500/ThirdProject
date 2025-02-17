from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from bs4 import BeautifulSoup
from DBManager import DBManager

import os
import time
import requests
import pandas as pd
import __LSTM.predic as pr

# 분석할 종목과 코드 리스트
list = {
    "삼성전자" : "005930",
    "LG전자" : "066570",
    "SK하이닉스" : "000660",
    "삼성바이오로직스" : "207940",
    "현대차" : "005380",
    "기아" : "000270",
    "대한항공" : "003490",
    "KB금융" : "105560",
    "포스코" : "005490",
    "카카오" : "035720"
}

'''
# 현재 날짜와 시간 가져오기
now = datetime.now()
'''


# 달 설정
for month in range(8, 11):

    if month == 9 :
        end_day = 31
    else :
        end_day = 32

    # 현재 날짜만 가져오기
    for date in range(1, end_day) :

        # current_date = date
        current_date_dash   = f"2024-{month:02}-{date:02}"
        current_date_withdot = f"2024.{month:02}.{date:02}"
        current_date_nodot   = f"2024{month:02}{date:02}"

        # 브라우저 선택
        driver = webdriver.Chrome()

        # _________________________url ext_________________________

        for item, code in list.items() :

            # 분석 시작 알림
            print(f"[{item} : {code}] {current_date_dash} 시작...")

            # 설정(기간: 당일, 유형: 지면기사)하고 뉴스 검색 url
            url = f"https://search.naver.com/search.naver?where=news&query={item}&sm=tab_opt&sort=1&photo=3&field=0&pd=3&ds={current_date_withdot}&de={current_date_withdot}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Afrom{current_date_nodot}to{current_date_nodot}&is_sug_officeid=0&office_category=0&service_area=0"
            print(f"URL : {url}")

            # 설정대로 뉴스를 검색하고 대기
            driver.get(url)
            time.sleep(2)

            # 스크롤 끝까지 내리기
            while True :
                before = driver.execute_script('return document.body.scrollHeight')
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)

                # 스크롤이 더 이상 내려가지 않으면 break
                after = driver.execute_script('return document.body.scrollHeight')
                if before == after :
                    break

            # 추출할 링크 선택
            sel_news = driver.find_elements(By.LINK_TEXT, '네이버뉴스')

            if len(sel_news) == 0 :
                print(f"{item}에 관한 {current_date_dash} 검색된 기사가 없습니다.")
                continue

            # 링크를 저장할 리스트 생성
            link_list = []

            # 모든 링크 찾아서 url 수집
            for news_item in sel_news :
                link_list.append(news_item.get_attribute('href'))

            # 데이터프레임화
            url_df = pd.DataFrame(link_list, columns=["링크"])

        # _________________________get text_________________________

            urlList = url_df["링크"]

            agent_head = {
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            }

            # 기사 내용이 들어갈 리스트 생성
            dic_arealist =[]

            for url_item in urlList :

                # URL 요청 및 HTML 가져오기
                result = requests.get(url = url_item, headers = agent_head)
                soup   = BeautifulSoup(result.text, "html.parser")

                # 기사 영역 선택
                dic_area = soup.select_one("#dic_area")

                # dic_area가 없으면 url을 삭제하고 다음 반복으로 넘어감
                if dic_area is None:
                    link_list.remove(url_item)
                    continue

                # 사진 설명 제거 (있을 경우)
                img_desc = dic_area.select_one("span.end_photo_org")
                if img_desc:
                    img_desc.decompose()

                # 기사 내용 가져오기 (공백 제거)
                dic_area_text = dic_area.get_text().strip()

                # 리스트에 추가
                dic_arealist.append(dic_area_text)

            if len(link_list) == 0 :
                print(f"{item}에 관한 {current_date_dash} 사용할 수 있는 기사가 없습니다.")
                continue

            # 데이터 프레임화
            contents = pd.DataFrame(dic_arealist, columns = ["기사내용"])

        # _________________________sentiment predict_________________________

            # 내부 공백 및 줄바꿈 제거
            contents = contents["기사내용"]
            contents = contents.replace("\n", "", regex=True)
            contents = contents.replace("\t", "", regex=True)

            # 점수 총합 및 점수 리스트 생성
            sum = 0
            scr_list = []
            avg_score = 0

            # 기사마다 감성분석 후 점수를 리스트로 저장
            for sent in contents:
                scr = pr.sentiment_predict(sent)
                scr_list.append(scr)
                sum += scr

            print(f"scr_list{scr_list}")
            exit()
            avg_score = sum / len(link_list)

        # _________________________DB insertion_________________________

            # insert 데이터 확인
            print(f"len(link_list)    : {len(link_list)}")
            print(f"len(dic_arealist) : {len(dic_arealist)}")
            print(f"len(scr_list)     : {len(scr_list)}")

            # 일일데이터를 데이터프레임화
            print(f"daily_data_table 데이터프레임화...")
            daily_data_table = pd.DataFrame({
                "date"  : [current_date_dash] * len(link_list),
                "name"  : [item] * len(link_list),
                "code"  : [code] * len(link_list),
                "url"   : link_list,
                "score" : scr_list
            })

            print(f"total_result_table 데이터프레임화...")
            # 분석결과 데이터를 데이터프레임화
            total_result_table = pd.DataFrame({
                "date" : [current_date_dash],
                "name" : [item],
                "score": [avg_score],
                "news_count" : [len(link_list)]
            })

        # DB 처리
            db = DBManager()
            db.DBOpen(
                host   = "192.168.0.184",
                dbname = "second_project",
                id     = "cho",
                pw     = "ezen"
            )

            print(f"insertion...")
            db.insert_df("daily_data", daily_data_table)
            db.insert_df("total_result", total_result_table)

            db.DBClose()

