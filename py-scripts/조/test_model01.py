import torch
import pandas as pd
from transformers import AutoTokenizer as AT
from transformers import AutoModelForSequenceClassification as AMSC
from DBManager import DBManager

# GPU 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using Device : {device}")

# 모델 및 토크나이저 로드
# 1. model_name = "beomi/kcbert-base"
# 2. model_name = "beomi/KcELECTRA-base"
# 3. model_name = "snunlp/KR-FinBERT"
# 4. model_name = "beomi/KcELECTRA-base-v2022"

model_name = "beomi/KcELECTRA-base-v2022"

tokenizer  = AT.from_pretrained(model_name)
model      = AMSC.from_pretrained(model_name).to(device)
model.eval()

# DB 불러오기
db = DBManager()
db.DBOpen(
    host   = "192.168.0.184",
    dbname = "third_project",
    id     = "cho",
    pw     = "ezen"
)

sql = "SELECT id, row_cont FROM disc_analysis WHERE analysis = 'F';"
df = db.fetch_DF(sql)

# 데이터 처리
if df is None or df.empty :
    print("분석할 데이터 없음")
else :
    print(f"[INFO] {len(df)}개 데이터 감성분석 중")

    # 배치 처리
    batch_size = 16
    results    = []

    for i in range(0, len(df), batch_size) :
        batch = df.iloc[i : i + batch_size]
        texts = batch["row_cont"].tolist()

        inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt").to(device)

        # 분석 수행
        with torch.no_grad() :
            outputs = model(**inputs)

            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            neg_probs, pos_probs = probs[:, 0].cpu().numpy(), probs[:, 1].cpu().numpy()

        # 라벨 변환
        for id, text, neg, pos in zip(batch["id"], texts, neg_probs, pos_probs) :
            if abs(neg - pos) < 0.1 :
                sent_type = "neutral"
                sent_scr  = round(pos, 4)
            else :
                sent_type = "positive" if pos > neg else "negative"
                sent_scr  = round(max(neg, pos), 4)

            print(f"[{sent_type.upper()}] ({sent_scr:.4f}) {text[:80]}...")
'''
            results.append((sent_type, sent_scr, id))

    # DB 업데이트
    try :
        db.cursor = db.con.cursor()
        sql = "UPDATE disc_analysis SET sent_type = %s, sent_scr = %s WHERE id = %s;"
        db.cursor.executemany(sql, results)
        db.con.commit()

        print(f"[INFO] {len(results)}개 데이터 분석 완료 및 저장 완료")
    except Exception as e :
        print(f"[ERROR] 데이터 저장 중 오류 발생 : {e}")
        db.con.rollback()
    finally :
        db.cursor.close()
'''
db.DBClose()