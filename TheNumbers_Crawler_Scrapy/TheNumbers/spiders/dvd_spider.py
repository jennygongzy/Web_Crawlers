# -*- coding: utf-8 -*-
import scrapy
from TheNumbers.items import DVDItems



class DvdSpiderSpider(scrapy.Spider):
	name = "dvd_spider"
	allowed_domains = ["www.the-numbers.com"]
	start_urls = ['http://www.the-numbers.com/home-market/chart-index/%s' % year for year in range(2009,2017)]

	def parse(self, response):
		week_urls_selector = response.xpath('//td[@class="month-weekend-day"]/a/@href')
		
		for week_url_selector in week_urls_selector:
			whole_week_url = response.urljoin(week_url_selector.extract())
			yield scrapy.Request(url = whole_week_url, callback =self.parse_week)


	def parse_week(self, response):

		dvd = DVDItems()

		rows = response.xpath('//table[@align="center"]//tr')

		for i in range(1,31):
			cells = rows[i].xpath('.//td')

			dvd['year'] = response.url.split('/')[-3]
			dvd['date'] = '/'.join(response.url.split('/')[-2:])
			form_type = response.url.split('/')[-4].split('-')[0]


			if form_type == 'packaged':
				dvd['DVD_Bluray_Comb'] = 'Comb'
				dvd['rank'] = str(i)
				dvd['previous_rank'] = '-'
				dvd['name'] = cells[1].xpath('.//text()').extract_first().encode(errors='ignore')
				dvd['units_this_week'] = cells[2].xpath('text()').extract_first()
				dvd['change'] = '-'
				dvd['total_unites'] = cells[3].xpath('text()').extract_first()
				dvd['spending_this_week'] = cells[4].xpath('text()').extract_first()
				dvd['total_spending'] = cells[5].xpath('text()').extract_first()
				dvd['weeks'] = cells[6].xpath('text()').extract_first()
			
			else: 
				dvd['DVD_Bluray_Comb'] = form_type
	
	 
				dvd['rank'] = str(i)
	
				previous_rank = cells[1].xpath('text()').extract_first()
				if previous_rank == None:
					dvd['previous_rank']='new'
				else:
					dvd['previous_rank']=previous_rank.replace('(','').replace(')','')
	
				dvd['name'] = cells[2].xpath('.//text()').extract_first().encode(errors='ignore')

				dvd['units_this_week'] = cells[3].xpath('text()').extract_first()
				dvd['change']  = cells[4].xpath('text()').extract_first().encode(errors='ignore')
				dvd['total_unites'] = cells[5].xpath('text()').extract_first()
				dvd['spending_this_week'] = cells[6].xpath('text()').extract_first()
				dvd['total_spending'] = cells[7].xpath('text()').extract_first()
				dvd['weeks'] = cells[8].xpath('text()').extract_first()


			yield dvd




