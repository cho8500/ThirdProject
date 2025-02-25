from DBManager import DBManager

import pandas as pd
import requests

# 분석할 종목과 코드 리스트
list = {
    "셀트리온" : "068270",
    "기아" : "000270",
    "두산에너빌리티" : "034020",
    "카카오" : "035720",
    "한화에어로스페이스" : "012450",
    "삼성SDI" : "006400",
    "한국전력" : "015760",
    "LG전자" : "066570",
    "SK하이닉스" : "000660",
    "현대차" : "005380"
}

# 데이터 정렬을 위한 시세 테이블 생성
all_sise_data = []

# 종목을 순회하며 시세 데이터 불러옴
for name, code in list.items() :

    print(f"{name} : {code} 시세 데이터 수집 시작...")

    agent_head = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36" }
    sise_table = None

    # 원하는 page(기간) 입력
    page = 18

    # ~ 검색 당일의 시세까지 가져오기
    # daily 코드(stock_01sise_ext_daily)와 같이 사용하면 중복 데이터가 발생할 수 있음
    for i in range(1, page+1) :

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
    trend_list = sise_table['전일비'] = sise_table['전일비'].apply(    lambda x: 'up' if '상승' in x else ('dn' if '하락' in x else ('fl' if '보합' in x else x)))
    traiding_volume_list = sise_table['거래량'].tolist()

    sise_table = pd.DataFrame({
        "date" : date_list,
        "name" : [name] * len(date_list),
        "code" : [code] * len(date_list),
        "trend": trend_list,
        "volume" : traiding_volume_list
    })

    # 날짜를 datetime 형식으로 변환
    sise_table['date'] = pd.to_datetime(sise_table['date'])

    # 2025년 6월 이전의 데이터를 필터링하여 삭제
    sise_table = sise_table[sise_table['date'] >= '2024.06.01']

    # 각각의 데이터프레임을 리스트에 저장
    all_sise_data.append(sise_table)

# 날짜 기준으로 모아서 정렬 하고 데이터프레임으로 변환
final_sise_table = pd.concat(all_sise_data).sort_values(by=["date", "name"], ascending=[True, True]).reset_index(drop=True)

print(final_sise_table)


# DB 처리
db = DBManager()
db.DBOpen(
    host   = "192.168.0.184",
    dbname = "third_project",
    id     = "cho",
    pw     = "ezen"
)
db.insert_df("tradingVolume", final_sise_table)
db.DBClose()