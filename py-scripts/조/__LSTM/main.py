import json
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from konlpy.tag import Okt

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# =====================================================================================================
# 1. 데이터 불러오기 및 전처리

file_name_train = "ratings_train.txt"
file_name_test  = "ratings_test.txt"

# 불용어 리스트
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

okt = Okt()

train_data = pd.read_table(file_name_train)
test_data  = pd.read_table(file_name_test)

print("원본 train_data.shape:", train_data.shape)
print("원본 test_data.shape :", test_data.shape)

# 중복 제거
train_data.drop_duplicates(subset=['document'], inplace=True)
test_data.drop_duplicates(subset=['document'],  inplace=True)

# 결측 제거 : 한글만 남김
train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","", regex=True)
train_data['document'] = train_data['document'].str.replace('^ +', "", regex=True)
train_data['document'].replace('', np.nan, inplace=True)
train_data.dropna(how='any', inplace=True)

test_data['document'] = test_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","", regex=True)
test_data['document'] = test_data['document'].str.replace('^ +', "", regex=True)
test_data['document'].replace('', np.nan, inplace=True)
test_data.dropna(how='any', inplace=True)

print("전처리 후 train_data.shape:", train_data.shape)
print("전처리 후 test_data.shape :", test_data.shape)

# =====================================================================================================
# 2. 형태소 분석(Okt) 및 불용어 제거

X_train_tokens = []
for sentence in tqdm(train_data['document']):
    tokenized = okt.morphs(sentence, stem=True)
    stopwords_removed = [w for w in tokenized if w not in stopwords]
    X_train_tokens.append(stopwords_removed)

X_test_tokens = []
for sentence in tqdm(test_data['document']):
    tokenized = okt.morphs(sentence, stem=True)
    stopwords_removed = [w for w in tokenized if w not in stopwords]
    X_test_tokens.append(stopwords_removed)

# 라벨
y_train = np.array(train_data['label'], dtype=int)
y_test  = np.array(test_data['label'],  dtype=int)

# =====================================================================================================
# 3. 정수 인코딩 (Tokenizer)

# 3-1) 전체 단어 빈도수를 먼저 파악
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train_tokens)

threshold  = 3  # 예: 3회 미만 출현 단어 제외
total_cnt  = len(tokenizer.word_index)
rare_cnt   = 0
total_freq = 0
rare_freq  = 0

for key, value in tokenizer.word_counts.items():
    total_freq += value
    if value < threshold:
        rare_cnt += 1
        rare_freq += value

print("단어 집합(vocabulary) 크기 : ", total_cnt)
print("등장 빈도수가 %d 미만인 희귀 단어의 수 : %d" % (threshold, rare_cnt))
print("희귀 단어 비율 : %.2f%%" % (rare_cnt/total_cnt*100))
print("전체 등장 빈도 중 희귀 단어 등장 비율 : %.2f%%" % (rare_freq/total_freq*100))

vocab_size = total_cnt - rare_cnt + 1  # 패딩 토큰 고려하여 +1
print("=> 실제 사용할 단어 집합 크기:", vocab_size)

# 3-2) Tokenizer 재정의
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(X_train_tokens)

# 정수 시퀀스로 변환
X_train = tokenizer.texts_to_sequences(X_train_tokens)
X_test  = tokenizer.texts_to_sequences(X_test_tokens)

# =====================================================================================================
# 4. 길이가 0인 샘플(빈 샘플) 제거

drop_train = [i for i, x in enumerate(X_train) if len(x) == 0]
X_train = np.delete(X_train, drop_train, axis=0)
y_train = np.delete(y_train, drop_train, axis=0)

print("빈 샘플 제거 후: X_train =", len(X_train), "y_train =", len(y_train))

# =====================================================================================================
# 5. 패딩 (문장 길이 통일)

max_len = 30  # 예: 30

X_train = pad_sequences(X_train, maxlen=max_len)
X_test  = pad_sequences(X_test,  maxlen=max_len)

print("최종 X_train.shape:", X_train.shape)
print("최종 X_test.shape :",  X_test.shape)

# =====================================================================================================
# 6. 전처리 데이터 저장 (피클/ JSON)

# 6-1) X, y 저장
with open("X_train_f.pickle","wb") as fw:
    pickle.dump(X_train, fw)
with open("y_train_f.pickle","wb") as fw:
    pickle.dump(y_train, fw)

with open("X_test_f.pickle","wb") as fw:
    pickle.dump(X_test, fw)
with open("y_test_f.pickle","wb") as fw:
    pickle.dump(y_test, fw)

# 6-2) word_index 저장
word_index_json = json.dumps(tokenizer.word_index, ensure_ascii=False)
with open("wordIndex.json","w", encoding='utf-8') as f:
    f.write(word_index_json)

# =====================================================================================================
# 7. 모델 구성 & 학습

embedding_dim = 100
hidden_units = 128

model = Sequential()
model.add(Embedding(input_dim=vocab_size,
                    output_dim=embedding_dim,
                    input_length=max_len))
model.add(LSTM(hidden_units))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# =====================================================================================================
# 8. 최적화

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
# 주의: metrics=['accuracy'] → 'val_accuracy'라는 이름이 로그에 찍힘
mc = ModelCheckpoint('best_model.h5',
                     monitor='val_accuracy',
                     mode='max',
                     verbose=1,
                     save_best_only=True)

history = model.fit(X_train, y_train,
                    epochs=15,
                    batch_size=512,
                    validation_split=0.2,
                    callbacks=[es, mc])

# =====================================================================================================
#  best_model 평가
best_model = load_model('best_model.h5')
loss, acc = best_model.evaluate(X_test, y_test, verbose=0)
print("\n테스트 정확도: %.4f" % acc)

print("main.py 끝 - 모든 파일과 모델 저장 완료")
