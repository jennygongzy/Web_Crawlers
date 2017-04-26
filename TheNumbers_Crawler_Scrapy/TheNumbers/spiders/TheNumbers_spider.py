# -*- coding: utf-8 -*-
import scrapy
from TheNumbers.items import ThenumbersItem



class TheNumbersSpider(scrapy.Spider):
	name = "TheNumbers_spider"
	allowed_domains = ["www.the-numbers.com"]
	start_urls = ['http://www.the-numbers.com/box-office/%s' % year for year in range(1996,2018)]

	#if use start_urls to be the first request, has to name the parse function "parse", as default
	def parse(self, response):
		week_urls_selector = response.xpath('//td[@class="month-weekend-day"]/a/@href')
	
		for week_url_selector in week_urls_selector:
			whole_week_url = response.urljoin(week_url_selector.extract())
			yield scrapy.Request(url = whole_week_url, callback =self.parse_week)


	def parse_week(self, response):

		movie = ThenumbersItem() 

		rows = response.xpath('//table[@align="CENTER"]//tr') #try put response into iteration
		# only keep Top 50, the first row is header. rows[1]~rows[50]
		for i in range(1,51):
			cells = rows[i].xpath('.//td')
		
			movie['year'] = response.url.split('/')[-3]
			movie['date'] = '/'.join(response.url.split('/')[-2:])
			movie['weekly_or_weekend'] = response.url.split('/')[-4]

	#from table, column = 10 
	#1
			movie['rank'] = str(i)

	#2
			previous_rank = cells[1].xpath('text()').extract_first()
			if previous_rank == None:
				movie['previous_rank']='new'
			else:
				movie['previous_rank']=previous_rank.replace('(','').replace(')','')
	#3
			movie_name = cells[2].xpath('.//text()').extract_first()
			#if the movie name is not the full name, use the href to generate the full name.
			if movie_name[-1] == u'\u2026': ##u'\u2026': '...' 
				movie['name'] = ' '.join(cells[2].xpath('.//@href').extract_first().split('/')[-1].split('#')[0].split('-'))
			else:
				movie['name'] = movie_name
    #4
			distributor = cells[3].xpath('.//text()').extract_first()
			if distributor[-1] == u'\u2026':
				movie['distributor'] = ' '.join(cells[3].xpath('.//@href').extract_first().split('/')[-1].split('-'))
			else:
				movie['distributor'] = distributor
    #5
			movie['gross'] = cells[4].xpath('text()').extract_first().encode(errors='ignore')
	#6
			movie['change'] = cells[5].xpath('text()').extract_first().encode(errors='ignore')
	#7
			movie['thtrs'] = cells[6].xpath('text()').extract_first().encode(errors='ignore')
	#8
			movie['Per_Thtrs'] = cells[7].xpath('text()').extract_first().encode(errors='ignore')
	#9
			movie['total_gross'] = cells[8].xpath('text()').extract_first().encode(errors='ignore')
	#10
			movie['days'] = cells[9].xpath('text()').extract_first().encode(errors='ignore')

			yield movie 




