from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

driver = webdriver.Chrome(ChromeDriverManager().install())

# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Chrome('/path/to/chromedriver') 
# driver = webdriver.Chrome('C:\Users\emr4\Desktop\chromedriver_win32')
driver.get('https://sci-hub.tw/10.1016/S0140-6736(14)61909-7')
# $ pip show webdriver-manager
# $ pip install webdriver-manager
# driver.find_element_by_name('id').send_keys('naver_id')
# 로그인 버튼을 눌러주자.
# driver.find_element_by_xpath('/html/body/viewer-pdf-toolbar//div[1]/div[1]/div[2]/cr-icon-button[2]').click()
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
url = soup.select('#article>iframe')[0]["src"]
driver.get(url)



# /html/body/viewer-pdf-toolbar//div[1]/div[1]/div[2]/cr-icon-button[2]