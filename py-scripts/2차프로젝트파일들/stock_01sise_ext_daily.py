from DBManager import DBManager
from datetime import datetime

import pandas as pd
import requests

# 분석할 종목과 코드 리스트
list = {
    "삼성전자" : "005930",
    "LG전자" : "066570",
    "SK하이닉스" : "000660",
    "삼성바이오로직스" : "207940",
    "현대차" : "005380",
    "기아" : "000270",
    "대한항공" : "003490",
    "KB금융" : "105560",
    "포스코" : "005490",
    "카카오" : "035720"
}

# 당일 데이터가 있다면 새로 받아오기 위해 삭제함
db = DBManager()
db.DBOpen(
    host   = "192.168.0.184",
    dbname = "second_project",
    id     = "cho",
    pw     = "ezen"
)

now = datetime.now()
current_date = now.date()
current_date_dash = current_date.strftime("%Y-%m-%d")

sql = f"delete from sise_data where date='{current_date_dash}';"
db.execute(sql)

# 종목을 순회하며 시세 데이터 불러옴
for name, code in list.items() :

    print(f"{name} : {code} 시세 데이터 수집 시작...")

    # 시세 데이터 url에서 데이터 가져오기
    agent_head = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36" }

    url = f"https://finance.naver.com/item/sise_day.naver?code={code}&page=1"
    print(f"url={url}")

    result = requests.get(url=url, headers=agent_head)
    html   = result.text
    result = pd.read_html(html)

    # html 코드에서 테이블을 데이터 프레임으로 변환
    df = result[0]

    sise_table = pd.DataFrame([{
        "date" : df['날짜'].dropna().iloc[0],
        "name" : name,
        "code" : code,
        "sise" : df['종가'].dropna().iloc[0]
    }])

    # DB 처리
    db.insert_df("sise_data", sise_table)

db.DBClose()