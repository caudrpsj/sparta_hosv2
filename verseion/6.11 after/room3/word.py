from wordcloud import WordCloud
import matplotlib.pyplot as plt
# from nltk.corpus import stopwords
import nltk
# nltk.download('stopwords')


from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  

articles = list(db.pubmed.find({},{'_id':0}))
abstractcloud = list()
for article in articles:
    tag = article['abstract']
    abstractcloud.append(tag)
abstractcloud_word = ''.join(abstractcloud)
# print(abstractcloud_word)

en_stop_words = set(nltk.corpus.stopwords.words('english'))
print(len(en_stop_words))
en_stop_words.update(['onychomatricoma','nail','the','tumor','palte','we', 'of','plate','diagnosis','case','the nail','tumor','case','of onychoamtricoma'])
en_stop_words.update(['lesion','Lichen planus','patients with','No abstract','Lichen','planus','We','RESULT'])
en_stop_words.update(['LP','LP ','condition','RESULT','diagnosis','LP','We','lichen planus','disease','No abstract','No','abstract','It','clinical','pateint','oral','oral lichen','CONCLUSION','RESULT','patient','METHOD','OBJECTIVE','patient with','group','conclusion','patient with','may', 'of','skin','of lichen','case','the nail','tumor','case','of onychoamtricoma','treatment','patient with','lichen','planus'])
en_stop_words.update(['reported','involvement','feature','The','We','disease','No abstract','No','abstract','It','diagnosis','clinical','pateint','CONCLUSION','RESULT','patient','METHOD','OBJECTIVE','patient with','group','conclusion','patient with','may', 'of','skin','case','treatment','patient with','lichen','planus'])
en_stop_words.add('RESULT')
print(len(en_stop_words))
# print(en_stop_words)

# Getting rid of the stopwords
clean_text = [word for word in abstractcloud_word.split() if word not in en_stop_words]

# Converting the list to string
text = ' '.join([str(elem) for elem in clean_text])

wc = WordCloud(width=1000, height=600, background_color="black", random_state=0, font_path=r'c:\Windows\Fonts\malgun.ttf')
plt.imshow(wc.generate(text))
plt.axis("off")
plt.show()

#  pip install wordcloud-1.7.0-cp38-cp38-win32.whl
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#wordcloud

# OT가 키워드임 