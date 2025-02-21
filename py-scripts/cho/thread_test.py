'''================
   CPU코어 개수 확인
   ================'''
import os
# print("CPU 코어 개수:", os.cpu_count())


'''============================
   웹 크롤링 max_workers 결정하기
   ============================'''
import concurrent.futures
import time

def test_speed(n):
    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(time.sleep, 2) for _ in range(10)]
        concurrent.futures.wait(futures)

    end = time.time()
    print(f"[INFO] 스레드 {n}개 실행 시간: {end - start:.2f}초")

# 테스트 실행
# for workers in [2, 5, 10, 20, 50]:
#     test_speed(workers)

'''
==========expected result==========
[INFO] 스레드 1개 실행 시간: 20.02초
[INFO] 스레드 2개 실행 시간: 10.01초
[INFO] 스레드 5개 실행 시간: 4.05초
[INFO] 스레드 10개 실행 시간: 2.02초
[INFO] 스레드 20개 실행 시간: 2.01초
[INFO] 스레드 50개 실행 시간: 2.00초
===================================
'''

'''====================
   웹 드라이버 효율 측정
   ===================='''
import concurrent.futures
import time
from selenium import webdriver

def test_driver_speed(n):
    start = time.time()

    def open_page():

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.naver.com")
        time.sleep(2)  # 2초간 대기
        driver.quit()

    with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(open_page) for _ in range(10)]
        concurrent.futures.wait(futures)

    end = time.time()
    print(f"[INFO] 스레드 {n}개 드라이버 실행 시간: {end - start:.2f}초")

# 웹드라이버 테스트 실행
for workers in [2, 5, 8, 10, 15, 20, 25, 30]:
    test_driver_speed(workers)
'''
===============expected result===============
[INFO] 스레드 2개 드라이버 실행 시간: 48.37초
[INFO] 스레드 5개 드라이버 실행 시간: 20.57초
[INFO] 스레드 10개 드라이버 실행 시간: 11.77초
=============================================
'''

'''=========================
   드라이버당 스레드 개수 측정
   ========================='''
import concurrent.futures
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WAIT
from selenium.webdriver.support import expected_conditions as EC

# 스레드가 수행할 간단한 작업
def simple_task(driver, url):
    try:
        driver.get(url)
        WAIT(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
        time.sleep(1)  # 페이지 로딩 이후 잠시 대기 (작업 시뮬레이션)
    except Exception as e:
        print(f"[오류] {e}")

def test_shared_driver_speed(n_threads, urls):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)

    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures = []
        for i, url in enumerate(urls):
            time.sleep(0.5)
            futures.append(executor.submit(simple_task, driver, url))

        concurrent.futures.wait(futures)

    end = time.time()
    driver.quit()

    print(f"[INFO] 스레드 {n_threads}개(드라이버 1개) 실행 시간: {end - start:.2f}초")

# 테스트할 URL (가벼운 페이지로 반복 사용 가능)
test_urls = ["https://www.naver.com"] * 20

# 스레드 개수 변경하며 테스트 실행
# for threads in [1, 2, 5, 10, 15, 20]:
#     test_shared_driver_speed(threads, test_urls)
'''
=================expected result=================
[INFO] 스레드 1개(드라이버 1개) 실행 시간: 24.95초
[INFO] 스레드 2개(드라이버 1개) 실행 시간: 13.35초
[INFO] 스레드 5개(드라이버 1개) 실행 시간: 11.34초
[INFO] 스레드 10개(드라이버 1개) 실행 시간: 11.33초
[INFO] 스레드 15개(드라이버 1개) 실행 시간: 11.32초
[INFO] 스레드 20개(드라이버 1개) 실행 시간: 11.31초
=================================================
'''