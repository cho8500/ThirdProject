import json
from DBManager import DBManager

# JSON 파일 경로
JSON_FILE_PATH = "./cho/stock_list.json"  # 파일 경로 수정 가능

# JSON 파일에서 종목 리스트 불러오기
def load_stock_list(json_file):

    with open(json_file, "r", encoding="utf-8") as file :
        stock_dict = json.load(file)

    return stock_dict

# stocks 테이블 업데이트
def update_stocks():
    stock_dict = load_stock_list(JSON_FILE_PATH)

    # DBManager 인스턴스 생성
    db = DBManager()

    db.DBOpen(
        host   = "192.168.0.184",
        dbname = "third_project",
        id     = "cho",
        pw     = "ezen"
    )

    try:
        # 새로운 데이터 INSERT
        sql = "INSERT INTO stocks (name, code) VALUES (%s, %s)"
        values = [(name, code) for name, code in stock_dict.items()]
        db.cursor.executemany(sql, values)  # 여러 개의 데이터를 한 번에 INSERT
        db.con.commit()

        print(f"[INFO] {len(values)}개 종목 데이터 삽입 완료.")

    except Exception as e:
        print(f"[ERROR] 데이터 삽입 중 오류 발생: {e}")
        db.con.rollback()

    finally:
        db.DBClose()
        print("[INFO] MySQL 연결 종료.")

if __name__ == "__main__":
    update_stocks()
