import pandas as pd
from __LSTM.predic import sentiment_predict  # predic.py의 감성 분석 함수 사용
from DBManager import DBManager

# DB 불러오기
db = DBManager()
db.DBOpen(
    host="192.168.0.184",
    dbname="third_project",
    id="cho",
    pw="ezen"
)

sql = "SELECT id, row_cont FROM disc_analysis WHERE analysis = 'F';"
df = db.fetch_DF(sql)

# 데이터 처리
if df is None or df.empty:
    print("분석할 데이터 없음")
else:
    print(f"[INFO] {len(df)}개 데이터 감성분석 중")

    # 감성 분석 실행
    for id, text in zip(df["id"], df["row_cont"]):
        score = sentiment_predict(text)  # predic.py의 감성 분석 함수 사용
        sentiment = "positive" if score > 50 else "negative"

        print(f"[{sentiment.upper()}] ({score:.2f}) {text[:80]}...")  # 80자 제한

db.DBClose()
