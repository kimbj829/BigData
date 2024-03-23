### import
import datetime
from bs4 import BeautifulSoup
import urllib.request
import requests
from urllib import parse

## 현재 시간을 출력하고 본인 스타일에 맞게 출력문 수정
now = datetime.datetime.now()       # 현재 시간
# print(now)

nowDate = now.strftime('%y년 %m월 %d일 %H시 %M분 입니다.')
# print(nowDate)
print('-'*100)
print('\t\t\t\t\t\t\t\t ※ Python Web Crawling Project ※')
print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t ID : KBJ')
print('-'*100)
print('반갑습니다,', '현재 시간은', nowDate, '\n')     # \n : 줄 바꿈
print("\t Let Me Summarise Today's Info !\n")

### 서울 날씨
print('#오늘의 #날씨 #요약 \n')

import binascii
web = 'https://search.naver.com/search.naver?where=nexearch&sm=top_clk.splogo&fbm=0&ie=utf8&query='
region = input("찾으시는 지역을 입력하세요 : ")
'''
web_region = web + region + "+날씨"
webpage = requests.get(web_region)

soup = BeautifulSoup(webpage.text, 'html.parser')
temps = soup.find('strong', '')     # 온도
print(temps.get_text())
cast = soup.find('p', 'summary')    # 날씨
# print(cast)
print('-->', region ,'날씨 :', temps.get_text(), cast.get_text())
'''
web_region = web + urllib.parse.quote(region + "날씨")
webpage = urllib.request.urlopen(web_region)
soup = BeautifulSoup(webpage, 'html.parser')
temps = soup.find('strong', '')     # 온도
print(temps.get_text())
cast = soup.find('p', 'summary')    # 날씨
# print(cast)
print('-->', region ,'날씨 :', temps.get_text(), cast.get_text())