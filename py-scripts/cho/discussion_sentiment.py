import pandas as pd
from DBManager import DBManager
from __LSTM.predic import sentiment_predict

# DB에서 전처리할 데이터 불러오기
def fetch_cont() :

    db = DBManager()
    db.DBOpen(
        host   = "192.168.0.184",
        dbname = "third_project",
        id     = "cho",
        pw     = "ezen"
        # host   = "localhost",
        # dbname = "third_project",
        # id     = "root",
        # pw     = "chogh"
    )

    sql = "SELECT id, title, comment FROM discussion WHERE analysis = 'F'"

    df = db.fetch_DF(sql)
    db.DBClose()

    return df

# 데이터 전처리
def preprocessing(df) :

    if df is None or df.empty :
        print("[INFO] 전처리할 데이터가 없습니다.")
        return None

    df["full_text"] = df["title"].fillna("") + " " + df["comment"].fillna("")

    df = df[~df["full_text"].str.contains(r"https:", regex=True)]
    df = df[~df["full_text"].str.contains(r"[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z ]", regex=True)]

    df["full_text"] = df["full_text"].str.replace(r"[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z ]", "", regex=True)
    df["full_text"] = df["full_text"].str.replace("\\s+", " ", regex=True).str.strip()

    return df

# 감성분석 실행
def sent_analysis(df) :

    if df is None or df.empty :
        print("[INFO] 감성분석할 데이터가 없습니다.")
        return None

    df["sent_score"] = df["comment"].apply(sentiment_predict)
    df["sent_type"]  = df["sent_score"].apply(lambda x : "positive" if x > 55 else ("negative" if x < 45 else "neutral"))

    return df

# DB에 결과 저장
def save_to_DB(df) :

    if df is None or df.empty :
        print("[INFO] 저장할 데이터가 없습니다.")
        return None

    db = DBManager()
    db.DBOpen(
        host   = "192.168.0.184",
        dbname = "third_project",
        id     = "cho",
        pw     = "ezen"
        # host   = "localhost",
        # dbname = "third_project",
        # id     = "root",
        # pw     = "chogh"
    )

    for _, row in df.iterrows():
        sql = """
            UPDATE discussion
            SET sent_type = %s, sent_score = FORMAT(%s, 2), analysis = 'T'
            WHERE id = %s;
        """
        values = (row["sent_type"], row["sent_score"], row["id"])
        db.execute(sql, values)

    db.DBClose()

def main() :

    df = fetch_cont()
    df = preprocessing(df)
    df = sent_analysis(df)
    save_to_DB(df)
    print("[INFO] 감성분석 완료 및 저장 완료")



'''--------실행--------'''
if __name__ == "__main__" :
    main()
