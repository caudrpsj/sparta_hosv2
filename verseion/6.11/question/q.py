import requests
from bs4 import BeautifulSoup

pmc_receive = 'PMC7268579'
url_pmc = 'https://www.ncbi.nlm.nih.gov/pmc/articles/' + pmc_receive
print(url_pmc)
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url_pmc,headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
url_download2 = soup.select_one('#rightcolumn>div:nth-child(2)>div>ul>li:nth-child(4)>a')
print(url_download2)
url_download = url_download2['href']
url_download = 'https://www.ncbi.nlm.nih.gov/' + url_download
print(url_download)
path_name = 'test'
file_name = '제목'
outpath = "C:/test/"+ path_name +"/" # 여기는 검색어로 
outfile = file_name+".pdf"  # 여기는 서지 정보 및 pmid
print(path_name)
print(file_name)
import urllib.request
open("sichub", mode="wb")
urllib.request.urlretrieve(url_download,outpath+outfile)
print('저장되었습니다')
