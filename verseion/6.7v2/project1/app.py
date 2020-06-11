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

  handle = Entrez.esearch(db="pubmed", term=search_receive, retmax=number_receive)
  record = Entrez.read(handle)
  idlist = record["IdList"]
  handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline")
  records = Medline.parse(handle)
  records = list(records)
  print (search_receive)
  for record in records:
    title = record.get("TI", "?")
    print(title)
    abstract = record.get("AB", "No abstract available")
    pmid = record.get("PMID", "")
    doi = record.get("LID", "")
    print(pmid)
    article = {
        'title': title ,
        'abstract': abstract,
        'PMID' : pmid,
        'DOI' : doi
       }
    db.pubmed.insert_one(article) 
       
  return jsonify({'result': 'success', 'msg': '메모가 성공적으로 작성되었습니다.'})

if __name__ == '__main__':
   app.run('localhost',port=5000,debug=True)