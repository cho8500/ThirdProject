import os
import subprocess
from datetime import datetime, timedelta

def log_exe_time (tag) :
    # 현재 날짜와 시간을 가져옵니다
    cur_time = datetime.now()

    # log.txt 파일에 이어쓰기로 이 파일이 실행된 시간을 기록
    with open('log.txt', 'a', encoding='utf-8') as file:
        file.write(
            f'실행 시각 : {tag} { cur_time.strftime("%Y-%m-%d %H:%M:%S")}\n')

log_exe_time("start")
#exit()

today = datetime.today()

# 이틀 전 데이터 긁어오기
target_time = today - timedelta(days=2)
target_time = target_time.strftime("%Y.%m.%d")

print(f"[대상 날짜 : {target_time}]")

# datetype = "yyyy.mm.dd"
start_date = "2025.02.25"
end_date   = "2025.02.25"

# start_date = target_time
# end_date   = target_time

# 실행할 Python 파일
scripts = [
    ("./cho/discussion_list_crawling.py", [start_date, end_date]),
    ("./cho/discussion_post_crawling.py", []),
    ("./cho/discussion_sentiment.py",     [])
]

log_dir = "./cho/log"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"/log_{target_time}.txt")

with open(log_file, "w", encoding="UTF-8") as log :

    for script, args in scripts:
        log_exe_time(script)
        try :
            log.write(f"[파일 실행] {script}\n")

            print(f"[INFO] 실행 중: {script} {''.join(args) if args else ''}")

            result = subprocess.run(["python", script, *args],
                                    stdout=log,
                                    stderr=log,
                                    text=True
                                    )

            if result.returncode != 0 :
                log.write(f"[ERROR] {script} 실행 중 오류 발생\n")
                print(f"[ERROR] {script} 실행 중 오류 발생")
                break

        except Exception as e :
            log.write(f"[ERROR] 예외 발생 : {e}\n")
            print(f"[ERROR] 예외 발생 : {e}")
            break

    log.write("[INFO] 모든 스크립트 실행 완료")

print(f"[INFO] 모든 스크립트 실행 완료 : 로그파일 저장({log_file})")