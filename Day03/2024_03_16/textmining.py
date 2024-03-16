''' 24 - 03 - 09  텍스트마이닝 '''
'''
텍스트 마이닝 : 문자로 된 데이터에서 가치 있는 정보를 얻어내는 분석 기법

형태소 분석 : 문장을 구성하는 어절들이 어떤 품사인지 파악하는 과정
            ex)문장을/구성/하는/어절들이/어떤/품사/인지/파악/하는/과정

- KoNLPy 패키지 : 한글 텍스트 형태소 분석 패키지

KoNLPy 패키지 설치

유의사항
1. 운영체제 버전에 맞는 JAVA 설치, 환경 변수 편집
2. 의존성 패키지 설치 = pip install jpype1
3. pip install konlpy
Terminal -> Command Prompt(base) 있는지 확인

환경변수 없을시
변수 : JAVA_HOME
값 : 자바 서버 위치
'''

### 연설문 로드
'''
파이썬에서 텍스트 파일을 읽어올 때 open() 함수를 쓰게 된다.

인코딩 : 컴퓨터가 문자를 표현하는 방식, 문서마다 인코딩 방식이 다르기 때문에 문서 파일과
        프로그램의 인코딩이 맞지 않으면 문자가 깨지게 된다.
'''
path = 'C:/Data/python/'

moon = open(path + 'speech_moon.txt', encoding='UTF-8').read()
# print(moon)

### 가장 많이 사용된 단어 확인

## 1. 불필요한 문자 제거
''' re : 문자 처리 패키지 '''
import re

''' 
정규 표현식 : 특정한 규칙을 가진 문자열을 표현하는 언어 
[^가-힣] : 한글이 아닌 모든 문자라는 뜻을 가진 정규표현식
변수 = re.sub('[^가-힣]', '', 변수)       #한글의 모든것을 제외하곤 다 제거 repl 자리가 대체할 내용
'''
moon = re.sub('[^가-힣]', ' ', moon)
# print(moon)

## 2. 명사 추출 -konlpy.tag.hannanum()의 nouns()를 이용한다.
import konlpy

hannanum = konlpy.tag.Hannanum()

# a = hannanum.nouns('대한민국의 영토는 한반도와 그 부속 도서로 한다, 대한민국 영토')
# print(a)

nouns = hannanum.nouns(moon)
# print(nouns)

## 3. 데이터 프레임으로 전환

import pandas as pd

df_word = pd.DataFrame({
    'word': nouns
})

# print(df_word)

## 4. 단어 빈도표 생성
df_word['count'] = df_word['word'].str.len()  # 단어의 길이 변수 추가
# print(df_word)

## 4-1. 두 글자 이상 단어만 남기기
df_word = df_word.query('count >= 2')
# print(df_word.sort_values('count'))

## 4-2. 단어 빈도 구하기
df_word = df_word.groupby('word', as_index=False) \
    .agg(n=('word', 'count')) \
    .sort_values('n', ascending=False)
# print(df_word)

## 5. 단어 빈도 막대 그래프 - 시각화
top20 = df_word.head(20)
# print(top20)

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'font.family': 'Malgun Gothic',
                     'figure.dpi': '120',
                     'figure.figsize': [6.5, 6]})

# sns.barplot(data=top20, y='word', x='n')
# plt.show()


### 워드 클라우드 생성
''' pip install wordcloud'''
import wordcloud

## 1. 한글 폰트 설정
font = 'C:/Windows/Fonts/HMKMMAG.TTF'  # 폰트 선정 후 경로 지정

## 2. 단어와 빈도를 담은 딕셔너리 생성
dic_word = df_word.set_index('word').to_dict()['n']  # 데이터 프레임을 딕셔너리로 변환
# print(dic_word)

## 3. 워드 클라우드 생성
# from wordcloud import WordCloud
# wc = WordCloud(
#     random_state= 1234,         # 난수 고정
#     font_path= font,            # 폰트 설정
#     width = 400,                # 가로 크기
#     height = 400,               # 세로 크기
#     background_color= 'white'   # 뒷 배경 색상
# )
# img_wordcloud = wc.generate_from_frequencies(dic_word) # 워드 클라우드 생성
#
# plt.figure(figsize=(10,10))     # 가로 세로 크기 설정
# plt.axis('off')                 # 테두리 선 없애기
# plt.imshow(img_wordcloud)       # 출력물을 지정
# plt.show()                      # 그래프 생성


### 워드 클라우드 모양 바꾸기

## 1. mask 만들기
import PIL  # 이미지 처리 패키지

icon = PIL.Image.open(path + 'cloud.png')

import numpy as np

img = PIL.Image.new('RGB', icon.size, (255, 255, 255))
img.paste(icon, icon)
img = np.array(img)
# print(img)

## 2. 워드 클라우드 생성
wc = wordcloud.WordCloud(random_state=1234,
                         font_path=font,
                         width=400,
                         height=400,
                         background_color='white',
                         mask=img,  # 마스킹 이미지 삽입
                         colormap='inferno')  # 컬러맵 설정
img_wordcloud = wc.generate_from_frequencies(dic_word)

## 3. 워드 클라우드 출력
# plt.figure(figsize=(10,10))
# plt.axis('off')
# plt.imshow(img_wordcloud)
# plt.show()
