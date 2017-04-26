# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


import random
import base64

##Add fake user agents ##
class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""
    def __init__(self, agents):
        self.agents = agents
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))
    def process_request(self, request, spider):
        #print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

