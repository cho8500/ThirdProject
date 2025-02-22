import concurrent.futures
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WAIT
from selenium.webdriver.support import expected_conditions as EC

# 크롤링 작업 함수
def crawl_task(driver, url):
    try:
        driver.get(url)
        WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
        time.sleep(1)
    except Exception as e:
        print(f"[오류] {e}")

# 각 드라이버별 작업 실행 함수
def driver_worker(urls, n_threads):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures = [executor.submit(crawl_task, driver, url) for url in urls]
        concurrent.futures.wait(futures)

    driver.quit()

# 테스트 실행 함수
def test_performance(n_drivers, n_threads, urls):
    url_chunks = [urls[i::n_drivers] for i in range(n_drivers)]

    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_drivers) as executor:
        futures = [executor.submit(driver_worker, chunk, n_threads) for chunk in url_chunks]
        concurrent.futures.wait(futures)

    end = time.time()
    duration = end - start
    print(f"[INFO] 드라이버 {n_drivers}개, 각 드라이버 스레드 {n_threads}개 실행 시간: {duration:.2f}초")
    return duration

# 메인 함수
def main():
    urls = ["https://www.naver.com"] * 24  # 고정된 작업량(24개)

    best_time = float("inf")
    best_config = (0, 0)

    for n_drivers in range(1, 5):  # 드라이버 개수 1~4개
        for n_threads in range(1, 7):  # 스레드 개수 1~6개
            print(f"\n[테스트 시작] 드라이버 {n_drivers}개, 스레드 {n_threads}개")
            duration = test_performance(n_drivers, n_threads, urls)

            if duration < best_time:
                best_time = duration
                best_config = (n_drivers, n_threads)

    print("\n[최적의 설정 결과]")
    print(f"- 드라이버 개수: {best_config[0]}개")
    print(f"- 각 드라이버별 스레드 개수: {best_config[1]}개")
    print(f"- 실행 시간: {best_time:.2f}초")

if __name__ == "__main__":
    main()
