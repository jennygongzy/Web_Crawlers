#-*- coding:utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from faker import Factory  
f = Factory.create()    
from Android.items import AndroidItem
from scrapy.utils.response import open_in_browser


class AndroidSpider(scrapy.Spider):
	name = 'AndroidSpider2'
	allow_domains = ['accounts.google.com','play.google.com']
	
	start_urls = [
	'https://play.google.com/store/apps/category/GAME_ACTION',
	'https://play.google.com/store/apps/category/GAME_ADVENTRUE',
	'https://play.google.com/store/apps/category/GAME_ARCADE',
	'https://play.google.com/store/apps/category/GAME_BOARD',
	'https://play.google.com/store/apps/category/GAME_CARD',
	'https://play.google.com/store/apps/category/GAME_CASINO',
	'https://play.google.com/store/apps/category/GAME_CASUAL',
	'https://play.google.com/store/apps/category/GAME_EDUCATIONAL',
	'https://play.google.com/store/apps/category/GAME_MUSIC',
	'https://play.google.com/store/apps/category/GAME_PUZZLE',
	'https://play.google.com/store/apps/category/GAME_RACING',
	'https://play.google.com/store/apps/category/GAME_ROLE_PLAYING',
	'https://play.google.com/store/apps/category/GAME_SIMULATION',
	'https://play.google.com/store/apps/category/GAME_SPORTS',
	'https://play.google.com/store/apps/category/GAME_STRATEGY',
	'https://play.google.com/store/apps/category/GAME_TRIVIA',
	'https://play.google.com/store/apps/category/GAME_WORD'
	]

	sub_category_names = ['Action','Adventrue','Arcade','Board','Card','Casino','Casual',
						'Educational','Music','Puzzle','Racing','Role Playing','Simulation',
						'Sports','Trivia','Word']

	headers = {'User-Agent': f.user_agent()}
	language = ['en','en_US']

	def parse(self,response):

		#may need to scroll 1 time

		#open_in_browser(response)

		app_urls = response.xpath('//a[@class = "title"]/@href').extract()
		seemore_urls = response.xpath('//a[contains(@class, "see-more")]/@href').extract()

		for app_url in app_urls:
			yield scrapy.Request(url = response.urljoin(app_url),
							#	 meta={'cookiejar': response.meta['cookiejar']}, 
								 headers=self.headers,                         
								 callback=self.parse_app)

		for seemore_url in seemore_urls:
			yield scrapy.Request(url = response.urljoin(seemore_url),
							#	 meta={'cookiejar': response.meta['cookiejar']}, 
								 headers=self.headers,                         
								 callback=self.parse_seemore_page)


	def parse_seemore_page(self,response):
		#may need to scroll 2~3 times

		app_urls = response.xpath('//a[@class = "title"]/@href').extract()

		for app_url in app_urls:

		   yield scrapy.Request(url = response.urljoin(app_url),
							#	meta={'cookiejar': response.meta['cookiejar']}, 
								headers=self.headers,                         
								callback=self.parse_app)


	def parse_app(self,response):


		#get 'similar app' seemore page

		seemore_urls = response.xpath('//a[contains(@class, "see-more")]/@href').extract()
		for seemore_url in seemore_urls:
			yield scrapy.Request(url = response.urljoin(seemore_url),
								# meta={'cookiejar': response.meta['cookiejar']}, 
								 headers=self.headers,                         
								 callback=self.parse_seemore_page)


		app_subcategory = response.xpath('//span[@itemprop="genre"]/text()').extract_first()
		app_language = response.xpath('/html[@lang]/@lang').extract_first()
		if  app_subcategory in self.sub_category_names and app_language in self.language:

			app = AndroidItem()
			app['name'] = response.xpath('//div[@class="id-app-title"]/text()').extract_first().encode(errors='ignore')
			app['sub_category'] = response.xpath('//span[@itemprop="genre"]/text()').extract_first()
			app['app_url'] = response.url
			app['icon_url'] = 'http:'+response.xpath('//img[@class="cover-image"]/@src').extract_first()

			app['maturity_rating'] = response.xpath('//div[@itemprop="contentRating"]/text()').extract_first()
			app['maturity_rating_reason'] = response.xpath('//div[@itemprop="contentRating"]/following-sibling::div/text()').extract_first()
		

			app['review_score'] = response.xpath('//meta[@itemprop="ratingValue"]/@content').extract_first()
			app['review_num'] = response.xpath('//meta[@itemprop="ratingCount"]/@content').extract_first()
			app['datePublished'] = response.xpath('//div[@itemprop="datePublished"]/text()').extract_first()
			app['download_num'] = response.xpath('//div[@itemprop="numDownloads"]/text()').extract_first()
			app['price'] = response.xpath('//div[text()="In-app Products"]/following-sibling::div/text()').extract_first()
			app['version'] = response.xpath('//div[@itemprop="softwareVersion"]/text()').extract_first()
			app['developer'] = response.xpath('//div[contains(text(),"Offered By")]/following-sibling::div/text()').extract_first()
			try:
				app['developer_address'] = response.xpath('//div[@class="content physical-address"]/text()').extract_first().replace('\n',' ')
			except:
				pass

			des_text_list = response.xpath('//div[@jsname="C4s9Ed"]/text()').extract()
			des_text = ' '.join([line.strip() for line in des_text_list])
			des_text = des_text.replace('_','').replace('-','').replace('*','').encode(errors='ignore')
			app['description'] = des_text

			yield app















