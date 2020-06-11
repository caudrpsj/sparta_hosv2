from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup
import Bio
from Bio import Entrez
Entrez.email ="caudrpsj@gmail.com"
from Bio import Medline

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
  return render_template('index.html')

@app.route('/pubmed', methods=['GET'])
def listing():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    # 2. articles라는 키 값으로 영화정보 내려주기
  articles = list(db.pubmed.find({},{'_id':0}))
  return jsonify({'result': 'success', 'articles': articles, 'msg': '성공적'})

## API 역할을 하는 부분
@app.route('/pubmed', methods=['POST'])
def saving():
		# 1. 클라이언트로부터 검색어를 받기
		# 2. 앱스트랙과 doi, pmid, 초록 정보를 긁어오기
		# 3. mongoDB에 데이터 넣기
  search_receive = request.form['search_give']
  number_receive = request.form['number_give']
  db.pubmed.remove()
   #  article = {
   #       'title': search_receive,
   #       'abstract': number_receive
   #       }
   #  db.pubmed.insert_one(article)
  choose_receive = request.form['choose_give']
  print(choose_receive)
  if choose_receive == '2' :
    print('match 함수로')
    idlist = saving_match(search_receive,number_receive)
  elif choose_receive == '3' :
    print('날짜 함수로')
    idlist = saving_date(search_receive,number_receive)
  else :  
    handle = Entrez.esearch(db="pubmed", term=search_receive, retmax=number_receive, sort='relevance')
    record = Entrez.read(handle)
    idlist = record["IdList"]

  handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline")
  records = Medline.parse(handle)
  records = list(records)
  print (search_receive)
  num = 0
  for record in records:
    num  += 1
    title = record.get("TI", "?")
    abstract = record.get("AB", "No abstract available")
    pmid = record.get("PMID", "")
    doi = record.get("LID", "")
    journal= record.get("SO", "")
    pmc= record.get("PMC", "")
    article = {
      'search' : search_receive,
      'title': title ,
      'abstract': abstract,
      'PMID' : pmid,
      'DOI' : doi,
      'journal': journal,
      'PMC':pmc,
      'Num' : num

       }
    db.pubmed.insert_one(article)  
  return jsonify({'result': 'success', 'msg': '로딩 완료.'})


# 검색함수 더만들기 
def saving_match(search_receive,number_receive):
  print('name')
  headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
  request_url = 'https://pubmed.ncbi.nlm.nih.gov/?term='+search_receive+'&size=50'
  data = requests.get(request_url,headers=headers)
  # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
  soup = BeautifulSoup(data.text, 'html.parser')
  #//*[@id="search-results"]/section/div[1]/div/article[1]/div[2]/div[1]/div[1]/span[3]/text()
  # select를 이용해서, tr들을 불러오기
  #/html/body/main/div[9]/div[2]/section/div[1]/div/article[1]/div[2]/div[1]/div[1]/span[5]/span
  pubmeds = soup.select('#search-results > section > div.search-results-chunks > div > article.labs-full-docsum')
  # pubmeds = soup.select('#search-results > section > div.search-results-chunks > div > article.labs-full-docsum > div.docsum-content > div.labs-docsum-citation full-citation')
  # movies (tr들) 의 반복문을 돌리기
  num = 0
  idlist = list()
  number_receive = int(number_receive)  
  for pubmeds_in in pubmeds:
      num  += 1
      # movie 안에 a 가 있으면,
      a_tag = pubmeds_in.select_one('div.docsum-wrap > div.docsum-content > div >span:nth-child(5)')
      b_tag = a_tag.text.split(': ')[1]
      # print (b_tag)
      # doi_split = b_tag.split('doi:')[1].split('. ')[0]
      print(number_receive)
      print(num)
      idlist.append(b_tag)
      # if a_tag is not None:
      #     print(a_tag.text)
      if num == number_receive :
        break
      
  return idlist

def saving_date(search_receive,number_receive):
  handle = Entrez.esearch(db="pubmed", term=search_receive, retmax=number_receive, sort='pub date')
  print('pubdate')
  record = Entrez.read(handle)
  idlist = record["IdList"]
  return idlist

# 다운로드 이치
@app.route('/download', methods=['POST'])
def downloadeach():
		# 1. 클라이언트로부터 검색어를 받기
		# 2. 앱스트랙과 doi, pmid, 초록 정보를 긁어오기
		# 3. mongoDB에 데이터 넣기
    
  pmid_receive = request.form['pmid_give']
  downloadtarget = db.pubmed.find_one({'PMID':pmid_receive})

  try : 
    downloadeach_doi(downloadtarget)
    msg = downloadeach_doi(downloadtarget)
  except:   
    print('pmc 확인하러 간다') 
    msg = downloadeach_pmc_yes(downloadtarget) 

  return jsonify({'result': 'success', 'msg': msg})


def downloadeach_doi(downloadtarget):
  downloadtarget_doi = downloadtarget['DOI']
  
  if downloadtarget_doi.count('[') >1 :
    url = downloadtarget['DOI'].split('[doi')[0].split('] ')[1]
  else :
    url = downloadtarget['DOI'].split('[doi')[0]
  #잠시 한번더확인
  if downloadtarget_doi == '' : 
    print('doi에는 안들어있음')
    downloadtarget_doi_confirm = downloadtarget['journal']
    downloadtarget_doi = downloadtarget_doi_confirm.split('doi: ')[1].split('. ')[0]
    print ('새로구한 doi')
    print(downloadtarget_doi)
    url = downloadtarget_doi
  # 확인
  url_scihub = 'https://sci-hub.tw/' + url
  print(url_scihub)
  headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
  data = requests.get(url_scihub,headers=headers)
  soup = BeautifulSoup(data.text, 'html.parser')
  # print(soup)
  url_download = soup.select('#article>iframe')[0]["src"]
  if 'https:' in url_download :
    url_download = url_download
  else:
    url_download = 'https:' + url_download
  print(url_download)
  path_name = downloadtarget['search']
  file_name = downloadtarget['PMID']
  outpath = "C:/test/"+ path_name +"/" # 여기는 검색어로 
  outfile = file_name+".pdf"  # 여기는 서지 정보 및 pmid
  print(path_name)
  print(file_name)
  print(outfile)
  print(outpath)
  import os
  if not os.path.isdir(outpath):
    os.mkdir(outpath)
  import urllib.request
  open("sichub", mode="wb")
  urllib.request.urlretrieve(url_download,outpath+outfile)
  print('저장되었습니다')
  return '다운로드 성공'
  
  # pmc_receive = downloadtarget['PMC']
  # print(pmc_receive)

  # if 'PMC' in pmc_receive :
  #   downloadeach_pmc(downloadtarget)
  #   print('pmc에 뭐가 있음')
  # else : 
  #   downloadeach_doi(downloadtarget)
  #   print('pmc에 뭐가 없음')
  

# def downloadeach_doi(downloadtarget) :
  


def downloadeach_pmc_yes(downloadtarget) :
  pmc_receive = downloadtarget['PMC']
  if 'PMC' in pmc_receive :
    downloadeach_pmc(downloadtarget)
    return downloadeach_pmc(downloadtarget)

  else : 
    print('pmc에 뭐가 없음')
    msg = '다운로드 실패'
    return msg

def downloadeach_pmc(downloadtarget) :
  pmc_receive = downloadtarget['PMC']
  url_pmc = 'https://www.ncbi.nlm.nih.gov/pmc/articles/' + pmc_receive
  print(url_pmc)
  # headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
  # data = requests.get(url_pmc,headers=headers)
  # soup = BeautifulSoup(data.text, 'html.parser')
  # url_download2 = soup.select_one('#rightcolumn>div:nth-child(2)>div>ul>li:nth-child(4)>a')
  # print(url_download2)
  # url_download = url_download2['href']
  # url_download = 'https://www.ncbi.nlm.nih.gov/' + url_download
  # print(url_download)
  # path_name = downloadtarget['search']
  # file_name = downloadtarget['PMID']
  # outpath = "C:/test/"+ path_name +"/" # 여기는 검색어로 
  # outfile = file_name+".pdf"  # 여기는 서지 정보 및 pmid
  # print(path_name)
  # print(file_name)
  # import urllib.request
  # open("sichub", mode="wb")
  # urllib.request.urlretrieve(url_download,outpath+outfile)
  # print('저장되었습니다')
  return url_pmc

if __name__ == '__main__':
    app.run('localhost',port=5000,debug=True)

  