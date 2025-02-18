import subprocess

# 실행할 Python 파일
scripts = [
    "./조/discussion_list_crawling.py",
    "./조/discussion_post_crawling.py",
    "./조/discussion_sentiment.py"
]

for script in scripts:

    print(f"실행 중: {script}")

    result = subprocess.run(["python", script], capture_output=True, text=True)
    print(result.stdout)

    if result.stderr:
        print(f"[ERROR] {script}\n{result.stderr}")
        break

print("[INFO] 모든 스크립트 실행 완료")
