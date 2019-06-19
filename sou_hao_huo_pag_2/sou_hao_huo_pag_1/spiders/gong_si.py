# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import random
import time
import os
import requests
# from ..items import SouHaoHuoItem
import pymysql
import re
import json
from bs4 import BeautifulSoup


class DianShangSpider(scrapy.Spider):
    name = 'dian_shang'

    start_url = 'http://www.912688.com/supply/20702717.html'

    def start_requests(self):
        # for num in range(2, 100):
        #     start_url = self.start_url.format(str(num))
        #     print('开始爬取第{}条数据'.format(num))
        yield scrapy.Request(url=self.start_url, callback=self.parse)


    def shuju(response, item, d_id_3_3, keywords_name_2):

        # 41. `mobile`,
        try:
            res_phone = response.xpath('/html/body/div[5]/div[5]/div[2]/ul/li[1]/span[3]/text()')[0].extract()
        except:
            print('没有')
        # str(res_phone)
        item['mobile'] = str(res_phone)

        # 42. `add_by`

        print('数据完成..')
















