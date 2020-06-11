import requests
from bs4 import BeautifulSoup

# URL을 읽어서 HTML를 받아오고,
# url = '10.1016/S0140-6736(14)61909-7'
# url_scihub = 'https://sci-hub.tw/' + url
# print(url_scihub)
# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(url_scihub,headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup = BeautifulSoup(data.text, 'html.parser')
# url_download = soup.select('#article>iframe')[0]["src"]
# print(url_download)

# 다운로드 연결하기

# outpath = "C:/test/"   # 여기는 검색어로 
# outfile = "sichub"+".pdf"  # 여기는 서지 정보 및 pmid
# open("sichub", mode="wb")
# urllib.request.urlretrieve(url,outpath+outfile)
# print('저장되었습니다')
pmc_receive ='PMC7268579'
url_pmc = 'https://www.ncbi.nlm.nih.gov/pmc/articles/' + pmc_receive
print(url_pmc)
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url_pmc,headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
url_download = soup.select('#rightcolumn>div:nth-child(2)>div>ul>li:nth-child(4)>a')[0]['href']
print(url_download)