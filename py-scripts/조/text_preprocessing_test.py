import re
import emoji
from soynlp.normalizer import repeat_normalize
from DBManager import DBManager

# 정규 표현식 패턴 정의
pattern = re.compile(f'[^ .,?!/@$%~％·∼()\x00-\x7Fㄱ-ㅣ가-힣]+')  # 한글, 특수문자 허용
url_pattern = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

# 전처리 함수
def clean(x):
    x = pattern.sub(' ', x)  # 특수문자 제거
    x = emoji.replace_emoji(x, replace='')  # 이모지 제거
    x = url_pattern.sub('', x)  # URL 제거
    x = x.strip()  # 앞뒤 공백 제거
    x = repeat_normalize(x, num_repeats=2)  # 반복 문자 정규화 (ex: "ㅋㅋㅋㅋ" → "ㅋㅋ")

    return x

db = DBManager()
db.DBOpen(
    host   = "localhost",
    dbname = "third_project",
    id     = "root",
    pw     = "chogh"
)
sql = "SELECT row_cont FROM disc_analysis LIMIT 20;"

df = db.fetch_DF(sql)

if df is not None and not df.empty :
    test_sentences = df["row_cont"].tolist()
else :
    test_sentences = []

db.DBClose()

# 전처리 적용 및 결과 출력
for i, sentence in enumerate(test_sentences, 1):
    print(f"{i}. Before: {sentence}")
    print(f"   After : {clean(sentence)}\n")
