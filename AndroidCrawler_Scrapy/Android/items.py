# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AndroidItem(scrapy.Item):

	name = scrapy.Field()
	sub_category = scrapy.Field()
	app_url = scrapy.Field()
	icon_url = scrapy.Field()
	maturity_rating = scrapy.Field()
	maturity_rating_reason = scrapy.Field()
	review_score = scrapy.Field()
	review_num = scrapy.Field()
	datePublished = scrapy.Field()
	download_num = scrapy.Field()
	price = scrapy.Field()
	version = scrapy.Field()
	developer = scrapy.Field()
	developer_address = scrapy.Field()
	description = scrapy.Field()


