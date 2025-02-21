from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as WAIT
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from bs4 import BeautifulSoup
from DBManager import DBManager

import time
import pandas as pd
import __LSTM.predic as pr
from  datetime import datetime, timedelta

import re
def extract_kr_en_cn(inputString): # 한글만 받아오기
    pattern = re.compile(r"[가-힣a-zA-Z一-龥]+")
    matches = pattern.findall(inputString)
    return ' '.join(matches)

def setup_driver():
    """ Selenium WebDriver 초기화 """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 화면 출력 없이 실행
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# 분석할 종목과 코드 리스트
stocks = {
    "셀트리온" : "068270",
    "기아" : "000270",
    "두산에너빌리티" : "034020",
    "카카오" : "035720",
    "한화에어로스페이스" : "012450",
    "삼성SDI" : "006400",
    "한국전력" : "015760",
    "LG전자" : "066570",
    "SK하이닉스" : "000660",
    "현대차" : "005380"
}


def fetch_news_links(driver, stock_name, stock_code, date):
    """ 네이버 뉴스 검색 결과에서 기사 링크 추출 """
    search_url = f"https://search.naver.com/search.naver?where=news&query={stock_name}&sm=tab_opt&sort=1&pd=3&ds={date}&de={date}&nso=so%3Add%2Cp%3Afrom{date.replace('.', '')}to{date.replace('.', '')}"
    driver.get(search_url)
    
    try:
        WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.LINK_TEXT, "네이버뉴스")))
    except:
        print(f"[WARN] {stock_name}에 대한 뉴스 데이터 없음")
        return []
    
    return [link.get_attribute('href') for link in driver.find_elements(By.LINK_TEXT, '네이버뉴스')]

def fetch_comments(driver, article_url):
    """ 기사 댓글 수집 """
    driver.get(article_url.replace("article/", "article/comment/"))
    time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    comments = [extract_kr_en_cn(c.text.strip()) for c in soup.select(".u_cbox_contents")]
    recomms = [int(r.text.strip()) for r in soup.select("em.u_cbox_cnt_recomm")]
    unrecomms = [int(ur.text.strip()) for ur in soup.select("em.u_cbox_cnt_unrecomm")]
    title = soup.select_one(".media_end_head_headline").text.strip() if soup.select_one(".media_end_head_headline") else ""
    
    return title, comments, recomms, unrecomms
    
def analyze_comments(comments):
    """ 댓글 감성 분석 수행 """
    scores, evaluations = [], []
    for comment in comments:
        score = round(pr.sentiment_predict(comment), 2)
        scores.append(score)
        evaluations.append("negative" if score < 45 else "neutral" if score <= 55 else "positive")
    return scores, evaluations

def insert_into_db(date, stock_name, stock_code, title, article_url, recomms, unrecomms, comments):
    """ 첫 번째 데이터 삽입 (comment까지) """
    db = DBManager()
    db.DBOpen(host="localhost", dbname="third_project", id="root", pw="ezen")
    
    df = pd.DataFrame({
        "date": date,
        "name": stock_name,
        "code": stock_code,
        "title": title.replace("'", "''").replace("`", "``").replace("\\", "\\\\"),
        "link": article_url,
        "up": recomms,
        "down": unrecomms,
        "comment": [comment.replace("'", "''").replace("`", "``").replace("\\", "\\\\") for comment in comments]
    })
    
    db.insert_df("newsComments", df)
    db.DBClose()
    print(f"[INFO] {stock_name} 데이터 저장 완료!")

def update_analysis_in_db(comments, scores, evaluations):
    """ 두 번째 데이터 업데이트 (analysis, sent_type, sent_score) """
    db = DBManager()
    db.DBOpen(host="localhost", dbname="third_project", id="root", pw="ezen")
    
    update_df = pd.DataFrame({
        "analysis": "T",
        "sent_score": scores,
        "sent_type": evaluations,
        "comment": comments
    })
    
    db.update_df(update_df)
    db.DBClose()
    print(f"[INFO] 감성 분석 결과 업데이트 완료!")


def main():
    driver = setup_driver()
    
    # 시작 날짜와 종료 날짜 설정
    start_date = datetime(2024, 11, 1)
    end_date = datetime(2025, 1, 31)
    
    # current_date를 시작 날짜로 초기화
    current_date = start_date
    
    while current_date <= end_date:
        date_str = current_date.strftime("%Y.%m.%d")
        
        for stock_name, stock_code in stocks.items():
            print(f"[INFO] {stock_name} ({stock_code}) - {date_str} 기사 수집 시작")
            article_links = fetch_news_links(driver, stock_name, stock_code, date_str)
            
            if not article_links:
                continue
            
            for article_url in article_links:
                print(f"[INFO] {article_url} 기사 분석 중")
                
                title, comments, recomms, unrecomms = fetch_comments(driver, article_url)
                
                if not comments:
                    continue
                
                insert_into_db(date_str, stock_name, stock_code, title, article_url, recomms, unrecomms, comments)
                
                scores, evaluations = analyze_comments(comments)
                update_analysis_in_db(comments, scores, evaluations)
                
        current_date += timedelta(days=1)

if __name__ == "__main__":
    main()
