# -*- coding: utf-8 -*-
import scrapy


class ZhegnXinSpider(scrapy.Spider):
    name = 'zhegn_xin'
    allowed_domains = ['http://s.912688.com/prod/dy/search']
    start_urls = ['http://http://s.912688.com/prod/dy/search/']

    def parse(self, response):
        pass
