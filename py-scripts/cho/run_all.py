import subprocess
from datetime import datetime

# datetype = "yyyy.mm.dd"
start_date = "2024.06.01"
end_date   = "2024.10.31"

# 실행할 Python 파일
scripts = [
    ("./cho/discussion_list_crawling.py", [start_date, end_date]),
    ("./cho/discussion_post_crawling.py", []),
    ("./cho/discussion_sentiment.py",     [])
]

for script, args in scripts:
    try :
        print(f"[INFO] 실행 중: {script} {''.join(args) if args else ''}")

        result = subprocess.run(["python", script, *args], stdout=None, stderr=None, text=True)

        if result.returncode != 0 :
            print(f"[ERROR] {script} 실행 중 오류 발생")
            break

    except Exception as e :
        print(f"[ERROR] 예외 발생 : {e}")
        break

print("[INFO] 모든 스크립트 실행 완료")
