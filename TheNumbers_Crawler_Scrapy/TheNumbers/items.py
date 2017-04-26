# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThenumbersItem(scrapy.Item):
	name = scrapy.Field()
	date = scrapy.Field()
	year = scrapy.Field()
	weekly_or_weekend = scrapy.Field()
	rank = scrapy.Field()
	previous_rank = scrapy.Field()
	distributor = scrapy.Field()
	gross = scrapy.Field()
	change = scrapy.Field()
	thtrs = scrapy.Field()
	Per_Thtrs = scrapy.Field()
	total_gross = scrapy.Field()
	days = scrapy.Field()
    
  
class DVDItems(scrapy.Item):
	name = scrapy.Field()
	date = scrapy.Field()
	year = scrapy.Field()
	DVD_Bluray_Comb = scrapy.Field()
	rank = scrapy.Field()
	previous_rank = scrapy.Field()
	units_this_week = scrapy.Field()
	total_unites = scrapy.Field()
	change = scrapy.Field()
	spending_this_week = scrapy.Field()
	total_spending = scrapy.Field()
	weeks = scrapy.Field()
