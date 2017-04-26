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
	name = 'AndroidSpider'
	allow_domains = ['accounts.google.com','play.google.com']
	
	subcategory_urls = [
	'https://play.google.com/store/apps/category/GAME_ACTION'
	'https://play.google.com/store/apps/category/GAME_ADVENTRUE'
	'https://play.google.com/store/apps/category/GAME_ARCADE'
	'https://play.google.com/store/apps/category/GAME_BOARD'
	'https://play.google.com/store/apps/category/GAME_CARD'
	'https://play.google.com/store/apps/category/GAME_CASINO'
	'https://play.google.com/store/apps/category/GAME_CASUAL'
	'https://play.google.com/store/apps/category/GAME_EDUCATIONAL'
	'https://play.google.com/store/apps/category/GAME_MUSIC'
	'https://play.google.com/store/apps/category/GAME_PUZZLE'
	'https://play.google.com/store/apps/category/GAME_RACING'
	'https://play.google.com/store/apps/category/GAME_ROLE_PLAYING'
	'https://play.google.com/store/apps/category/GAME_SIMULATION'
	'https://play.google.com/store/apps/category/GAME_SPORTS'
	'https://play.google.com/store/apps/category/GAME_STRATEGY'
	'https://play.google.com/store/apps/category/GAME_TRIVIA'
	'https://play.google.com/store/apps/category/GAME_WORD'
	]

	headers = {'Host': 'accounts.google.com','User-Agent': f.user_agent()}

	

	start_urls = ['https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fplay.google.com%2Fstore%3Fhl%3Den&followup=https%3A%2F%2Fplay.google.com%2Fstore%3Fhl%3Den&service=googleplay&sacu=1&passive=1209600&ignoreShadow=0&acui=0#Email=zeyanggong%40gmail.com']
	
	def parse(self,response):
		formdata = {
		'Email': 'zeyanggong@gmail.com',
		'Passwd': 'yinhuodefu'
		}

		return scrapy.FormRequest.from_response(response,
												formdata=formdata,
												headers=self.headers,
												meta={'cookiejar': 1},
												callback=self.after_login)

	def after_login(self, response):
	
		self.headers['Host'] = "play.google.com"
		
	#    for sub_url in subcategory_urls:
			
	#        yield scrapy.Request(url=sub_url,
	#                              meta={'cookiejar': response.meta['cookiejar']}, #此时cookie信息里已经有登录进去了
	#                              headers=self.headers,                           #带着header和cookie，网站就不会让我们继续登陆了
	#                              callback=self.parse_subcategory_page)#把当前页面的内容parse一遍
		
		return [scrapy.Request(url='https://play.google.com/store/apps/category/GAME_ACTION',
							   meta={'cookiejar': response.meta['cookiejar']}, 
							   headers=self.headers,                         
							   callback=self.parse_subcategory_page)]

	def parse_subcategory_page(self,response):

		#may need to scroll 1 time

		open_in_browser(response)
'''
		app_urls = 
		seemore_urls = 

		for app_url in app_urls:
			yield scrapy.Request(url = app_url,
								 meta={'cookiejar': response.meta['cookiejar']}, 
								 headers=self.headers,                         
								 callback=self.parse_app)

		for seemore_url in seemore_urls:
			yield scrapy.Request(url = seemore_url,
								 meta={'cookiejar': response.meta['cookiejar']}, 
								 headers=self.headers,                         
								 callback=self.parse_seemore_page)

	def parse_seemore_page(self,response):
		#may need to scroll 2~3 times

		app_urls = 

		for app_url in app_urls:

		   yield scrapy.Request(url = app_url,
								meta={'cookiejar': response.meta['cookiejar']}, 
								headers=self.headers,                         
								callback=self.parse_app)

		
	def parse_app(self,response):

		#get 'similar app' seemore page

		seemore_urls = 

		for seemore_url in seemore_urls:
			yield scrapy.Request(url = seemore_url,
								 meta={'cookiejar': response.meta['cookiejar']}, 
								 headers=self.headers,                         
								 callback=self.parse_seemore_page)

		#app = AndroidItem()
		pass


'''










