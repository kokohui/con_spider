# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import re
from ..items import HuiCongGongItem
import os
import random
import requests
from time import sleep
import pymysql
import time
from lxml import etree

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SuppySpider(scrapy.Spider):
    name = 'suppy'
    start_urls = ['https://www.hc360.com/']

    def parse(self, response):
        """获取123目录名字, url"""

        div_list = response.xpath('//*[@id="category"]/div')
        for div in div_list:
            one_class_name = div.xpath('./@data-name')[0].extract()

            li_list = div.xpath('./div[@class="sideBarLeft"]//li')
            for li in li_list:
                two_class_name = li.xpath('./span/text()')[0].extract()

                a_list = li.xpath('./div[@class="sideBarLinkBox"]/a')
                for a in a_list:
                    tree_class_name = a.xpath('./text()')[0].extract()

                    tree_class_url = a.xpath('./@href')[0].extract()
                    print(tree_class_url)
                    tree_class_id = tree_class_url.split('/')[-1].replace('.html', '')

                    item = HuiCongGongItem()
                    item['one_class_name'] = str(one_class_name)
                    item['two_class_name'] = str(two_class_name)
                    item['tree_class_name'] = str(tree_class_name)
                    item['tree_class_id'] = str(tree_class_id)

                    yield item

