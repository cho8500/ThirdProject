from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime

import pandas as pd
import requests
import time
import news_01stock_ext as stocks

# 현재 날짜와 시간 가져오기
now = datetime.now()

# 현재 날짜만 가져오기
current_date = now.date()
current_date_withdot = current_date.strftime("%Y.%m.%d")
current_date_nodot   = current_date.strftime("%Y%m%d")

# 브라우저 선택
driver = webdriver.Chrome()

# 뉴스를 검색할 종목 10개 리스트
list = stocks.get_stocks()

'''
# 2월 1일부터 2월 5일까지의 기사 설정
date_nodot = ""
date_dot = ""

for day in range(1,6) :
    day = format(day, "02")
    print(day)
    date_nodot = f"202502{day}"
    date_dot = f"2025.02.{day}"
'''

for item in list :
    
    # NAVER만 예외처리; 영문기사가 많이 나옴
    if item == "NAVER" :
        item = "네이버"
    
    # 설정(기간: 당일, 유형: 지면기사)하고 뉴스 검색 url
    url = f"https://search.naver.com/search.naver?where=news&query={item}&sm=tab_opt&sort=1&photo=3&field=0&pd=3&ds={current_date_withdot}&de={current_date_withdot}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Afrom{current_date_nodot}to{current_date_nodot}&is_sug_officeid=0&office_category=0&service_area=0"

    '''
    #날짜를 지정해서 크롤링하는 코드  ### 작성중
    url = f"https://search.naver.com/search.naver?where=news&query={item}&sm=tab_opt&sort=1&photo=3&field=0&pd=3&ds={date_dot}&de={date_dot}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Afrom{date_nodot}to{date_nodot}&is_sug_officeid=0&office_category=0&service_area=0"
    
    time.sleep(10)
    '''
    
    print(f"대상 사이트 주소 : {url}")
    print("크롤링 시작")

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

    # 링크를 저장할 리스트 생성
    link_list = []

    # 모든 링크 찾아서 주소 수집
    for news_item in sel_news :
        link_list.append(news_item.get_attribute('href'))

    # 데이터프레임화
    df = pd.DataFrame(link_list, columns=["링크"])

    if item == "네이버" :
        item == "NAVER"
    
    # csv 파일로 저장
    #df.to_csv(f"./companies/{item}/1d_{item}_{current_date}_link.csv", encoding="utf-8")
    df.to_csv(f"./companies/{item}/1d_{item}_{current_date_nodot}_link.csv", encoding="utf-8")

    print(f"{item}.csv 파일이 저장되었습니다")

