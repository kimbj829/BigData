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


