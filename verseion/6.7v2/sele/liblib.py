# https://sci-hub.tw/10.1016/S0140-6736(14)61909-7
import urllib.request
# from urllib import request
url = 'https://twin.sci-hub.tw/7138/f8851f2a67360ee69c8bc3603f24b86d/boehncke2015.pdf#view=FitH'
# 이제 내가 해야할것은 받은것을쭉 목록을 만들어서 이름을 붙여서 주는거지 
# savename = 'scihub'
# -------------------------
# mem= urllib.request.urlopen(url).read()

outpath = "C:/test/"
outfile = "sichub"+".pdf"
open("sichub", mode="wb")
urllib.request.urlretrieve(url,outpath+outfile)
print('저장되었습니다')
# --------------------------------

# with open(savename, mode="wb") as f:
#     f.write(mem)
#     print("저장되었습니다")

