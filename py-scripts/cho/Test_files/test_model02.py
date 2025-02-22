import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 사용 모델 선택
# model_name = "beomi/KcELECTRA-base"
# model_name = "snunlp/KR-FinBERT"
# model_name = "beomi/kcbert-base"
model_name = "beomi/KcELECTRA-base-v2022"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 분석할 문장
text = "이 주식은 망할 것 같다."

# 토큰화
inputs = tokenizer(text, return_tensors="pt")

# 예측 실행
with torch.no_grad():
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

# 결과 출력
negative_prob = probs[0][0].item()
positive_prob = probs[0][1].item()

print(f"부정 확률: {negative_prob:.4f}, 긍정 확률: {positive_prob:.4f}")

"""
[이 주식은 망할 것 같다.]

beomi/KcELECTRA-base       : 부정 확률: 0.4947, 긍정 확률: 0.5053
snunlp/KR-FinBERT          : 부정 확률: 0.3292, 긍정 확률: 0.6708
beomi/kcbert-base          : 부정 확률: 0.3889, 긍정 확률: 0.6111
beomi/KcELECTRA-base-v2022 : 부정 확률: 0.5186, 긍정 확률: 0.4814
"""

