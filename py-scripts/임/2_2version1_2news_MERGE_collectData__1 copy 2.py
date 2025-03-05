from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as WAIT
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from DBManager import DBManager  # DBManager 클래스를 수정하지 않습니다.

import time
import pandas as pd
import __LSTM.predic as pr  # 감성 분석 모듈
import re

def extract_kr_en_cn(inputString):  # 한글, 영어, 숫자 포함
    pattern = re.compile(r"[가-힣a-zA-Z0-9一-龥\s\.,!?]+")
    matches = pattern.findall(inputString)
    return ''.join(matches)

def setup_driver():
    """Selenium WebDriver 초기화"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 화면 출력 없이 실행
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# 분석할 종목과 코드 리스트
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

def fetch_news_links(driver, stock_name, stock_code, current_date_dash):
    """네이버 뉴스 검색 결과에서 기사 링크 추출"""
    search_url = f"https://finance.naver.com/news/news_search.naver?rcdate=&q={stock_code}&sm=all.basic&pd=1&stDateStart={current_date_dash}&stDateEnd={current_date_dash}"
    driver.get(search_url)

    try:
        WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".articleSubject a")))
        print("뉴스 데이터 찾음")
    except:
        print(f"[WARN] {stock_name}- {current_date_dash}에 대한 뉴스 데이터 없음")
        return []

    # 맨 뒤 페이지로 이동하여 총 페이지 수 파악
    try:
        lastpageBtn = driver.find_element(By.CSS_SELECTOR, ".pgRR")
        print("맨뒤 버튼이 존재합니다")
        driver.execute_script("arguments[0].click();", lastpageBtn)
        time.sleep(2)
        current_url = driver.current_url
        match = re.search(r'page=(\d+)', current_url)
        lastpage = int(match.group(1)) if match else 1
    except Exception:
        print(f"{stock_name} & page={search_url} 맨뒤 버튼 없음 ")
        lastpage = 1

    print(f"총 페이지 수: {lastpage}")

    urllist = []

    # 각 페이지를 순회하며 기사 링크 수집
    for page in range(1, lastpage + 1):
        driver.get(f"{search_url}&page={page}")
        time.sleep(2)
        try:
            WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".articleSubject a")))
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            article_subjects = soup.select(".articleSubject a")
            for subject in article_subjects:
                link = subject.get("href")
                if link:
                    if not link.startswith("http"):
                        link = "https://finance.naver.com" + link
                    urllist.append(link)
        except Exception as e:
            print(f"{stock_name} & page={page} 기사 없음 : {str(e)}")

    if not urllist:
        print(f"[INFO] {stock_name} - {current_date_dash} 기사 링크가 없습니다")

    return urllist

def fetch_comments(driver, article_url):
    """기사 댓글 수집"""
    # 댓글 페이지 URL 생성
    comment_url = article_url.replace("/news/", "/comment/news/")  # URL 구조에 따라 수정 필요
    driver.get(comment_url)
    time.sleep(2)

    # 더보기 버튼 클릭하여 모든 댓글 로드
    while True:
        try:
            more_button = driver.find_element(By.CSS_SELECTOR, ".u_cbox_btn_more")
            driver.execute_script("arguments[0].click();", more_button)
            time.sleep(1)
            print("더보기 버튼을 클릭했습니다.")
        except:
            print("더보기 버튼이 더 이상 존재하지 않거나, 찾을 수 없습니다.")
            break  # 더보기 버튼이 없으면 종료

    soup = BeautifulSoup(driver.page_source, "html.parser")
    # 댓글들 수집
    comments = [extract_kr_en_cn(c.text.strip()) for c in soup.select(".u_cbox_contents")]
    # 추천수와 비추천수 수집
    recomms = [int(r.text.strip()) for r in soup.select("em.u_cbox_cnt_recomm")]
    unrecomms = [int(ur.text.strip()) for ur in soup.select("em.u_cbox_cnt_unrecomm")]

    # 기사 제목 추출
    driver.get(article_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    title_element = soup.select_one(".media_end_head_headline")
    #title_element = soup.select_one(".article_info h3")
    title = title_element.text.strip() if title_element else "제목을 찾을 수 없습니다."

    return title, comments, recomms, unrecomms

def analyze_comments(comments):
    """댓글 감성 분석 수행"""
    scores, evaluations = [], []
    for comment in comments:
        score = round(pr.sentiment_predict(comment), 2)
        scores.append(score)
        evaluations.append("negative" if score < 45 else "neutral" if score <= 55 else "positive")
    return scores, evaluations

def insert_into_db(date, stock_name, stock_code, title, article_url, recomms, unrecomms, comments):
    """데이터 삽입"""
    db = DBManager()
    db.DBOpen(host="localhost", dbname="third_project", id="root", pw="ezen")

    # 특수 문자 처리
    title_processed = title.replace("'", "''").replace("`", "``").replace("\\", "\\\\")

    if stock_code == "%BC%BF%C6%AE%B8%AE%BF%C2":  # 셀트리온
        stock_code = "068270"
    elif stock_code == "%B1%E2%BE%C6":  # 기아
        stock_code = "000270"
    elif stock_code == "%B5%CE%BB%EA%BF%A1%B3%CA%BA%F4%B8%AE%C6%BC":  # 두산에너빌리티
        stock_code = "034020"
    elif stock_code == "%C4%AB%C4%AB%BF%C0":  # 카카오
        stock_code = "035720"
    elif stock_code == "%C7%D1%C8%AD%BF%A1%BE%EE%B7%CE%BD%BA%C6%E4%C0%CC%BD%BA":  # 한화에어로스페이스
        stock_code = "012450"
    elif stock_code == "%BB%EF%BC%BASDI":  # 삼성SDI
        stock_code = "006400"
    elif stock_code == "%C7%D1%B1%B9%C0%FC%B7%C2":  # 한국전력
        stock_code = "015760"
    elif stock_code == "LG%C0%FC%C0%DA":  # LG전자
        stock_code = "066570"
    elif stock_code == "SK%C7%CF%C0%CC%B4%D0%BD%BA":  # SK하이닉스
        stock_code = "000660"
    elif stock_code == "%C7%F6%B4%EB%C2%F7":  # 현대차
        stock_code = "005380"

    # totalresult 데이터프레임 생성
    totalresult = pd.DataFrame({
        "date": [date] * len(comments),
        "name": [stock_name] * len(comments),
        "code": [stock_code] * len(comments),
        "title": [title_processed] * len(comments),
        "link": [article_url] * len(comments),
        "up": recomms,
        "down": unrecomms,
        "comment": [c.replace("'", "''").replace("`", "``").replace("\\", "\\\\") for c in comments]
    })

    # 데이터 삽입
    db.insert_df("newscomments1", totalresult)
    db.DBClose()
    print(f"[INFO] {stock_name} 데이터 저장 완료!")

def update_analysis_in_db(comments, scores, evaluations):
    """데이터 업데이트"""
    db = DBManager()
    db.DBOpen(host="localhost", dbname="third_project", id="root", pw="ezen")

    # 특수 문자 처리
    # comments_processed = [comment.replace("'", "''").replace("`", "``").replace("\\", "\\\\") for comment in comments]
    comments_processed = [c.replace("'", "''").replace("`", "``").replace("\\", "\\\\") for c in comments]

    # resultupdate 데이터프레임 생성
    resultupdate = pd.DataFrame({
        #"analysis": ["T"] * len(comments),
        "sent_type": evaluations,
        "sent_score": scores,
        "comment": comments_processed
    })

    print(f"{resultupdate}+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    # 데이터 업데이트
    db.update_df(resultupdate)
    db.DBClose()
    print(f"[INFO] 감성 분석 결과 업데이트 완료!")

def main():
    driver = setup_driver()

    # 시작 날짜와 종료 날짜 설정 
    start_date = datetime(2025, 1, 9)
    end_date = datetime(2025, 2, 28)

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

                try:
                    title, comments, recomms, unrecomms = fetch_comments(driver, article_url)
                except Exception as e:
                    print(f"[ERROR] 댓글 수집 중 오류 발생: {str(e)}")
                    continue

                if not comments:
                    continue

                # 감성 분석 수행
                scores, evaluations = analyze_comments(comments)

                print(f"[INFO] 기사 제목: {title}")
                for cmt, score, recomm, unrecomm in zip(comments, scores, recomms, unrecomms):
                    print(f"댓글: {cmt}, 감성 점수: {score}, 추천수: {recomm}, 비추천수: {unrecomm}")

                # 데이터베이스에 저장
                insert_into_db(date_str, stock_name, stock_code, title, article_url, recomms, unrecomms, comments)
                update_analysis_in_db(comments, scores, evaluations)

        current_date += timedelta(days=1)

    driver.quit()

if __name__ == "__main__":
    main()



            
            
            # 추출할 링크 선택
'''
         
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