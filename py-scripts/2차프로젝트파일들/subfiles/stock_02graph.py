import pandas as pd
import matplotlib.pyplot as plt

# 종목 가져오기
list = ["삼성전자"]

# ,"SK하이닉스","LG에너지솔루션","삼성바이오로직스","현대차","기아","셀트리온","KB금융","네이버","카카오"

for item in list :

    # csv파일 가져오기
    '''경로 수정'''
    #df = pd.read_csv(f"./{item}/6m_{item}_sise.csv", encoding='utf-8')
    df = pd.read_csv(f"./companies/{item}/6m_{item}_20250205_sise.csv", encoding='utf-8')

    # 오래된 자료부터 새로운 자료순으로 정렬
    df = df.sort_index(ascending = False)

    dates      = df["날짜"]
    SiseJongga = df["종가"] # 종가 값만 불러오기

    '''있어야하나? 주석처리하고 결과값 같이 써놓기'''
    print(f"타입{type(SiseJongga)}")

    '''이 함수가 꼭 for문 안에 있어야하나?'''
    def toInteger(data) :
        data = str(data)
        data = data.replace(".0","")    # 소수점 제거
        data = int(data)                # 타입을 int로 변환
        return data

    SiseJongga = SiseJongga.apply(toInteger)
    print(f"타입{type(SiseJongga)}")
    #print(SiseJongga)

    # ================== 그래프 ==================
    import matplotlib.dates as mdates

    # 한글 폰트 설정
    plt.rc('font', family="Malgun Gothic")

    # 마이너스 기호 설정; 한글 폰트일 경우, 숫자 값중 음수(마이너스 기호)에 문제가 발생
    plt.rcParams['axes.unicode_minus'] = False

    # 데이터 준비
    x = dates
    y = SiseJongga

    # 그래프 사이즈 설정
    plt.figure(figsize=(9,7))

    # 그래프 그리기
    plt.plot(
        x, y,
        color     = "gray",
        linestyle = '-',
        linewidth = 2,
        label     = "주가 동향"
        )

    # 그래프 제목설정
    plt.title(
        f"{item} 주가 동향",
        fontsize = 20,
        color    = "black"
    )

    plt.xlabel("날짜")          # x축 이름
    plt.ylabel("주가")          # y축 이름
    plt.legend(loc = "best")    # 범례 위치

    # x, y 눈금 xticks yticks
    plt.xticks(ticks = x, labels = x, fontsize = "12", rotation = 45)
    plt.yticks(fontsize = "15")

    # 날짜 간격 두기
    plt.locator_params(axis = 'x', nbins = len(x) / 10)

    # 격자선 추가
    plt.grid(
        color     = "gray",
        linestyle = "-",
        axis      = "both",
        alpha     = 0.3
    )

    # 그래프 저장하고 보여주기
    plt.savefig(f"./companies/{item}/6m_{item}주가그래프.png")
    plt.show()
