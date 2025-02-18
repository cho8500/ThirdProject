import subprocess

# 실행할 Python 파일
scripts = [
    "./discussion_list_crawling.py",
    "./discussion_post_crawling.py",
    "./discussion_sentiment.py"
]

for script in scripts:
    try :
        print(f"실행 중: {script}")

        #result = subprocess.run(["python", script], capture_output=True, text=True)
        result = subprocess.run(["python", script], stdout=None, stderr=None, text=True)
        #print(result.stdout)

        if result.stderr:
            print(f"[ERROR] {script}\n{result.stderr}")
            break
    except Exception as e :
        print(e)

print("[INFO] 모든 스크립트 실행 완료")
