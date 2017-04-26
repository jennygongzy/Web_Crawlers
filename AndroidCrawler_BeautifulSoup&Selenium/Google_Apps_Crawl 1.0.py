#By Jenny Gong
# Crawl Android Apps information in Top Free Games category 
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver 
import time

f=open('Google_Apps_crawl.txt','w')

url = 'https://play.google.com/store/apps/category/GAME/collection/topselling_free?hl=en'

driver = webdriver.Chrome('/Users/gongzeyang/Downloads/chromedriver')
driver.get(url)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

wholepage = driver.page_source
soup = BeautifulSoup(wholepage,'html.parser')

appurls = [tag['href'] for tag in soup.find_all('a',class_='title') if tag.get('href').startswith('/store/apps/details?')]

def description(soup):
    deslist=[]
    tag=soup.find('div',jsname='C4s9Ed')
    deslist.append(tag.get_text())
    for item in tag.find_all('p'):
        try: 
            for i in item.contents: 
                deslist.append(item.contents[i].get_text())
        except: 
            deslist.append(item.get_text())
    for item in deslist:
        item.replace('\t',' ')
        item.replace('\n',' ')
    desstr=' '.join(deslist) 
    return desstr

for appurl in appurls:
    purl='https://play.google.com'+appurl
    preq=requests.get(purl)
    psoup=BeautifulSoup(preq.text,'html.parser')

    name = psoup.find('div',class_='id-app-title').get_text()
    review = psoup.find('div',class_='score').get_text()
    review_num = psoup.find('span',class_='reviews-num').get_text()
    date_published = psoup.find('div',class_='content',itemprop='datePublished').get_text()

    try:
        current_version = psoup.find('div',itemprop='softwareVersion').get_text()
    except:
        current_version = 'NA'
    seller = psoup.find(string=re.compile('Offered By')).find_previous('div').find_next_sibling('div').get_text()
    des = description(psoup)

    writestr = (name+'\t'+str(purl)+'\t'+review+'\t'+review_num+'\t'+date_published+'\t'+current_version
                +'\t'+seller+'\t'+des+'\n')
    
    #print writestr
    f.write(writestr.encode('ascii',errors='ignore'))
    
f.close()


    



