from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from bs4 import BeautifulSoup
#from DBManager import DBManager

import os
import time
import requests
import pandas as pd
#import __LSTM.predic as pr

# 분석할 종목과 코드 리스트
list = {
    "삼성전자" : "005930",
    "LG전자" : "066570",
    "SK하이닉스" : "000660",
    "현대차" : "005380",
    "더본코리아" : "475560"
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
       
       
        current_date_dash   = f"2025-02-12"
        current_date_withdot = f"2025.02.12"
        current_date_nodot   = f"20250212"

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
            commentlist =[]

            for url_item in urlList :
                print(url_item,"을 탐색합니다")
                url_item = url_item.replace("article/","article/comment/")
                #url = url_item
                url = "https://n.news.naver.com/mnews/article/comment/366/0001053512?sid=105"
                print(f"URL : {url}")
                
                # URL 요청 및 HTML 가져오기
                # result = requests.get(url = url_item, headers = agent_head)
                # soup   = BeautifulSoup(result.text, "html.parser")
                
                print("셀레니움에게 주소를 전달합니다")
                driver.get(url)
                time.sleep(1)
                
                
                    # 더보기 
                while True :
                    try:
                        print("더보기 버튼을 찾습니다")
                        morebutton = driver.find_element(By.CSS_SELECTOR,".u_cbox_page_more") # 찾기
                        morebutton.click()
                        time.sleep(1)
                    except Exception as e:
                        print(e)
                        break
                
                # 더보기 버튼을 눌러 페이지 소스가 변경되었으므로
                # driver에게 페이지의 소스를 다시 요청
                print("더보기 버튼이 더이상 생성되지 않습니다")
                print("페이지 소스를 받아옵니다")
                tmp = driver.page_source
                print("bs4로 페이지를 파싱합니다")
                soup   = BeautifulSoup(tmp, "html.parser")
                print("댓글을 찾습니다")
                comment = soup.select(".u_cbox_contents")
                print("추천의 개수를 찾습니다")
                recomm = soup.select(".u_cbox_cnt_recomm")
                print("비추천의 개수를 찾습니다")
                unrecomm = soup.select(".u_cbox_cnt_unrecomm")

                 #.u_cbox_contents가 없으면 url 삭제후 다음 반복으로 넘어감
                if comment is None:
                    link_list.remove(url_item)
                    continue
                
                # 댓글 내용 가져오기 (공백 제거)
                for co in comment :
                    commentlist.append(co.get_text())

                print(f"length : {len(commentlist)}=======================")
                print(f"recomm  length : {len(recomm)}=======================")
                print(f"unrecomm length : {len(unrecomm)}=======================")

                totalresult = pd.DataFrame({
                    "URL" : url,
                    "commentlist" : commentlist,
                    "recomm" :recomm,
                    "unrecomm" : unrecomm
                })

                print(totalresult["URL"])

                exit()
                # 리스트에 추가
                # commentlist.append(comment_text)

            if len(link_list) == 0 :
                print(f"{item}에 관한 {current_date_dash} 사용할 수 있는 기사가 없습니다.")
                continue

            # 데이터 프레임화
            contents = pd.DataFrame(commentlist, columns = ["기사내용"])
            print(contents)
            exit()
            
        driver.quit()