import pandas as pd
import requests

from bs4 import BeautifulSoup

# 분석할 종목 리스트

list = ["삼성전자"]

for item in list :

    # csv파일 읽어오기
    '''파일경로, 인코딩 확인'''
    # df = pd.read_csv(f"./companies/{item}/1d_{item}_20250205_link.csv", encoding="euc-kr")
    df = pd.read_csv(f"./companies/삼성전자/1d_삼성전자_20250205_link.csv", encoding="utf-8")

    # csv파일에서 링크 추출
    urlList = df["링크"]
    agent_head = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36" }

    dic_arealist =[]

    for url_item in urlList :

        result = requests.get(url = url_item, headers = agent_head)
        html   = result.text
        soup   = BeautifulSoup(html, "html.parser")

        #title = soup.find("article", class_="newsct_body")

        #기사내용 뽑아오기
        dic_area = soup.select_one("#dic_area")

        # dic_area가 없으면 진행하지 않고 다음 반복으로 넘어감
        img_desc = soup.select_one("#dic_area > span.end_photo_org")        # 사진의 설명 제거하기  ### 이해가 어려움

        # img_desc 가 없을때
        # 기사에 사진이 없음
        if img_desc :
            # 사진이 있음 -> 사진 설명 제거
            img_desc.decompose()                            # soup 자체에서 사라짐

        # 사진 설명까지 제거된 기사 내용을 가져옴
        dic_area_text = dic_area.get_text()
        print(dic_area_text)
        # exit()

        #dic_area_text = ()
        if dic_area :                                                        #내용이 없으면 실행 도중에 오류가 남.
            dic_area_text = dic_area.get_text()                              #문자만 가져오기
        print(dic_area_text)                                                 #기사내용 프린트 해보기
        dic_arealist.append(dic_area_text)                                   #기사내용 순서대로 다 입력

    contents = pd.DataFrame(dic_arealist, columns=["기사내용"])               #데이터프레임화
    # contents.to_csv(f"./companies/{item}/1d_{item}_20250205_dic_arealist.csv", encoding="utf-8")

    contents.to_csv(f"./companies/삼성전자/1d_삼성전자_20250205_dic_arealist.csv", encoding="utf-8")
    print(f"{item} 관련 기사내용이 저장되었습니다.")

