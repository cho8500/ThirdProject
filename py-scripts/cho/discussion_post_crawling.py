import concurrent.futures

from bs4                           import BeautifulSoup
from selenium                      import webdriver
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait as WAIT
from selenium.webdriver.support    import expected_conditions as EC

from DBManager import DBManager

'''===========================
   DB에서 크롤링 할 URL 가져오기
   ==========================='''
def fetch_URLs(limit=1000) :

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

    # 한 종목 끝나면 DB에 UPDATE 하도록 변경 > 지금은 일괄로 넣기 때문에 중간에 끊기면 다 날아감
    # 0221 수정사항 : LIMIT 추가해서 한번에 불러와 처리하는 용량 제한 > 성능향상 가능
    sql = f"SELECT id, name, date, link FROM discussion WHERE comment IS NULL LIMIT {limit}"
    df  = db.fetch_DF(sql)
    db.DBClose()

    return df

'''=====================================
   게시글 내용을 크롤링 하고 COMMENT를 반환
   ====================================='''
def crawl_comment(name, date, url, driver) :

    comment    = None

    try :
        print(f"[INFO] 크롤링 시작 [{name}] {date} : {url}")
        driver.get(url)
        WAIT(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".view_se")))
        soup        = BeautifulSoup(driver.page_source, "html.parser")
        comment_div = soup.select_one(".view_se")

        if comment_div :
            comment = " ".join(comment_div.get_text(strip=True).replace("\n", " ").split())

    except Exception as e :
        print(f"[ERROR] 크롤링 오류 : {e}")

    return comment

'''===============
   웹 드라이버 로드
   ==============='''
def driver_worker(url_rows) :

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver     = webdriver.Chrome(options=options)

    results     = []
    failed_urls = []

    # 멀티스레드 쓰고싶다 / thread 인자 받아오기
    # with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor :
    #     futures = [executor.submit(crawl_comment, row.name, row.date, row.link, driver) for row in url_rows]

    #     for future, row in zip(futures, url_rows) :
    #         comment = future.result()

    #         if comment :
    #             results.append((comment, row.id))
    #         else :
    #             failed_urls.append(row.link)

    for row in url_rows:
        comment = crawl_comment(row.name, row.date, row.link, driver)
        if comment:
            results.append((comment, row.id))
        else:
            failed_urls.append(row.link)

    driver.quit()

    return results, failed_urls

'''============================
   crawl_comment 실행 및 DB 저장
   ============================'''
def process_comment(batch=1000, drivers=1) :

    while True :

        urls_df = fetch_URLs(limit=batch)

        if urls_df.empty :
            print("[INFO] 크롤링할 데이터 없음")
            return

        print(f"[INFO] {len(urls_df)}개 크롤링 시작 (드라이버 {drivers} x 스레드 1)")

        url_chunks = [urls_df.iloc[i::drivers] for i in range(drivers)]

        all_results        = []
        all_failed_results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=drivers) as executor :
            futures = [executor.submit(driver_worker, chunk.itertuples()) for chunk in url_chunks]

            for future in futures :
                results, failed_urls = future.result()
                all_results.extend(results)
                all_failed_results.extend(failed_urls)

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

        if all_results :
            print(f"[INFO] {len(all_results)}개 데이터 저장 중...")

            # 크롤링한 데이터 UDATE
            sql = """
                UPDATE discussion
                SET comment = %s
                WHERE id = %s;
            """
            db.cursor.executemany(sql, all_results)
            db.con.commit()

            print(f"[INFO] {len(all_results)}개 데이터 저장 완료")

        if all_failed_results :
            print(f"[ERROR] {len(all_failed_results)}개의 개시글 크롤링 실패")
            for f_url in all_failed_results :
                print(f"- {f_url}")

        db.DBClose()

#===========================================================================================

'''--------실행--------'''
if __name__ == "__main__" :
    process_comment(batch=1000, drivers=10)