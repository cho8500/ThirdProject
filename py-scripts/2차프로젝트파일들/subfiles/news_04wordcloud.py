import requests
import pandas as pd

from bs4 import BeautifulSoup

contents = pd.read_csv("./companies/삼성전자/1d_삼성전자_20250205_dic_arealist.csv")

print(f"{contents.iloc[1]}인덱스")

contents = contents['기사내용'].iloc[1]

#contents.astype(str)

from konlpy.tag import Okt
okt = Okt()

#명사만 추출한다
nouns = okt.nouns(contents)
print(nouns)

#명사의 출현 빈도 산출
nouns.sort()
'''{
    '단어' : 빈도수,
    '단어' : 빈도수,
    ...
    }'''

dic = {}
for word in nouns :     # 명사 목록에서 명사 하나씩 꺼냅니다
    if word in dic :    # 꺼낸 명사가 dic의 키중에 있는지 확인
       # 키중에 명사가 있습니다.
       # -> 빈도수에 1을 더합니다.
       dic[word] += 1
    else :              # dic의 키중에 명사와 일치하는 키가 없음
        dic[word] = 1
#print(dic)


# dic은 정렬이 되지 않기에(dic의 키들은 순서가 없음)
# dic을 df로 변경해야 함
words = []
count = []
# dic의 키와 값을 각각 words, count리스트에 넣습니다
for key in dic :
    words.append(key)
    count.append(dic[key])

# word와 빈도수를 이용하여 df을 생성
import pandas as pd
# 컬럼으로 단어 목록을 사용하고, 데이터로 빈도수 목록을 사용
df = pd.DataFrame([words, count])
#print(df)

# 행과 열을 뒤집는다
df = df.transpose()
#print(df)

#컬럼을 '단어', '빈도수'로 지정한다
df.columns= ['단어', '빈도수']

#빈도수를 정수형으로 변환
df['빈도수'] = df['빈도수'].astype('int64')
#print(df.info())

#빈도수의 내림차순으로 정렬
df = df.sort_values(by="빈도수", ascending=False)
print(df.head())

#df 데이터로 시각화
# 빈도수 2 이하는 제거
# df[ 조건식 ] -> 슬라이싱 -> df["빈도수"] > 2 : df '빈도수'컬럼의 값이 2를 초과
df = df[ df ["빈도수"] > 2]
#print(df)

# 빈도수를 꺽은선 그래프로 출력하기
import matplotlib.pyplot as plt
from matplotlib import rc

rc('font', family="Malgun Gothic")
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(5,4), dpi = 150)
plt.plot(df["단어"], df["빈도수"], label="빈도수", marker="P")
plt.xticks(rotation = 45)
plt.legend
plt.title("단어별 빈도수 ")
plt.show()

# 단어의 빈도수 시각화 방법중 인기가 좋은 워드클라우드를 사용
# pip install wordcloud

from wordcloud import WordCloud

#워드 클라우드 셋팅
wc = WordCloud(
    font_path="HANYGO230.ttf",  # 폰트경로(파일명포함) << 수정필요 : ttf파일 subfiles로 옮김(2025.02.10)
    background_color="white" ,  # 배경색
    width = 800,               # 너비
    height=600                  # 높이
)
# 단어 : 빈도수 딕셔너리를 데이터로 받음
# df에서 dic를 생성
wordlist = {}
for i in range(len(df)) :
    # wordlist[단어] = 빈도수
    #df["단어"].iloc[i]
    #df["빈도수"].iloc[i]
    wordlist[df["단어"].iloc[i]] = df['빈도수'].iloc[i]
print(wordlist)

# 정제된 데이터로 워드클라우드 생성
wc.generate_from_frequencies(wordlist)
plt.figure(figsize=(8,6))
plt.imshow(wc)
plt.axis('off')
plt.show()

# 기사의 전체 단어 빈도수로 워드 클라우드 생성
wc.generate_from_frequencies(dic)
plt.figure(figsize=(8,6))
plt.imshow(wc)
plt.axis('off')
plt.savefig("./companies/삼성전자/1d_삼성전자_wordcloud.png", dpi=300, bbox_inches='tight')
plt.show()