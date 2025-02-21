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
    "LG전자": "066570",
    "SK하이닉스": "000660",
    "현대차": "005380",
    "더본코리아": "475560"
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
    comments = [c.text.strip() for c in soup.select(".u_cbox_contents")]
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

def insert_into_db(date, stock_name, stock_code, title, article_url, recomms, unrecomms, comments, scores, evaluations):
    """ 데이터베이스에 데이터 삽입 """
    db = DBManager()
    db.DBOpen(host="localhost", dbname="third_project", id="root", pw="ezen")
    
    df = pd.DataFrame({
        "date": date,
        "name": stock_name,
        "code": stock_code,
        "title": title,
        "link": article_url,
        "up": recomms,
        "down": unrecomms,
        "comment": comments,
        "sent_score": scores,
        "sent_type": evaluations
    })
    
    db.insert_df("news_comments", df)
    db.DBClose()
    print(f"[INFO] {stock_name} 데이터 저장 완료!")

def main():
    driver = setup_driver()
    
    for month in range(10, 13):
        for day in range(1, 32 if month != 11 else 31):
            date_str = f"2024.{month:02}.{day:02}"
            
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
                    
                    scores, evaluations = analyze_comments(comments)
                    insert_into_db(date_str, stock_name, stock_code, title, article_url, recomms, unrecomms, comments, scores, evaluations)
                    
    driver.quit()

if __name__ == "__main__":
    main()
