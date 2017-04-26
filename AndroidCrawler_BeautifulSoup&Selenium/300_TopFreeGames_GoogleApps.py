#By Jenny Gong
# Crawl Google Apps information in Top Free Games category, 300 games in total
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver 
import time

f=open('300_FreeGames_GoogleApps.txt','w')

headerstr = str('name\tapppurl\treview_title\treview_content\t'+
                'content_rating\tcontent_rating_reason+\ticon_url\trating_score\t'+
                'rating_num\tcurrent_version\tDeveloper\tdescription\n')
f.write(headerstr)

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
    review_score = psoup.find('div',class_='score').get_text()
    review_num = psoup.find('span',class_='reviews-num').get_text()
    date_published = psoup.find('div',class_='content',itemprop='datePublished').get_text()

    try:
        current_version = psoup.find('div',itemprop='softwareVersion').get_text()
    except:
        current_version = 'NA'
    seller = psoup.find(string=re.compile('Offered By')).find_previous('div').find_next_sibling('div').get_text()
    des = description(psoup)
    
    review_title_list=[tag.find(class_='review-title').get_text() for tag in psoup.find_all('div',class_='review-text')]
    review_title = ';'.join(review_title_list)
    review_content_list=[tag.get_text() for tag in psoup.find_all('div',class_='review-text')]
    review_content = ';'.join(review_content_list)

    content_rating = psoup.find(class_='content',itemprop='contentRating').get_text()
    if psoup.find(class_='content',itemprop='contentRating').next_sibling.next_sibling.get_text()=='Learn more':
        content_rating_reason ='NA'
    else:
        content_rating_reason = psoup.find(class_='content',itemprop='contentRating').next_sibling.next_sibling.get_text()
       
    icon_url = 'http:'+str(psoup.find('img',class_='cover-image').get('src'))

    writestr = (name+'\t'+str(purl)+'\t'+review_title+'\t'+review_content+'\t'+
                content_rating+'\t'+content_rating_reason+'\t'+icon_url+'\t'+review_score+'\t'
                +review_num+'\t'+current_version+'\t'+seller+'\t'+des+'\n')
    
    #print writestr
    f.write(writestr.encode('ascii',errors='ignore'))
    
f.close()
