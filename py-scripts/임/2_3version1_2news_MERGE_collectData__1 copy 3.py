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


def fetch_news_links(driver, stock_name, stock_code, current_date_dash):
    """ 네이버 뉴스 검색 결과에서 기사 링크 추출 """
    search_url = f"https://finance.naver.com/news/news_search.naver?rcdate=&q={stock_code}&x=0&y=0&sm=all.basic&pd=1&stDateStart={current_date_dash}&stDateEnd={current_date_dash}"
    driver.get(search_url)
    
    try:
        WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".articlesubject a")))
        print("뉴스 데이터 찾음")
    except:
        print(f"[WARN] {stock_name}- {current_date_dash}에 대한 뉴스 데이터 없음")
        return []
    
    # 1. 맨 뒤 페이지로 이동
    try:
        lastpageBtn = driver.find_element(By.CSS_SELECTOR, ".pgRR")
        print("맨뒤 버튼이 존재합니다")
        WAIT(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".pgRR")))
        driver.execute_script("arguments[0].scrollIntoView();", lastpageBtn)
        lastpageBtn.click()
        print("맨뒤 버튼을 클릭합니다")
        time.sleep(2)
        current_url = driver.current_url
        match = re.search(r'page=(\d+)', current_url)
        lastpage = int(match.group(1)) if match else 1
    except Exception:
        print(f"{stock_name} & page={search_url} 맨뒤 버튼 없음 ")
        lastpage = 1
    
    current_url = driver.current_url
    print(f"현재 페이지 URL: {current_url}")
    
    urllist = []
    
    # 2. 다시 처음 페이지로 이동하여 페이지를 하나씩 넘기며 기사 링크를 수집
    for page in range(1, int(lastpage) + 1):
        driver.get(f"{search_url}&page={page}")
        time.sleep(3)
        try:
            WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".articlesubject a")))
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            article_subjects = soup.select(".articlesubject a")
            for subject in article_subjects:
                link = subject.get("href")
                if link:
                    urllist.append(link)
        except Exception as e:
            print(f"{stock_name} & page={search_url} 기사 없음 : {str(e)}")
    
    #print(f"[DEBUG] {stock_name} 링크: {urllist}")
    if not urllist : 
        print(f"[INFO] {stock_name} - {current_date_dash} 기사 링크가 없습니다")
    
    return urllist


def fetch_comments(driver, article_url):
    """ 기사 댓글 수집 """
    driver.get(article_url)
    
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
    start_date = datetime(2024, 6, 1)
    end_date = datetime(2024, 6, 2)
    
    # current_date를 시작 날짜로 초기화
    current_date = start_date
    
    while current_date <= end_date:
        date_str = current_date.strftime("%Y.%m.%d")
        
        current_date_dash = current_date.strftime("%Y-%m-%d")
        
        for stock_name, stock_code in stocksencoding.items():
            print(f"[INFO] {stock_name} ({stock_code}) - {date_str} 기사 수집 시작")
            article_links = fetch_news_links(driver, stock_name, stock_code, current_date_dash)
            
            if not article_links:
                continue
            
            for article_url in article_links:
                print(f"[INFO] {article_url} 기사 분석 중")
                
                title, comments, recomms, unrecomms = fetch_comments(driver, article_url)
                
                if not comments:
                    continue
                
                # 감성 분석 수행 (추가된 부분)
                scores, evaluations = analyze_comments(comments)
                
                print(f"[INFO] 기사 제목: {title}")
                for comment, score, recomm, unrecomm in zip(comments, scores, recomms, unrecomms):
                    print(f"댓글: {comment}, 감성 점수: {score}, 추천수: {recomm}, 비추천수: {unrecomm}")
                
                '''
                insert_into_db(date_str, stock_name, stock_code, title, article_url, recomms, unrecomms, comments)
                
                scores, evaluations = analyze_comments(comments)
                update_analysis_in_db(comments, scores, evaluations)
                '''
                print(f"analyze__comments={analyze_comments}")
                exit()
        current_date += timedelta(days=1)

if __name__ == "__main__":
    main()
