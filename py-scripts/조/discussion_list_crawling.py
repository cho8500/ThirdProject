import json
import time
import pandas as pd

from DBManager import DBManager
from bs4       import BeautifulSoup
from selenium  import webdriver
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait       as WAIT
from selenium.webdriver.support    import expected_conditions as EC

''' ===========================
    Json에서 종목 리스트 불러오기
    =========================== '''
def load_stock_list(json_file) :

    with open(f"{json_file}", "r", encoding = "UTF-8") as file :
        stock_dict = json.load(file)

    return stock_dict

''' ==============================
    네이버 주식 종목토론방 크롤링하기
    ============================== '''
def crawl_discussion(name, code, start_date, end_date) :

    # 기본 URL
    base_url = f"https://finance.naver.com/item/board.naver?code={code}"

    # Selenium 설정 : 백그라운드 실행, 렌더링 지정
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options = options)

    all_posts = []
    page      = 1

    # 페이지마다 날짜를 확인하며 데이터 수집
    while True :

        url = f"{base_url}&page={page}"

        driver.get(url)

        # 페이지 로딩 대기
        try :
            WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".type2 tbody")))
        except Exception :
            print(f"{name} & page={page} 데이터 로드 실패")
            break

        # 페이지 파싱
        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.select(".type2 tbody tr")

        stop_flag = False

        # td 개수로 데이터 수집할 열을 판별하고 수집
        for row in rows :
            cols = row.select("td")
            if len(cols) < 5 :
                continue

            # 클린봇에 의해 숨겨진 게시글은 건너뛰기
            title_tag      = cols[1]
            cleanbot_title = title_tag.select_one(".cleanbot_list_blind")

            if cleanbot_title :
                continue

            for span in title_tag.find_all("span") :
                span.decompose()

            title     = title_tag.get_text(strip=True)
            date      = cols[0].text.strip()[:10]
            link      = f'https://finance.naver.com{cols[1].a["href"][:48] if cols[1].a else ""}'
            view      = cols[3].text.strip()
            recommend = cols[4].text.strip()
            dislike   = cols[5].text.strip()

            # 수집한 날짜 데이터가 정해진 범위 안에 있는지 확인
            if start_date <= date <= end_date :
               all_posts.append([name, code, date, title, link, view, recommend, dislike])
            elif date < start_date :
                stop_flag = True

        # 정해진 날짜를 벗어났으면 while 밖으로
        if stop_flag :
            break

        # 정해진 날짜를 벗어나지 않았으면 다음페이지로
        page += 1

    # 수집하는 드라이버 종료
    driver.quit()

    # 데이터를 데이터프레임화
    postDf = pd.DataFrame(all_posts, columns = ["name", "code", "date", "title", "link", "view", "recommend", "dislike"])

    return postDf

''' ===========================
    "table"에 "dataFrame"을 저장
    =========================== '''
def save_to_DB (table_name, df) :

    db = DBManager()
    db.DBOpen(
        host   = "192.168.0.184",
        dbname = "third_project",
        id     = "cho",
        pw     = "ezen"
        # host   = "localhost",
        # dbname = "third_project",
        # id     = "root",
        # pw     = "chogh"
    )
    db.insert_df(table_name, df)
    db.DBClose()

#===========================================================================================

'''--------실행--------'''
if __name__ == "__main__" :

    list = load_stock_list("./조/stock_list_test.json")

    # datetype = "yyyy.mm.dd"
    start_date = "2025.02.11"
    end_date   = "2025.02.11"

    for name, code in list.items() :

        print(f"[{name}] {start_date} ~ {end_date} 크롤링...")

        table_name = "disc_data"

        df = crawl_discussion(name, code, start_date, end_date)

        if not df.empty :
            save_to_DB(table_name, df)
        else :
            print("저장할 수 있는 데이터가 없습니다.")