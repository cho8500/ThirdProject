import time
import pymysql

from bs4                           import BeautifulSoup
from selenium                      import webdriver
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait as WAIT
from selenium.webdriver.support    import expected_conditions as EC

from DBManager import DBManager

# DB에서 크롤링 할 URL 가져오기
def fetch_URLs() :

    db = DBManager()
    db.DBOpen(
        host   = "192.168.0.184",
        dbname = "third_project",
        id     = "cho",
        pw     = "ezen"
    )
    sql = "SELECT name, code, date, link FROM disc_data WHERE content = 'F'"
    df = db.fetch_DF(sql)
    db.DBClose()

    return df

# 게시글 내용을 크롤링 하고 CONTENT를 반환
def crawl_content(url) :

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options = options)
    driver.get(url)

    try :
        WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".view_se")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        content_div = soup.select_one(".view_se")

        if content_div :
            content = content_div.get_text(strip=True)
        else :
            content = None

    except Exception as e :
        print(f"[크롤링 실패 오류] {e}")
        content = None

    finally :
        driver.quit()

    if content :
        return content.replace("\n", " ").strip()
    else :
        return content

# crawl_content 실행 및 DB 저장
def process_content() :

    urls_df = fetch_URLs()

    db = DBManager()
    db.DBOpen(
        host   = "192.168.0.184",
        dbname = "third_project",
        id     = "cho",
        pw     = "ezen"
    )

    for _, row in urls_df.iterrows() :

        content = crawl_content(row["link"])

        if content :

            sql = f"""
                INSERT INTO disc_analysis (date, name, code, link, row_cont)
                VALUES ('{row['date']}', '{row['name']}', '{row['code']}', '{row['link']}', '{content}');
            """
            db.execute(sql)

            sql = f"""
                UPDATE disc_data SET content = 'T'
                WHERE link = '{row['link']}';
            """
            db.execute(sql)
    db.DBClose()


if __name__ == "__main__" :
    process_content()