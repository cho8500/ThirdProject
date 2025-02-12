import json
import time
import pandas as pd

from DBManager import DBManager
from bs4       import BeautifulSoup
from selenium  import webdriver
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait       as WAIT
from selenium.webdriver.support    import expected_conditions as EC


# Json에서 종목 리스트 불러오기
def load_stock_list(json_file) :

    with open(f"{json_file}", "r", encoding = "UTF-8") as file :
        stock_dict = json.load(file)

    return stock_dict

# 네이버 주식 종목토론방 크롤링하기
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

    # 정해진 기간동안의 게시물을 전부 가져오기
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
            cols = row.find_all("td")
            if len(cols) < 5 :
                continue

            title = cols[1].text.strip()

            # 클린봇에 의해 삭제된 게시글은 수집하지 않기
            if "클린봇" in title :
                continue

            date      = cols[0].text.strip()[:10]
            link      = cols[1].a["href"] if cols[1].a else ""
            view      = cols[2].text.strip()
            recommend = cols[3].text.strip()
            dislike   = cols[4].text.strip()

            if start_date <= date <= end_date :
               all_posts.append([name, code, date, title, link, view, recommend, dislike])
            elif date < start_date :
                stop_flag = True

        if stop_flag :
            break

        page += 1

    driver.quit()
    postDf = pd.DataFrame(all_posts, columns = ["name", "code", "date", "title", "link", "view", "recommend", "dislike"])

    return postDf

# "테이블"에 "데이터프레임"을 저장
def save_to_DB (table_name, df) :

    db = DBManager()
    db.DBOpen(
        host   = "localhost",
        dbname = "test",
        id     = "cho",
        pw     = "ezen"
    )
    db.insert_df(table_name, df)
    db.DBClose()

    print(f"{len(df)}개 데이터 저장 완료")



'''--------실행--------'''
if __name__ == "__main__" :

    list = load_stock_list("./조/stock_list_test.json")

    print(list)
    print(type(list))

    start_date = "2025.02.11"
    end_date   = "2025.02.11"

    for name, code in list.items() :

        print(f"[{name}] {start_date} ~ {end_date} 크롤링...")

        df = crawl_discussion(name, code, start_date, end_date)

        if not df.empty :
            save_to_DB("test_table", df)
        else :
            print("저장할 수 있는 데이터가 없습니다.")

