''' 24 - 03 - 09 강의 자료 '''

''' Review - 

1. 조건에 맞는 데이터만 추출
exam.query('nclass == 1') <- 1이 숫자가 아닌 문자일 시 1 양쪽에 "1" 이리  씀

2. 여러 조건
exam.query('nclass == 2 & math >= 50')  <- nclass가 2반이고 수학점수가 50점 이상

3. 필요한 변수만 추출
exam['math']
exam[['nclass','math','english']]   <- 여러 변수 추출

4. 정렬
exam.sort_values('math')    <- 수학점수를 기준으로 오름차순
exam.sort_values(['math', ascending = False]) <- 수학 점수를 기준으로 내림차순

5. 파생변수 추가
exam.assign(total = exam['math'] + exam['english'] + exam['science],
            mean = (exam['math'] + exam['english'] + exam['science])/3)
exam.assign(test = np.where(exam['science'] >= 60, 'pass', 'fail'))
            
6. 집단별로 요약
exam.groupby('nclass)\
    .agg(mean_math = ('math', 'mean'))
    
7. 데이터 합치기
pd.merge(test1, test2, how = 'left', on = 'id')     #가로로 합치기
pd.concat([group_a, group_b])                       #세로로 합치기

8. 결측치 정제
pd.isna(df).sum()       #결측치 확인
df_nomiss = df.dropna(subset = ['score'] #결측치 제거
df_nomiss = df.dropna(subset = ['score', 's']) #여러 변수 동시에 결측치 제거

9. 이상치
df['s'].value_counts()

# 이상치 결측 처리
df['s'] = np.where(df['s'] == 3, np.nan, df['s']

# 극단치 결측 처리
mpg['hwy'] = np.where((mpg['hwy'] < 4.5) | (mpg['hwy'] > 40.5),
                     np.nan, mpg['hwy'])
'''
# ------------------------------------------------------------------------------

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
    'word' : nouns
})

# print(df_word)

## 4. 단어 빈도표 생성
df_word['count'] = df_word['word'].str.len()       #단어의 길이 변수 추가
# print(df_word)

## 4-1. 두 글자 이상 단어만 남기기
df_word = df_word.query('count >= 2')
# print(df_word.sort_values('count'))

## 4-2. 단어 빈도 구하기
df_word = df_word.groupby('word', as_index=False)\
    .agg(n=('word', 'count'))\
    .sort_values('n', ascending=False)
# print(df_word)

## 5. 단어 빈도 막대 그래프 - 시각화
top20 = df_word.head(20)
# print(top20)

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'font.family' : 'Malgun Gothic',
                     'figure.dpi' : '120',
                     'figure.figsize' : [6.5,6]})

# sns.barplot(data=top20, y='word', x='n')
# plt.show()


### 워드 클라우드 생성
''' pip install wordcloud'''
import wordcloud

## 1. 한글 폰트 설정
font = 'C:/Windows/Fonts/HMKMMAG.TTF'   # 폰트 선정 후 경로 지정

## 2. 단어와 빈도를 담은 딕셔너리 생성
dic_word = df_word.set_index('word').to_dict()['n']      # 데이터 프레임을 딕셔너리로 변환
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
import PIL                         # 이미지 처리 패키지

icon = PIL.Image.open(path + 'cloud.png')

import numpy as np
img = PIL.Image.new('RGB', icon.size, (255, 255, 255))
img.paste(icon, icon)
img = np.array(img)
# print(img)

## 2. 워드 클라우드 생성
wc = wordcloud.WordCloud(random_state = 1234,
                         font_path = font,
                         width = 400,
                         height = 400,
                         background_color= 'white',
                         mask = img,            # 마스킹 이미지 삽입
                         colormap= 'inferno')   # 컬러맵 설정
img_wordcloud = wc.generate_from_frequencies(dic_word)

## 3. 워드 클라우드 출력
# plt.figure(figsize=(10,10))
# plt.axis('off')
# plt.imshow(img_wordcloud)
# plt.show()

# ------------------------------------------------------------------------------
''' 24 - 03 - 09  통계적 자료 분석 '''
import matplotlib.pyplot as plt

'''
통계적 가설 검정 : 유의 확률을 사용해서 가설을 검정하는 방법

- 유의학률 : 실제로는 집단 간에 차이가 없는데 우연히 차이가 있는 데이터가 추출될 확률
        -> 유의확률의 기준은 0.05

- 기술 통계 : 데이터를 요약해서 설명하는 통계 분석 기법
- 추론 통계 : 단순히 요약하는 것을 넘어서 어떤 값이 발생할 확률을 계산하는 분석 기법

    1) 이런 차이가 우연히 나타날 확률이 작다면 -> 성별 월급차이가 통계적으로 유의하다.
    2) 이런 차이가 우연히 나타날 확률이 크다면 -> 성별 월급차이가 통계적으로 유의하지 않다.
'''

'''
t-test (t 검정) : 두 집단의 평귬에 통계적으로 유의한 차이가 있는지 알아볼 때 사용하는 통계 분석 기법
'''

### compact 자동차와 suv 자동차의 도시 연비 t 검정
import pandas as pd
path = 'C:/Data/python/'
mpg = pd.read_csv(path + 'mpg.csv')

## 1. 기술 통계 분석 - 평균 비교
a = mpg.query('category in ["compact", "suv"]')\
    .groupby('category', as_index=False)\
    .agg(n = ('category', 'count'),
         mean = ('cty', 'mean'))
# print(a)

compact = mpg.query('category == "compact"')['cty']
# print(compact)
suv = mpg.query('category == "suv"')['cty']

## 2. t-test
from scipy import stats
result = stats.ttest_ind(compact, suv, equal_var=True)       # equal_var = True : 두 변수안의 값이 퍼짐 정도가 같다고 가정.
# print(result)

'''
pvalue=2.3909550904711282e-21 은 유의확률이 2.3905... 앞에 0이 21개 있는 값보다 작다는 의미다.
pvalue 가 0.05보다 작기 떄문에 이 분석 결과는
'compacy'차와 'suv'간 평균 도시 연비 차이가 통계적으로 유의미하다.
'''

### 일반 휘발유와 고급 휘발유의 도시 연비 t 검정
# print(mpg)

## 1. 기술 통계 분석
a = mpg.query('fl in ["r", "p"]')\
    .groupby('fl', as_index=False)\
    .agg(n = ('fl', 'count'),
         mean = ('cty', 'mean'))
# print(a)

## 2. t-test
r = mpg.query('fl == "r"')['cty']
p = mpg.query('fl == "p"')['cty']

result = stats.ttest_ind(r, p, equal_var=True)
# print(result)

'''
출력 결과를 보면 pvalue가 0.05보다 큰 0.287... 이다. 실제로는 차이가 없는데
우연에 의해 이런 정도의 차이가 관찰될 확률이 28.75% 라는 의미다.
따라서, 일반 휘발유와 고급 휘발유를 사용하는 자동차의 도시 연비 차이가 통계적으로 유의하지 않다.
'''

# ------------------------------------------------------------------------------
''' 
상관 분석 - 두 변수가 서로 관련이 있는지 검정하는 통계 분석 기법 

1. 상관계수 : 상관분석으로 도출되는 값
 -> 관련성의 정도를 0~1 사이의 값으로 표현
 -> 1에 가까울 수록 관련성이 크다.
 -> 상관계수가 양수면 정비례, 음수면 반비례  -1 0 1
'''

### 실업자 수와 개인 소비 지출의 관계
''' 가설 : 실업자 수가 증가하면 개인 소비 지출이 줄어들 것이다. '''
economics = pd.read_csv(path + 'economics.csv')
# print(economics)

## 1. 상관계수 구하기 - 상관행렬을 생성해서 구한다.
# print(economics[['unemploy', 'pce']].corr())        # 정비례 관계다.

## 2. 유의확률을 구하기 - df.corr() 이용하면 상관계수를 알 수 있지만 유의확률은 모른다.

result = stats.pearsonr(economics['unemploy'], economics['pce'])
# print(result)
'''
statistic=0.6145176141932082 <- 상관계수
pvalue=6.773527303289964e-61 <- 유의확률

유의확률이 0.05미만이므로 실업자 수와 개인 소비 지출의 상관관계가 통계적으로 유의하다.
'''

### 상관행렬 히트맵 만들기(여러 변수)

## 1. 상관행렬
mtcars = pd.read_csv(path + 'mtcars.csv')
# print(mtcars.head())

car_cor = mtcars.corr()
car_cor = round(car_cor, 2)     # 소수점 둘째 자리까지 반올림
# print(car_cor)

## 2. 히트맵 만들기 - 시각화
# plt.rcParams.update({'figure.dpi' : '120',
#                      'figure.figsize' : [7.5, 5.5] })   # 가로 세로 크기
#
# import seaborn as sns
# sns.heatmap(car_cor,
#             annot = True,       # 상관계수 표시 여부
#             cmap = 'RdBu')      # 컬러맵
#
# plt.show()

## 3. 대각 행렬 제거

## 3-1 mask 만들기
import numpy as np
import seaborn as sns

mask = np.zeros_like(car_cor)
# print(mask)

mask[np.triu_indices_from(mask)] = 1    # 오른쪽 위 대각 행렬을 1로 바꿔주는 함수
# print(mask)

## 3-2 히트맵에 적용
# sns.heatmap(car_cor,
#             annot = True,
#             fmt = 'd',
#             cmap = 'RdBu',
#             mask = mask)
# plt.show()

# ------------------------------------------------------------------------------
import seaborn as sns
import  matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# plt.rcParams.update({'figure.figsize' : [10,8]})
#
# flights = sns.load_dataset('flights')
# # print(flights.head())
#
# df = flights.pivot('month', 'year', 'passengers')  # 월별 연도별 승객수 집계한 피벗 테이블 생성

# movies = pd.read_csv(path + 'movies.csv', index_col='movieId')
# genres_dummies = movies['genres'].str.get_dummies(sep='|')

# print(genres_dummies)

# print(genres_dummies.corr())

''' 장르 A와 장르 B의 상관관계 : 어떤 영화가 장르 A를 가지고 있을때, 장르 B도 갖고 있는 정도를 말한다. '''

# plt.rcdefaults()
# import matplotlib as mpl
# mpl.rc_file_defaults()
#
# plt.figure(figsize=(30,20))
# sns.heatmap(genres_dummies.corr(), annot = True)
# plt.show()

# ------------------------------------------------------------------------------
''' 24 - 03 - 09  웹 크롤링 '''
'''
웹 크롤링(Web Crawring) : 특정 사이트에서 원하는 정보를 긁어오는 행위
'''
'''
HTML : 웹 페이지의 표시를 위해서 개발된 지배적인 마크업 언어

- HTML 기본 구조

<!DOCTYPE html>
<html>
<head>
    <title> 페이지의 제목 </title>
</head>
<body>
    <h1> 제목 </h1>
    <p> 들어갈 문장 </p>
</body>
</html>

 -> tag : 열린태그 <> 와 닫힌태그 </> 사이의 콘텐츠를 위치하여 문서의 구조로 표현한 것
    1) h1 태그 : 문서의 제목 h1 ~ h6
    2) p 태그 : 단락을 지정할 수 있는 태그
    3) img 태그 : 이미지를 표시할 수 있는 태그, 닫힌 태그 필요가 x
    4) input, button 태그 : 사용자의 입력이 필요할 때 input,
                            사용자가 클릭할 수 있는 버튼
    5) ul, ol, il 태그 : 리스트를 표현할 때 사용하는 태그
    6) div, span 태그 : 사용 시 요소가 즉각적으로 나타나는 것과는 별개로 화면 내에서 아무런 역활은 없지만,
                        문서의 영역을 분리하고 인라인 요소를 감쌀 때 사용하는 태그
'''
import requests

### 당근 마켓 인기 매물 긁어오기
url = 'https://www.daangn.com/hot_articles'
web = requests.get(url)
# print(web.text)

'''
BeautifulSoup 라이브러리 : HTML 문서에서 원하는 부분만 추출할 때 사용하는 패키지
'''

from bs4 import BeautifulSoup

soup = BeautifulSoup(web.content, 'html.parser')           # 웹에 모든 정보를 다 들고옴
'''
파싱 : 컴퓨터에서 번역기가 원시 부호를 기계어로 번역하는 과정의 한 단계
'''

## ul 태그의 하위 항목을 모두 뽑아오고 싶을 때
import time

# for child in soup.ul.children:
    # time.sleep(3)
    # print(child)

## 1. 정규식 활용하는 방법 - <ol>이든 <ul>이든 다 포함된 리스트를 긁어오고 싶을 때
import re
# for f in soup.find_all(re.compile('[ou]')):
#     print(f)

## 2. 리스트 활용 - 원하는 태그를 직접 지정해서 뽑는 경우 (h1, p만 보고싶다.)
# for f in soup.find_all(['h1', 'p']):
#     print(f)

## 3. HTML 속성 활용 - 속성을 지정해서 뽑고 싶을 때
a = soup.find_all(attrs= {'class' : 'card-title'})
p = soup.find_all(attrs = {'class' : 'card-price '})

# print(a)
#
# for i in a:
#     print('매물명 :',i)

## 4. 텍스트만 가져 오고 싶을 때
'''
range(처음, 끝, 단위) : 범위 생성 함수
range 함수의 끝 부분은 -1로 범위를 잡는다.
'''
# for a in range(0, 100, 2):
#     print(a)

# print(soup.select('.card-title'))       # . <-속성이라는 뜻

# for x in range(0, 10):      #0부터 9까지 자동 생성
#     # print(soup.select('.card-title'))
#     print('현재 x값 :', x)
#     print(soup.select('.card-title')[x].get_text())

# 상관분석, 웹 크롤링, 감성분석(텍스터마이닝 + 머신러닝)