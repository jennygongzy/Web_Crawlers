#By Jenny Gong
# Crawl Google Apps information in Games subcategory 

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import requests


#change the output file name for each subcategory
f=open('Andriodcrawl_0305.txt','w') 

#input a subcategory page 
url = 'https://play.google.com/store/apps/category/GAME_WORD'

def description(soup):
    #this function parse the description text, and put them into one string
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

def parse_app(psoup):
    name = psoup.find('div',class_='id-app-title').get_text()
    try:
        review_score = psoup.find('div',class_='score').get_text()
        review_num = psoup.find('span',class_='reviews-num').get_text()
    except:
        review_score='NA'
        review_num='NA'
        
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

    writestr = (name+'\t'+str(wholeurl)+'\t'+review_title+'\t'+review_content+'\t'+
                content_rating+'\t'+content_rating_reason+'\t'+icon_url+'\t'+review_score+'\t'
                +review_num+'\t'+current_version+'\t'+seller+'\t'+des+'\n')

    return writestr

#print header 
headerstr = str('name\tapppurl\treview_title\treview_content\t'+
                'content_rating\tcontent_rating_reason+\ticon_url\trating_score\t'+
                'rating_num\tcurrent_version\tDeveloper\tdescription\n')
f.write(headerstr)

#read source page
driver = webdriver.Chrome('/Users/gongzeyang/Downloads/chromedriver')
driver.get(url)
loginpage=driver.find_element_by_id('gb_70').get_attribute('href')
driver.get(loginpage)
gid=driver.find_element_by_id('Email')
gid.send_keys('zeyanggong@gmail.com')
nextbutton=driver.find_element_by_id('next')
nextbutton.click()
time.sleep(3)
passwd=driver.find_element_by_id('Passwd')
passwd.send_keys('yinhuodefu')
signin=driver.find_element_by_id("signIn")
signin.click()
time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#time.sleep(3)
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#time.sleep(3)

wholepage = driver.page_source
soup = BeautifulSoup(wholepage,'html.parser')

seemoreurls=[tag['href'] for tag in soup.find_all('a',class_='see-more')]

#go inside seemore pages 
for seemoreurl in seemoreurls:
    purl='https://play.google.com'+seemoreurl

    driver.get(purl)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
#    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#    time.sleep(2)
#    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#    time.sleep(2)

    seemorepage=driver.page_source
    seemoresoup = BeautifulSoup(seemorepage,'html.parser')

    appurls=[tag['href'] for tag in seemoresoup.find_all('a',class_='title') if tag.get('href').startswith('/store/apps/details')]
    
    #go inside each app page
    for appurl in appurls:
        wholeurl='https://play.google.com'+appurl
        req=requests.get(wholeurl)
        psoup=BeautifulSoup(req.text,'html.parser')
    
        writestr = parse_app(psoup)
        #print writestr
        f.write(writestr.encode(errors='ignore'))
    



    
f.close()
