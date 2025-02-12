from DBManager import DBManager

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

# 데이터 정렬을 위한 시세 테이블 생성
all_sise_data = []

# 종목을 순회하며 시세 데이터 불러옴
for name, code in list.items() :

    print(f"{name} : {code} 시세 데이터 수집 시작...")

    agent_head = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36" }
    sise_table = None

    # 원하는 page(기간) 입력
    page = 13

    # ~ 검색 당일의 시세까지 가져오기
    # daily 코드(stock_01sise_ext_daily)와 같이 사용하면 중복 데이터가 발생할 수 있음
    for i in range(1, page) :

        url = f"https://finance.naver.com/item/sise_day.naver?code={code}&page={i}"
        print(f"url={url}")

        result = requests.get(url=url, headers=agent_head)
        html   = result.text
        result = pd.read_html(html)

        #  html 코드에서 테이블을 데이터 프레임으로 변환
        df = result[0]

        # NaN 데이터 삭제
        df = df.dropna(subset=['날짜'], axis=0, how='any')

        # 데이터를 이어붙여서 저장
        if sise_table is None :
            sise_table = df
        else :
            sise_table = pd.concat([sise_table, df])

    # 시세 데이터를 데이터프레임화
    date_list = sise_table['날짜'].tolist()
    sise_list = sise_table['종가'].tolist()

    sise_table = pd.DataFrame({
        "date" : date_list,
        "name" : [name] * len(date_list),
        "code" : [code] * len(date_list),
        "sise" : sise_list
    })

    # 각각의 데이터프레임을 리스트에 저장
    all_sise_data.append(sise_table)

# 날짜 기준으로 모아서 정렬 하고 데이터프레임으로 변환
final_sise_table = pd.concat(all_sise_data).sort_values(by=["date", "name"], ascending=[True, True]).reset_index(drop=True)

# DB 처리
db = DBManager()
db.DBOpen(
    host   = "192.168.0.184",
    dbname = "second_project",
    id     = "cho",
    pw     = "ezen"
)
db.insert_df("sise_data", final_sise_table)
db.DBClose()