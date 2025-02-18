# -*- coding: utf-8 -*-
# =====================================================================================================
# predic.py
# - 학습되어 저장된 best_model.h5 불러오기
# - wordIndex.json 불러오기
# - 사용자 입력 문장에 대한 감성분석

import re
import json
import numpy as np
import pandas as pd
import tensorflow as tf

from konlpy.tag import Okt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# =====================================================================================================
# 1. 사용자 정의 파라미터

max_len = 30   # 학습 시 사용했던 패딩 길이
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','을','으로','자','에','와','한','하다']

# =====================================================================================================
# 2. 모델 및 word_index 로드

model_path = "./조/__LSTM/best_model.h5"      # 이미 학습된 모델 파일
word_index_path = "./조/__LSTM/wordIndex.json" # 학습 시 사용한 word_index (Tokenizer) 정보

print("[INFO] 모델 및 word_index 로딩 중...")

loaded_model = load_model(model_path)

with open(word_index_path, "r", encoding='utf-8') as fr:
    word_index = json.load(fr)

print("[INFO] 모델 및 word_index 로딩 완료")

# =====================================================================================================
# 3. 감성분석 함수 정의

okt = Okt()

def sentiment_predict(sentence):
    # 1) 한글, 공백 외 문자 제거
    sentence = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", sentence)

    # 2) 형태소 분석
    tokens = okt.morphs(sentence, stem=True)

    # 3) 불용어 제거
    tokens = [w for w in tokens if w not in stopwords]

    # 4) word_index를 이용해 정수 인코딩
    #    - 만약 word_index에 없는 단어는 OOV 처리를 해줄 수 있음 (여기서는 2번 토큰 등)
    encoded = []
    for w in tokens:
        if w in word_index:
            encoded.append(word_index[w])
        else:
            encoded.append(2)  # 임의로 OOV(Out-Of-Vocabulary)를 2번 토큰으로 처리

    # 5) 패딩
    pad_seq = pad_sequences([encoded], maxlen=max_len)

    # 6) 예측
    score = float(loaded_model.predict(pad_seq))

    # 7) 결과 해석
    scr = score*100
    # print(f"{scr:.2f}")

    return scr

    '''
    if score > 0.5:
        print(f"[긍정] {score*100:.2f}% 확률로 긍정 리뷰입니다.\n")
    else:
        print(f"[부정] {(1-score)*100:.2f}% 확률로 부정 리뷰입니다.\n")
    '''

# =====================================================================================================
# 4. 감성분석 테스트

if __name__ == "__main__":

    list = ["삼성전자","SK하이닉스","LG에너지솔루션","삼성바이오로직스","현대차","기아","셀트리온","KB금융","네이버","카카오"]

    for item in list:

        df = pd.read_csv(f"./companies/{item}/1d_{item}_20250205_dic_arealist.csv", encoding='utf-8')
        df = df["기사내용"]
        df.replace("\n", "")
        df.replace("\t", "")

        sum = 0

        for sent in df:
            scr = sentiment_predict(sent)
            sum += scr

        avg_list = {'평균': [], '날짜' : []}
        df = pd.DataFrame(avg_list)

        avg = round(sum / df.size, 2)
        newrow = {'평균' : avg, '날짜' : 20250205 }
        df = df.append(newrow, ignore_index=True)
        df["날짜"] = df["날짜"].astype(int)
        print(df)
        df.to_csv(f"./companies/{item}/6m_{item}_avg_result.csv",encoding="utf-8")
        exit()

