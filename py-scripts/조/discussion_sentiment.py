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

    sql = "SELECT id, comment FROM discussion WHERE analysis = 'T'"

    df = db.fetch_DF(sql)
    db.DBClose()

    return df

# 데이터 전처리
def preprocessing(df) :

    df["comment"] = df["comment"].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣0-9 ]", "", regex=True)
    df["comment"] = df["comment"].str.replace("\\s+", " ", regex=True)
    df.dropna(subset=["comment"], inplace=True)

    return df

# 감성분석 실행
def sent_analysis(df) :

    df["sent_score"] = df["comment"].apply(sentiment_predict)
    df["sent_type"]  = df["sent_score"].apply(lambda x : "positive" if x > 55 else ("negative" if x < 45 else "neutral"))

    return df

# DB에 결과 저장
def save_to_DB(df) :

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
    if df.empty :
        print("[INFO] 분석할 데이터 없음")
        return

    df = preprocessing(df)
    df = sent_analysis(df)
    save_to_DB(df)
    print("[INFO] 감성분석 완료 및 저장 완료")



'''--------실행--------'''
if __name__ == "__main__" :
    main()
