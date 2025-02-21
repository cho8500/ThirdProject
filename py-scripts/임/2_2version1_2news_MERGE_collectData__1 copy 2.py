from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as WAIT
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from bs4 import BeautifulSoup
from DBManager import DBManager

import os
import time
import requests
import pandas as pd
import __LSTM.predic as pr
import tensorflow as tf
import re

# 분석할 종목과 코드 리스트
'''
stocksencoding = {
    "셀트리온": "%BC%BF%C6%AE%B8%AE%BF%C2", 
    "기아": "%B1%E2%BE%C6", 
    "두산에너빌리티": "%B5%CE%BB%EA%BF%A1%B3%CA%BA%F4%B8%AE%C6%BC", 
    "카카오": "%C4%AB%C4%AB%BF%C0", 
    "한화에어로스페이스": "%C7%D1%C8%AD%BF%A1%BE%EE%B7%CE%BD%BA%C6%E4%C0%CC%BD%BA", 
    "삼성SDI": "%BB%EF%BC%BASDI", 
    "한국전력": "%C7%D1%B1%B9%C0%FC%B7%C2", 
    "LG전자": "LG%C0%FC%C0%DA", 
    "SK하이닉스": "SK%C7%CF%C0%CC%B4%D0%BD%BA", 
    "현대차": "%C7%F6%B4%EB%C2%F7"
}
'''
### 실험중 나중에 삭제 예정
stocksencoding = {
    "기아": "%B1%E2%BE%C6" 
}


# 현재 날짜와 시간 가져오기
now = datetime.now()

# 날짜 범위 설정
start_date = "2024.10.01"
end_date = "2024.12.31"

# 달 설정
for month in range(10, 13):

    if month == 11:
        end_day = 31
    else:
        end_day = 32

    # 현재 날짜만 가져오기
    for date in range(1, end_day):

        current_date_dash = f"2024-{month:02}-{date:02}"
        current_date_withdot = f"2024.{month:02}.{date:02}"
        current_date_nodot = f"2024{month:02}{date:02}"

        # 브라우저 선택
        driver = webdriver.Chrome()

        scr_list = []
        eval_list = []

        # URL 추출
        for item, code in stocksencoding.items():

            # 분석 시작 알림
            print(f"[{item} : {code}] {current_date_dash} 시작...")

            # 설정(기간: 당일, 유형: 지면기사)하고 뉴스 검색 URL
            url = f"https://finance.naver.com/news/news_search.naver?rcdate=&q={code}&x=0&y=0&sm=all.basic&pd=1&stDateStart={current_date_dash}&stDateEnd={current_date_dash}"
            print(f"URL : {url}")
            
            # 설정대로 뉴스를 검색하고 대기
            driver.get(url)
            try:
                WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pgRR")))
            except Exception:
                print(f"{item} & page={url} 맨뒤 버튼 없음 ")
            
            lastpageBtn = driver.find_element(By.CSS_SELECTOR, ".pgRR")
            
            # 빈 리스트인지 확인
            if lastpageBtn:
                print("맨뒤 버튼이 존재합니다")
                WAIT(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".pgRR")))
                #요소로 스크롤 이동
                driver.execute_script("arguments[0].scrollIntoView();", lastpageBtn)
                lastpageBtn.click()
                print("맨뒤 버튼을 클릭합니다")
                time.sleep(2)
                current_url = driver.current_url
                match = re.search(r'page=(\d+)', current_url)
                lastpage = int(match.group(1)) if match else 1
            else:
                lastpage = 1
            
            current_url = driver.current_url
            print(f"현재 페이지 URL: {current_url}")
            
            lastpage = 1
            match = re.search(r'page=(\d+)', current_url)
            if match:
                lastpage = match.group(1)
                print(f'Page number: {lastpage}')
            else:
                print('Page number not found')
            
            urllist = []
            #driver.get(url)
            for page in range (1, int(lastpage) + 1) :
                driver.get(f"{url}&page={page}")
                time.sleep(3)
                try:
                    WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".articleSubject")))
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "html.parser")
                    article_subjects = soup.select(".articleSubject a")
                    for subject in article_subjects:
                            link = subject.get("href")
                            if link :
                                urllist.append(link)
                    if lastpage == lastpage:
                        break
                except Exception:
                    print(f"{item} & page={url} 기사 없음 ")

            print(f"urllist{urllist}")
            print(f"url_int{len(urllist)}")
            exit()
            # 추출할 링크 선택
            '''
            print("exit를 실행합니다")
            exit()
            
            
            # 기사가 없으면 반복을 넘어감
            if len(sel_news) == 0:
                print(f"{item}에 관한 {current_date_dash} 검색된 기사가 없습니다.")
                continue

            # 링크를 저장할 리스트 생성
            link_list = []

            # 모든 링크 찾아서 URL 수집
            for news_item in sel_news:
                link_list.append(news_item.get_attribute('href'))

            # 데이터프레임화
            url_df = pd.DataFrame(link_list, columns=["링크"])

            # 기사 내용이 들어갈 리스트 생성
            commentlist = []

            if len(link_list) == 0:
                print(f"{item}에 관한 {current_date_dash} 사용할 수 있는 기사가 없습니다.")
                continue

            for url_item in urlList:
                print(url_item, "을 탐색합니다")
                url_item = url_item.replace("article/", "article/comment/")
                print(f"URL : {url}")

                print("셀레니움에게 주소를 전달합니다")
                driver.get(url)
                time.sleep(3)

                flag = True

                while flag:
                    morebutton = driver.find_element(By.CSS_SELECTOR, ".u_cbox_page_more")
                    print(f"[morebutton]\n{morebutton}")

                    if not morebutton.empty:
                        morebutton.click()
                        time.sleep(2)
                    else:
                        flag = False

                print("더보기 버튼이 더이상 생성되지 않습니다")
                print("페이지 소스를 받아옵니다")
                tmp = driver.page_source
                print("bs4로 페이지를 파싱합니다")
                soup = BeautifulSoup(tmp, "html.parser")
                print("댓글을 찾습니다")
                comment = soup.select(".u_cbox_contents")
                print("추천의 개수를 찾습니다")
                recommlist = soup.select("em.u_cbox_cnt_recomm")
                print("비추천의 개수를 찾습니다")
                unrecommlist = soup.select("em.u_cbox_cnt_unrecomm")
                title = soup.select_one(".media_end_head_headline")

                if comment is None:
                    link_list.remove(url_item)
                    continue

                # 댓글 내용 가져오기 (공백 제거)
                for co in comment:
                    co = co.text
                    if co is not None:
                        co = co.replace("'", "").replace("\"", "")
                        commentlist.append(co)

                # DB 삽입
                title = title.get_text().strip()
                recommlist = [element.get_text().strip() for element in recommlist]
                unrecommlist = [element.get_text().strip() for element in unrecommlist]

                recommlist = pd.Series(recommlist).astype(int)
                unrecommlist = pd.Series(unrecommlist).astype(int)

                # 기사마다 감성분석 후 점수를 리스트로 저장
                for sent in commentlist:
                    scr = pr.sentiment_predict(sent)
                    scr = round(scr, 2)
                    if scr < 45:
                        eval = "negative"
                    elif 45 <= scr <= 55:
                        eval = "neutral"
                    else:
                        eval = "positive"
                    eval_list.append(eval)
                    scr_list.append(scr)

                totalresult = pd.DataFrame({
                    "date": [current_date_dash] * len(commentlist),
                    "name": [item] * len(commentlist),
                    "code": [code] * len(commentlist),
                    "title": [title] * len(commentlist),
                    "link": [url] * len(commentlist),
                    "up": recommlist,
                    "down": unrecommlist,
                    "comment": commentlist
                })

                resultupdate = pd.DataFrame({
                    "analysis": "T",
                    "sent_type": eval_list,
                    "sent_score": scr_list,
                    "comment": commentlist
                })

                db = DBManager()
                db.DBOpen(
                    host="localhost",
                    dbname="third_project",
                    id="root",
                    pw="ezen"
                )

                print(f"insertion...")
                db.insert_df("news_comments", totalresult)
                print("totalresult DB에 입력 성공!")

                if db.update_df(resultupdate):
                    print("resultupdate DB에 갱신 성공!")
                else:
                    print("업데이트 중 오류가 발생했습니다.")

                db.DBClose()
  '''