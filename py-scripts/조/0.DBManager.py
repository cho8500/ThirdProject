# DBManager 클래스 선언
import pymysql
import numpy
import pandas as pd

class DBManager :

    '''=========
    필드멤버 선언
    ========='''
    # 생성자
    def __init__(self) :
        self.con    = None
        self.cursor = None
        self.data   = []

    '''==========
    DB연결 및 종료
    =========='''
    # DB 연결
    def DBOpen(self, host, dbname, id, pw) :

        try :
            self.con = pymysql.connect(
                host = host,
                user = id,
                password = pw,
                db = dbname,
                charset='utf8'
            )
            self.cursor = self.con.cursor()
            return True

        except Exception as e :
            print(f"[DB 연결 오류] {e}")
            self.con    = None
            self.cursor = None
            return False

    # DB 종료
    def DBClose(self) :

        if self.con :
            self.con.close()
            self.con = None

    '''=================================
    SQL 실행 : INSERTION, UPDATE, DELETE
    ================================='''
    # INSERT, UPDATE, DELETE
    def execute(self, sql, values=None) :
        print(f"SQL : {sql}")

        try :
            self.cursor = self.con.cursor()

            if values :
                self.cursor.execute(sql, values)
            else :
                self.cursor.execute(sql)

            self.con.commit()
            return True

        except Exception as e :
            print(f"[SQL 실행오류] {e}")
            self.con.rollback()
            return False

        finally :
            if self.cursor :
                self.cursor.close()

    # INSERT DF
    def insert_df(self, table_name, df) :

        # 컬럼명 및 VALUES(%s, %s, ...) 생성
        columns = ", ".join(df.columns)
        values  = ", ".join(["%s"] * len(df.columns))
        sql     = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

        # DataFrame을 튜플 리스트로 변환
        data = [tuple(row) for row in df.to_numpy()]

        try:
            self.cursor = self.con.cursor()
            self.cursor.executemany(sql, data)  # 여러 개의 데이터를 실행
            self.con.commit()
            print(f"{len(data)}개의 데이터가 성공적으로 처리되었습니다.")
            return True

        except Exception as e:
            print(f"[데이터 처리 오류] {e}")
            self.con.rollback()
            return False

        finally :
            if self.cursor :
                self.cursor.close()

    '''==============
    SQL 실행 : SELECT
    =============='''
    # SELECT
    def executeQuery(self, sql, values=None) :
        print(f"SQL : {sql}")

        try :
            self.cursor = self.con.cursor()

            if values :
                self.cursor.execute(sql, values)
            else :
                self.cursor.execute(sql)

            self.data = self.cursor.fetchall()
            return True

        except Exception as e :
            print(f"[SQL 조회오류] {e}")
            self.data = []
            return False

        finally :
            if self.cursor :
                self.cursor.close()

    # SELECT 결과를 DF로 반환
    def fetch_DF(self, sql, values=None) :

        if self.executeQuery(sql, values) :
            column = [desc[0] for desc in self.cursor.description]
            df     = pd.DataFrame(self.data, columns=column)
            return df

        return None

    # SELECT 데이터의 개수를 반환
    def GetTotal(self) :
        return len(self.data)

    # SELECT 데이터의 컬럼 이름으로 컬럼 값 가져오기
    # 데이터의 인덱스 번호가 필요
    def GetValue(self, index, column) :

        try :
            # 커서 객체가 없거나, 가져온 데이터가 없으면
            if not self.cursor or not self.data:
                return "cursor 객체 없음"

            # 인덱스가 범위를 벗어나면
            if index < 0 or index >= len(self.data) :
                return "인덱스 범위 벗어남"

            # 컬럼 이름이 빈문자열로 넘어오면
            if column == None or column == "" :
                return "column 이름 또는 타입 오류"

            # 컬럼 인덱스를 dict로 저장
            column_map = {item[0] : idx for idx, item in enumerate(self.cursor.description)}

            # 해당 컬럼이 있으면 데이터 반환, 없으면 빈문자
            if column in column_map :
                return self.data[index][column_map[column]]
            else :
                return ""

        except Exception as e :
            print(f"[GetValue 오류] {e}")
            return ""



    '''======================================================
    [불용처리]

    # SELECT 닫기 : 각 함수 안으로 포함
    def CloseQuery(self) :
        self.cursor.close()

    # SELECT 한 전체 데이터를 df으로 받아오는 메소드
    # executeQuery -> GetDf 세트로 사용 : fetchDF() 함수로 통합
    def GetDf(self) :
        columns = []
        for item in self.cursor.description :
            columns.append(item[0])
        df = pd.DataFrame(self.data)
        df.columns = columns
        return df
    ======================================================='''