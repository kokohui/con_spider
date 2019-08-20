# -*- coding: utf-8 -*-
import scrapy


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
