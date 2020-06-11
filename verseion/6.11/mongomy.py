import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://pubmed.ncbi.nlm.nih.gov/?term=onychomatricoma&size=50',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')
#//*[@id="search-results"]/section/div[1]/div/article[1]/div[2]/div[1]/div[1]/span[3]/text()
# select를 이용해서, tr들을 불러오기
pubmeds = soup.select('#search-results > section > div.search-results-chunks > div > article.labs-full-docsum')
# pubmeds = soup.select('#search-results > section > div.search-results-chunks > div > article.labs-full-docsum > div.docsum-content > div.labs-docsum-citation full-citation')
# movies (tr들) 의 반복문을 돌리기
num = 0
for pubmeds_in in pubmeds:
    num  += 1
    # movie 안에 a 가 있으면,
    a_tag = pubmeds_in.select_one('div.docsum-wrap > div.docsum-content > div >span:nth-child(3)')
    b_tag = a_tag.text
    # print (b_tag)
    doi_split = b_tag.split('doi:')[1].split('. ')[0]
    print (num, doi_split)
    # if a_tag is not None:
    #     print(a_tag.text)