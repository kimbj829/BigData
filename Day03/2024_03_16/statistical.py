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
