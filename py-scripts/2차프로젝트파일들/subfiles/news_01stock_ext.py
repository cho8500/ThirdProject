import requests
from bs4 import BeautifulSoup
import os

def get_stocks():

    url      = "https://finance.naver.com/sise/sise_market_sum.naver"
    headers  = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers = headers)
    soup     = BeautifulSoup(response.text, "html.parser")

    # 시가총액 상위 10개 기업 가져오기
    stock_elements = soup.select("table.type_2 tbody tr td a.tltle")[:15]

    top_stocks = []

    for stock in stock_elements:

        stock_name = stock.text.strip()

        # "삼성전자우" 제외
        if stock_name != "삼성전자우":
            top_stocks.append(stock_name)
                
        # 가져온 종목 목록으로 파일 생성
        folder_path = f"./companies/{stock_name}"

        # 폴더 생성, 이미 폴더가 존재해도 에러 없이 코드가 실행됩니다.
        os.makedirs(folder_path, exist_ok = True)
    
        # 10개 종목만 가져오기
        if len(top_stocks) == 10:
            break
        
    return top_stocks

# 테스트 실행
if __name__ == "__main__":
    print(get_stocks())
