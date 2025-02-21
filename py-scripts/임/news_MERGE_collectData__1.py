from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait       as WAIT
from selenium.webdriver.support    import expected_conditions as EC
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

update = "update "
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

2024.10.01
2024.12.31
'''

# 달 설정
for month in range(10, 13):

    if month == 11 :
        end_day = 31
    else :
        end_day = 32

    # 현재 날짜만 가져오기
    for date in range(1, end_day) :

        # current_date = date
        current_date_dash    = f"2024-{month:02}-{date:02}"
        current_date_withdot = f"2024.{month:02}.{date:02}"
        current_date_nodot   = f"2024{month:02}{date:02}"
        '''
        # 임의 test용   ### 제거 예정
        current_date_dash    = f"2025-02-12"
        current_date_withdot = f"2025.02.12"
        current_date_nodot   = f"20250212"
        '''
        # 브라우저 선택
        driver = webdriver.Chrome()
        
        scr_list = []
        eval_list = []

        # _________________________url ext_________________________

        for item, code in list.items() :

            # 분석 시작 알림
            print(f"[{item} : {code}] {current_date_dash} 시작...")

            # 설정(기간: 당일, 유형: 지면기사)하고 뉴스 검색 url
            url = f"https://search.naver.com/search.naver?where=news&query={item}&sm=tab_opt&sort=1&photo=3&field=0&pd=3&ds={current_date_withdot}&de={current_date_withdot}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Afrom{current_date_nodot}to{current_date_nodot}&is_sug_officeid=0&office_category=0&service_area=0"
            print(f"URL : {url}")

            # 설정대로 뉴스를 검색하고 대기
            driver.get(url)
            try :
                WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.LINK_TEXT, "네이버뉴스")))
            except Exception :
                print(f"{item} & page={url} 데이터 로드 실패")
                break

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
            
            if len(link_list) == 0 :
                print(f"{item}에 관한 {current_date_dash} 사용할 수 있는 기사가 없습니다.")
                continue

            for url_item in urlList :
                print(url_item,"을 탐색합니다")
                url_item = url_item.replace("article/","article/comment/")
                # 실제로 실행할때 사용 할거
                # url = url_item
                ### 실제로 실행하게 되면 지워야 하는 거 ↓
                # url = "https://n.news.naver.com/mnews/article/comment/366/0001053512?sid=105"
                print(f"URL : {url}")
                
                print("셀레니움에게 주소를 전달합니다")
                driver.get(url)
                time.sleep(3)
                
                # try :
                #     WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".u_cbox_page_more")))
                # except Exception as e:
                #     print(f"[ERROR] {e}")
                #     print(f"[더보기 버튼 없음] {item} & page={url}")
                
                flag = True
                
                while flag :
                    morebutton = driver.find_element(By.CSS_SELECTOR,".u_cbox_page_more")
                    
                    print(f"[morebutton]\n{morebutton}")
                    
                    if not morebutton.empty :
                        morebutton.click()
                        time.sleep(2)
                    else :
                        flag = False
                
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
                recommlist = soup.select("em.u_cbox_cnt_recomm")
                print("비추천의 개수를 찾습니다")
                unrecommlist = soup.select("em.u_cbox_cnt_unrecomm")
                title = soup.select_one(".media_end_head_headline")

                 #.u_cbox_contents가 없으면 url 삭제후 다음 반복으로 넘어감
                if comment is None:
                    link_list.remove(url_item)
                    continue
                
                # 댓글 내용 가져오기 (공백 제거)
                for co in comment :
                    co = co.text
                    if co is not None:
                        co = co.replace("'", "").replace("\"", "") #따옴표 제거 
                        commentlist.append(co)

        # _________________________DB insertion_________________________

                #  str만 가져오고 좋아요, 싫어요의 타입 변경
                
                title = title.get_text().strip()
                                
                recommlist   = [element.get_text().strip() for element in recommlist]
                unrecommlist = [element.get_text().strip() for element in unrecommlist]
                
                recommlist   = pd.Series(recommlist).astype(int)
                unrecommlist = pd.Series(unrecommlist).astype(int)
                
                print(f"length          : ===== {len(commentlist)} =====")
                print(f"recomm  length  : ===== {len(recommlist)} =====")
                print(recommlist)
                print(f"unrecomm length : ===== {len(unrecommlist)} =====")
                print(unrecommlist)
                
                # 기사마다 감성분석 후 점수를 리스트로 저장
                for sent in commentlist:
                    scr = pr.sentiment_predict(sent)
                    scr = round(scr, 2)
                    if scr < 45 :
                        eval = "negative"
                    elif 45 <= scr <= 55 :
                        eval = "neutral"
                    else :
                        eval = "positive"
                    eval_list.append(eval)
                    scr_list.append(scr)

                print(f"점수리스트 : ======{scr_list}======")
                
                # 일일데이터를 데이터프레임화
                print(f"totalresult 데이터프레임화...")
                totalresult = pd.DataFrame({
                    "date"      : [current_date_dash ]  * len(commentlist)  ,
                    "name"      : [item]                * len(commentlist) ,
                    "code"      : [code]                * len(commentlist)  ,
                    "title"     : [title]               * len(commentlist)  ,
                    "link"      : [url]                 * len(commentlist)  ,
                    "up"      : recommlist,
                    "down"   : unrecommlist,
                    "comment"   : commentlist
                })
                #print(totalresult)
                #print(totalresult["comment"], totalresult["score"] )
                
                resultupdate = pd.DataFrame({
                    "analysis"  : "T",
                    "sent_type": eval_list,
                    "sent_score"     : scr_list,
                    "comment"   : commentlist
                })
                
            # DB 처리
                db = DBManager()
                db.DBOpen(
                    host   = "localhost",
                    dbname = "third_project",
                    id     = "root",
                    pw     = "ezen"
                )

                print(f"insertion...")
                db.insert_df("news_comments", totalresult)
                print("totalresult DB에 입력 성공!")
                
                #sql = f"update news_comments set analysis = 'T', sent_type = '{resultupdate['evaluation']}', sent_score = {resultupdate['score']} where comment = '{resultupdate['comment']}'"
                #db.executeQuery(sql)
                
                # resultupdate 데이터프레임을 사용하여 업데이트 작업 수행
                if db.update_df(resultupdate):
                    print("resultupdate DB에 갱신 성공!")
                else:
                    print("업데이트 중 오류가 발생했습니다.")

                db.DBClose()
                #exit()