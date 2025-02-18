# DBManager 클래스 선언
import pymysql
import numpy
import pandas as pd

class DBManager :
    # 필드멤버 선언

    # 생성자
    def __init__(self) :
        self.con    = None
        self.cursor = None

    # DB 연결 메소드
    def DBOpen(self, host, dbname, id, pw) :
        try :
            self.con = pymysql.connect(
                host = host,
                user = id,
                password = pw,
                db = dbname,
                charset='utf8'
            )
            return True
        except Exception as e :
            print(e)
            return False

    # DB 연결 종료 메소드
    def DBClose(self) :
        self.con.close()

    # insert, update, delete 처리하는 메소드
    def execute(self, sql) :
        print(f"sql : {sql}")
        try :
            self.cursor = self.con.cursor()
            self.cursor.execute(sql)
            self.con.commit()
            self.cursor.close()
            return True
        except Exception as e :
            print(e)
            self.con.rollback()
            self.cursor.close()
            return False

    # select 처리 메소드
    def executeQuery(self, sql) :
        print(f"sql : {sql}")
        try :
            self.cursor = self.con.cursor()
            self.cursor.execute(sql)
            # 모든 데이터를 한번에 가져옵니다
            self.data = self.cursor.fetchall()
            return True
        except Exception as e :
            print(e)
            return False

    def insert_df(self, table_name, df) :

        # 컬럼명 및 VALUES(%s, %s, ...) 생성
        columns = ", ".join(df.columns)
        values  = ", ".join(["%s"] * len(df.columns))
        sql     = f"insert into {table_name} ({columns}) values ({values})"

        # DataFrame을 튜플 리스트로 변환
        data = [tuple(row) for row in df.to_numpy()]

        try:
            self.cursor = self.con.cursor()
            self.cursor.executemany(sql, data)  # 여러 개의 데이터를 실행
            self.con.commit()
            self.cursor.close()
            print(f"{len(data)}개의 데이터가 성공적으로 처리되었습니다.")
            print("="*50)
            return True
        except Exception as e:
            print(f"데이터 처리 중 오류 발생: {e}")
            self.con.rollback()
            return False

    # select 닫기 메소드
    def CloseQuery(self) :
        self.cursor.close()

    # get Total 메소드
    def GetTotal(self) :
        return len(self.data)

    # 컬럼 이름으로 컬럼 값 가져오는 메소드
    # 데이터의 인덱스 번호가 필요
    def GetValue(self, index, column) :

        # 커서 객체가 없거나, 가져온 데이터가 없으면
        if not self.cursor or not self.data:
            return ""

        # 인덱스가 범위를 벗어나면
        if index < 0 or index >= len(self.data) :
            return ""

        # 컬럼 이름이 빈문자열로 넘어오면
        if column == None or column == "" :
            return ""

        # 컬럼 번호를 세기
        column_count = -1

        # 컬럼 이름을 차례대로 가져오기
        for item in self.cursor.description :
            column_count += 1
            name = item[0]
            # 원하는 컬럼 이름을 찾음
            if column == name :
                # self.data[인덱스번호][컬럼번호]
                return self.data[index][column_count]
        return ""   # 컬럼 이름이 없으면

    # 전체 데이터를 df으로 받아오는 메소드
    def GetDf(self) :
        columns = []
        for item in self.cursor.description :
            columns.append(item[0])
        df = pd.DataFrame(self.data)
        df.columns = columns
        return df
    
        # 데이터프레임을 사용하여 업데이트를 실행하는 메소드
    def update_df(self, df):  # <--- 여기에 새로 추가된 메소드입니다
        try:
            self.cursor = self.con.cursor()
            for index, row in df.iterrows():
                update_sql = f"UPDATE news_comments SET analysis = 'T', sent_type = '{row['evaluation']}', sent_score = {row['score']} WHERE comment = '{row['comment']}'"
                print(f"sql : {update_sql}")
                self.cursor.execute(update_sql)
            self.con.commit()
            self.cursor.close()
            print(f"{len(df)}개의 데이터가 성공적으로 업데이트되었습니다.")
            return True
        except Exception as e:
            print(f"데이터 업데이트 중 오류 발생: {e}")
            self.con.rollback()
            return False