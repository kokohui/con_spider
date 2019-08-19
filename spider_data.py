# -*- coding: utf-8 -*-
import scrapy


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'
    allowed_domains = ['https://www.npicp.com/buy']
    start_urls = ['http://https://www.npicp.com/buy/']

    def parse(self, response):
        pass
