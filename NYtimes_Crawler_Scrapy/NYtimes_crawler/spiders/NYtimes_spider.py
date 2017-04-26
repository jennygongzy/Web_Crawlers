# -*- coding: utf-8 -*-
import scrapy
from NYtimes_crawler.items import NytimesCrawlerItem

class NYtimesSpider(scrapy.Spider):

	name = 'NYtimesSpider'

	allowed_domains = ['www.nytimes.com']

	start_urls = ['https://www.nytimes.com/topic/destination/china']

	def parse(self, response):
		for url in response.xpath('//div[@class="stream"]//div[@class="story-body"]/a[@class="story-link"]/@href').extract(): ##找到循环体
			
			print url 
			yield scrapy.Request(url, callback = self.parse_page) 

	def parse_page(self, response):
		
		article = NytimesCrawlerItem()

		article['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
		article['link'] = response.url
		article['author'] = response.xpath('//span[starts-with(@class,"byline-author")]/text()').extract_first()     #starts-with(@tag, 'tagname') 
		                                                                                          #因为class tag有的是‘byline－author’ 有的是‘byline－author ’
		article['time'] = response.xpath('//div[contains(@class,"story-meta-footer")]//time/text()').extract_first()
		article['body'] = '\n'.join(response.xpath('//p[@class="story-body-text story-content"]/text()').extract()) #extract all text in the <p> tag
		
		yield article










