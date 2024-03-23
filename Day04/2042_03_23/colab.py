'''
## 리뷰 데이터 감성 분석
상품 및 서비스, 기관, 단체, 사회적 이슈, 사건 등에 관해서 소셜미디어에 남긴 의견을 수집하고 분석해서 사람들의 감성의 상태 및 태도에 대한 변화, 평가, 선호도 등을 파악하는 빅 데이터 기술
'''
'''
##pip 설치 파일
pip install tensorflow
pip install keras
pip install scikit-learn
pip install nltk
pip install konlpy
pip install pandas
pip install matplotlib
'''

### import
import pickle
import pandas as pd
import numpy as np
import re
import tqdm
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 데이터 로드

train_data = pd.read_table('ratings_train.txt')
test_data = pd.read_table('ratings_test.txt')

print('훈련용 리뷰 개수 :', len(train_data))
print(train_data[:5]) # 상위 5개 출력
print('테스트용 리뷰 개수 :', len(test_data))
print(test_data[:5])  # 상위 5개 출력

''' 데이터 정제 '''

# document 열과 label 열의 중복을 제외한 값의 개수
train_data['document'].nunique(), test_data['document'].nunique()

# 중복 제거
train_data.drop_duplicates(subset=['document'], inplace=True)
print('총 샘플의 개수 :', len(train_data))

train_data['label'].value_counts().plot(kind='bar')

# 정확한 개수 출력
print(train_data.groupby('label').size().reset_index(name='count'))

# 비어있는 값(NULL)이 있는지 확인
print(train_data.isnull().sum())

# NULL 이 어느 열에 존재 하는지 확인 -> 몇번째 인덱스인지?
train_data.loc[train_data.document.isnull()]

train_data = train_data.dropna(how='any') # NULL 이 존재하는 행 제거
print(train_data.isnull().sum)

# 제거 후 샘플 개수 최종 확인
print(len(train_data))

''' 데이터 전처리 '''

# 한글이랑 띄워쓰기 제외하고 모두 제거
train_data['document'] = train_data['document'].str.replace('[^ㄱ-ㅎ ㅏ-ㅣ 가-힣 ]','')
train_data[:5]

# NUll 변경, 존재 확인
train_data['document'] = train_data['document'].str.replace('^ +', '')  # whilte space를 empty 데이터로 변경
train_data['document'].replace('', np.nan, inplace=True)
print(train_data.isnull().sum())

train_data.loc[train_data.document.isnull()][:10]

train_data = train_data.dropna(how='any')
print(len(train_data))

# 테스트 데이터에 동일한 전처리 진행
test_data.drop_duplicates(subset=['document'], inplace=True)  # 중복 제거
test_data['document'] = test_data['document'].str.replace('[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','')
test_data['document'] = test_data['document'].str.replace('^ +', '')  # 공백 -> emp
test_data['document'].replace('', np.nan, inplace=True)
test_data = test_data.dropna(how='any')
print('전처리 후 테스트용 데이터 개수 :', len(test_data))

'''
##토큰화
토큰화 과정에서 불용어 제거 - 보편화된 불용어를 사용해도 무방하지만 우리가 다루고자 하는 데이터를 지속적으로 검토하면서 추가하는 경우가 대부분이다.
'''

stopwords = ['의', '가', '이', '은', '들', '는', '좀', '걍', '잘', '과', '도', '를',
             '으로', '자', '에', '와', '한', '하다']

okt = Okt()
okt.morphs('와 이런것도 영화라고 차라리 뮤직비디오가 나을 뻔', stem=True)

# 불용어를 제거하고 x_train 이라는 리스트에 넣어주는 작업
from tqdm import tqdm

X_train = [] # 채워줄 빈 리스트 생성
for sentence in tqdm(train_data['document']):
  tokenized_sentence = okt.morphs(sentence)
  stopwords_remove_sentence = [word for word in tokenized_sentence if not word in stopwords]  # 불용어 제거 코드
  X_train.append(stopwords_remove_sentence)

print(X_train[:5])

# 테스트 데이터에 토큰화, 불용어 제거 진행
X_test = []

for sentence in tqdm(test_data['document']):
  tokenized_sentence = okt.morphs(sentence)
  stopwords_remove_sentence = [word for word in tokenized_sentence if not word in stopwords]
  X_test.append(stopwords_remove_sentence)

print(X_test[:5])

'''
##정수 인코딩
1. 토큰화가 진행되고 난 다음에 떨어지는 모든 단어에 각자 고유의 번호(정수)를 붙여준다.
2. 각 정수는 데이터에서 등장 빈도수가 높은 순서대로 부여가 된다. -> 인덱스 숫자가 큰 단어들은 빈도수가 낮다.
3. 등장 빈도수가 3회 미만인 단어들이 우리데이터에서 얼마나 비중을 차지하는지 확인하고 제거를 진행하도록 한다.
'''

# 훈련 데이터에서 단어 집합을 생성

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

print(tokenizer.word_index)


threshold = 3

total_cnt = len(tokenizer.word_index)   # 총 단어의 수
rare_cnt = 0    # 등장 빈도수가 3보다 작은 단어의 수
total_freq = 0  # 훈련 데이터의 전체 단어 빈도수 총합
rare_freq = 0   # 등장 빈도수가 3보다 작은 단어의 등장 빈도수 총합

# 단어와 빈도수의 쌍을 key와 value로 받아본다.
import time
for key, value in tokenizer.word_counts.items():  # items() : 결과값을 쌍으로 반환해주는 함수
  #print(key, value)
  total_freq = total_freq + value
  # print(total_freq)
  # time.sleep(1)

  if(value < threshold):    # 등장 빈도수가 3보다 작을 때
    rare_cnt = rare_cnt + 1
    rare_freq = rare_freq + value

print('단어 집합의 크기 :', total_cnt)
print('등장 빈도가 %s 번 이하인 희귀 단어의 수 : %s' %(threshold -1, rare_cnt))
print('단어 집합에서 희귀 단어의 비율 :', (rare_cnt/total_cnt)*100, '%')
print('전체 등장 빈도에서 희귀 단어의 빈도 비율 :', (rare_freq/total_freq)*100, '%')

''' 결과값을 보아하니 등장 빈도가 2번이하인 단어들은 자연어 처리과정에서 별로 중요하지 않을 수 있다.'''

# 등장 빈도수가 2 이하인 단어들의 수를 제외한 단어의 개수를 단어 집합 최대 크기로 제한한다.
# 전체 단어 개수 중 빈도가 2 이하인 단어는 제거

vocab_size = total_cnt - rare_cnt + 1 # 0 번을 고려
print('단어 집합의 크기 :', vocab_size)

# 32314 를 keras 토크나이저의 인자로 넘겨주고, 텍스트를 정수로 변환

tokenizer = Tokenizer(vocab_size)
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train) # 시퀀스로 변환
X_test = tokenizer.texts_to_sequences(X_test) # 테스트도 변환

print(X_train[:5])

y_train = np.array(train_data['label'])
y_test = np.array(test_data['label'])

''' 만약에 빈도수가 낮은 단어만으로 구성된 샘플은 빈(empty) 데이터가 되었다는 의미 -> 제거해준다. '''

drop_train = [index for index, sentence in enumerate(X_train) if len(sentence) < 1]

# 빈 샘플 제거
X_train = np.delete(X_train, drop_train, axis = 0)
y_train = np.delete(y_train, drop_train, axis = 0)
print(len(X_train))
print(len(y_train))

'''
## 패딩

서로 다른 길이의 샘플들의 길이를 동일하게 맞춰주는 작업
'''

from matplotlib import pyplot as plt

print('리뷰의 최대 길이 :', max(len(review) for review in X_train))
print('리뷰의 평균 길이 :', sum(map(len, X_train))/len(X_train))
plt.hist([len(review) for review in X_train], bins = 50)
plt.xlabel('Length of Samples')
plt.ylabel('Number of Samples')
plt.show