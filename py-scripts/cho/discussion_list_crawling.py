import json
import pandas as pd

from DBManager                     import DBManager
from bs4                           import BeautifulSoup
from datetime                      import datetime
from selenium                      import webdriver
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
# driver.execute_script(url) 방식으로 차단 우회
# 지정한 날짜가 나올 때까지 10페이지씩 이동 : 크롤링 속도 향상
def crawl_discussion(name, code, start_date, end_date) :

    # 기본 URL
    base_url = f"https://finance.naver.com/item/board.naver?code={code}"

    # Selenium 설정
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")              # 백그라운드 실행
    options.add_argument("--window-size=1920x1080") # 해상도 설정

    # options.add_argument("--disable-gpu") # GPU 가속 비활성화
    # options.add_argument("--log-level=3") # 불필요한 로그 제거
    # options.add_argument("--disable-infobars") # 안내메시지 제거
    # options.add_argument("--disabled-extensions") # 불필요한 확장프로그램 로드 방지
    # options.add_argument("--disabled-notifications") # 알림차단
    # options.add_argument("--disabled-popup-blocking") # 팝업 차단 해제
    # options.add_argument("--disable-blink-features=AutomationControlled") # selenium 감지방지
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36") # User-Agent 변경

    driver = webdriver.Chrome(options = options)

    all_posts   = []
    page        = 1
    step_size   = 1
    end_date_dt = datetime.strptime(end_date, "%Y.%m.%d")

    while True :
        try :
            # 웹 드라이버 로드 대기
            driver.execute_script(f"window.location.href='{base_url}&page={page}';")
            WAIT(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".type2 tbody")))

            soup = BeautifulSoup(driver.page_source, "html.parser")
            rows = soup.select(".type2 tbody tr")

            if not rows :
                print(f"[ERROR] {name} page={page} 데이터 없음. 크롤링 종료")
                break

            # 페이지 최상단 날짜 확인
            first_date = None

            for row in rows :
                cols = row.select("td")
                if len(cols) < 5 :
                    continue
                first_date = cols[0].text.strip()[:10]
                break

            print(f"[{name}] page : {page} / 최상단 날짜 : {first_date} / step size : {step_size}")

            if first_date is None :
                print(f"[ERROR] {name} {page}페이지 날짜 확인 불가")
                break

            # 날짜 비교 후 step_size 조정
            first_date_dt = datetime.strptime(first_date, "%Y.%m.%d")
            date_diff     = abs((first_date_dt - end_date_dt).days)

            if date_diff >= 15 :
                step_size = 50
            elif 7 <= date_diff < 15 :
                step_size = 10
            elif 3 <= date_diff < 7 :
                step_size = 2
            else :
                step_size = 1

            # 날짜 확인 후 크롤링 개시 또는 page 조정
            if start_date <= first_date <= end_date :
                print(f"[{name}] page={page} 범위 내 탐색 시작")

                while True :
                    print(f"[{name}] page={page} first_date={first_date} 크롤링 중...")
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    rows = soup.select(".type2 tbody tr")

                    stop_flag = False
                    for row in rows :
                        cols = row.select("td")
                        if len(cols) < 5 :
                            continue

                        title_tag      = cols[1]
                        cleanbot_title = title_tag.select_one(".cleanbot_list_blind")

                        if cleanbot_title :
                            continue

                        for span in title_tag.find_all("span") :
                            span.decompose()

                        title = title_tag.get_text(strip=True)
                        date  = cols[0].text.strip()[:10]
                        link  = f'https://finance.naver.com{cols[1].a["href"][:48] if cols[1].a else ""}'
                        view  = cols[3].text.strip()
                        up    = cols[4].text.strip()
                        down  = cols[5].text.strip()

                        # 수집한 날짜 데이터가 정해진 범위 안에 있는지 확인
                        if start_date <= date <= end_date :
                            all_posts.append([name, code, date, title, link, view, up, down])
                        elif date < start_date :
                            stop_flag = True

                    # 정해진 날짜를 벗어났으면 while 밖으로
                    if stop_flag :
                        break

                    page += 1
                    driver.execute_script(f"window.location.href='{base_url}&page={page}';")
                    WAIT(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".type2 tbody")))

                break

            elif first_date > end_date :
                page += step_size
            else :
                page -= step_size

        except Exception as e :
            print(f"[ERROR] {name} {page} 로드 실패 : {e}")
            break

    # 드라이버 종료
    driver.quit()

    # 데이터프레임화
    postDf = pd.DataFrame(all_posts, columns = ["name", "code", "date", "title", "link", "view", "up", "down"])

    if not postDf.empty :
        postDf["date"] = pd.to_datetime(postDf["date"])
        postDf = postDf.sort_values(by="date")

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

    list = load_stock_list("./cho/stock_list.json")

    # datetype = "yyyy.mm.dd"
    start_date = "2024.11.01"
    end_date   = "2025.01.31"

    for name, code in list.items() :

        print(f"[{name}] {start_date} ~ {end_date} 크롤링...")

        table_name = "discussion"

        df = crawl_discussion(name, code, start_date, end_date)

        if not df.empty :
            save_to_DB(table_name, df)
        else :
            print("저장할 수 있는 데이터가 없습니다.")