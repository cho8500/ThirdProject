'''================
   CPU코어 개수 확인
   ================'''
import os
print("CPU 코어 개수:", os.cpu_count())


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
for workers in [2, 5, 10, 20, 50]:
    test_speed(workers)

'''
==========expecte result==========
[INFO] 스레드 1개 실행 시간: 20.02초
[INFO] 스레드 2개 실행 시간: 10.01초
[INFO] 스레드 5개 실행 시간: 4.05초
[INFO] 스레드 10개 실행 시간: 2.02초
[INFO] 스레드 20개 실행 시간: 2.01초
[INFO] 스레드 50개 실행 시간: 2.00초
==================================
'''