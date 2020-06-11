# https://sci-hub.tw/10.1016/S0140-6736(14)61909-7
import urllib.request
from urllib.request import urlopen
from urllib import request

url = '10.1016/S0140-6736(14)61909-7'
url_scihub = 'https://sci-hub.tw/' + url
url_scihub = "http://sci-hub.tw/downloads-ii/2019-12-31/30/llamas-velasco2019.pdf#view=FitH"

print(url_scihub)

# 이제 내가 해야할것은 받은것을쭉 목록을 만들어서 이름을 붙여서 주는거지 
# savename = 'scihub'
# -------------------------
# mem= urllib.request.urlopen(url).read()

outpath = "C:/test/"
outfile = "sichub"+".pdf"
open("sichub", mode="wb")
urllib.request.urlretrieve(url_scihub,outpath+outfile)
print('저장되었습니다')
# --------------------------------

# with open(savename, mode="wb") as f:
#     f.write(mem)
#     print("저장되었습니다")

