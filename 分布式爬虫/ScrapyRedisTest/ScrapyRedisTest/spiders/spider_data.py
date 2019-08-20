# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider


class SpiderDataSpider(RedisCrawlSpider):
    name = 'spider_data'
    # allowed_domains = ['www.baidu.com\']
    # start_urls = ['http://www.baidu.com\/']

    redis_key = 'shixisheng:start_urls'

    def parse(self, response):
        pass
