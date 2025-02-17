import time
import pymysql
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
def fetch_URLs() :

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

    sql = "SELECT id, link FROM discussion WHERE comment IS NULL"

    df = db.fetch_DF(sql)
    db.DBClose()

    return df

'''=====================================
   게시글 내용을 크롤링 하고 COMMENT를 반환
   ====================================='''
def crawl_comment(url) :

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    driver  = webdriver.Chrome(options = options)

    comment = None

    try :
        print(f"[크롤링 시작] {url}")

        driver.get(url)
        WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".view_se")))
        soup        = BeautifulSoup(driver.page_source, "html.parser")
        comment_div = soup.select_one(".view_se")

        if comment_div :
            comment = " ".join(comment_div.get_text(strip=True).replace("\n", " ").split())

    except Exception as e :
        print(f"[크롤링 오류] {e}")

    finally :
        driver.quit()

    return comment

'''============================
   crawl_comment 실행 및 DB 저장
   ============================'''
def process_comment() :

    urls_df = fetch_URLs()

    if urls_df.empty :
        print("[INFO] 크롤링할 데이터 없음")
        return

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

    print(f"[INFO] {len(urls_df)}개 게시글 크롤링...")

    # URL 저장 dict, 결과 저장 list 생성
    urls        = {}
    result      = []
    failed_urls = []

    # ThreadPoolExecutor : 최대 10개 스레드 병렬 실행
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor :

        for _, row in urls_df.iterrows() :
            future = executor.submit(crawl_comment, row["link"])
            urls[future] = row

        for future in concurrent.futures.as_completed(urls) :

            row = urls[future]

            try :
                comment = future.result()

                if comment :
                    result.append((
                        comment,
                        row["id"]
                    ))
                else :
                    failed_urls.append(row["link"])

            except Exception as e :
                print(f"[크롤링 오류] {row['link']} - {e}")
                failed_urls.append(row["link"])

    if result :
        print(f"[INFO] {len(result)}개 데이터 저장 중...")

        # 크롤링한 데이터 INSERT
        sql = """
            UPDATE discussion
            SET comment = %s
            WHERE id = %s;
        """
        db.cursor.executemany(sql, result)
        db.con.commit()

        print(f"[INFO] {len(result)}개 데이터 저장 완료")

    if failed_urls :
        print(f"[ERROR] {len(failed_urls)}개의 개시글 크롤링 실패")
        for f_url in failed_urls :
            print(f"- {f_url}")

    db.DBClose()

#===========================================================================================

'''--------실행--------'''
if __name__ == "__main__" :
    process_comment()