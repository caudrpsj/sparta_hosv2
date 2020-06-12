from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  

articles = list(db.pubmed.find({},{'_id':0}))
abstractcloud = list()
tag_2= list()
tag_3 = list()
num =0
for article in articles:
    num += 1
    tag = article['abstract']
    tag_2 = tag.split('. ')
    print(tag_2[-1])
    tag_3 = tag_2[-1]
    if tag_3 =='No abstract available':
        tag_3 = ''
    abstractcloud.append(tag_3)
abstractcloud_word = ''.join(abstractcloud)
# print(abstractcloud_word)

stopwords = set(STOPWORDS) 
stopwords.update(['onychomatricoma','nail','the','tumor','palte','we', 'of','plate','diagnosis','case','the nail','tumor','case','of onychoamtricoma','No abstract available','NO','abstract','report','rare','clinical','review','OM','Conclusion','lichen planus'])
print(stopwords)
wc = WordCloud(stopwords=stopwords, width=1000, height=600, background_color="white", random_state=0, font_path=r'c:\Windows\Fonts\malgun.ttf')
plt.imshow(wc.generate(abstractcloud_word))
plt.axis("off")
plt.show()

# #  pip install wordcloud-1.7.0-cp38-cp38-win32.whl
# # https://www.lfd.uci.edu/~gohlke/pythonlibs/#wordcloud

# # OT가 키워드임 



