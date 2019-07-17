# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import WangshanghuiItem
import time
import datetime
import random
import re
from bs4 import BeautifulSoup


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'
    # allowed_domains = ['http://www.7wsh.com/']
    start_urls = ['http://so.7wsh.com/?page=1&kw=%E6%89%8B%E6%9C%BA&type=buy']

    def parse(self, response):
        detail_url_list = response.xpath('/html/body/div[4]/div[3]/div[1]/ul/li/dl/dd[1]/h3/a/@href')
        for detail_url in detail_url_list:
            detail_url = detail_url.extract()
            yield Request(url=detail_url, callback=self.detail_url)

    def detail_url(self, response):
        item = WangshanghuiItem()

        # # # 公司简介
        # summary = ''
        # try:
        #     summary = response.xpath('//*[@id="index-page"]/body/div[3]/div[3]/div[2]/ul/li[6]/span[2]/text()')[
        #         0].extract()
        #     print('summary', summary)
        # except:
        #     print('summary', summary)
        # item['summary'] = str(summary)
        #
        # # # # 经营范围
        # scopes = ''
        # try:
        #     scopes = \
        #     response.xpath('//*[@id="index-page"]/body/div[3]/div[3]/div[2]/ul/li[7]/span[2]/text()').extract()[0]
        #     print('scopes', scopes)
        # except:
        #     print('scopes', scopes)
        # item['scopes'] = scopes
        #
        # # # # 地址
        # address = ''
        # try:
        #     address = response.xpath('//span[@class="val"]/text()')[0].extract()
        #     print('address', address)
        # except:
        #     print('address', address)
        # item['address'] = str(address)
        #
        # # # # 公司名称
        # com_name = ''
        # try:
        #     com_name = response.xpath('//div[@class="member-company fl"]/ul/li[1]/a/text()')[0].extract()
        #     print('com_name', com_name)
        # except:
        #     print('com_name', com_name)
        # item['com_name'] = str(com_name)

        # # `create_date`
        create_date = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        item['create_date'] = create_date

        # # # 商品价格
        # price = ''
        # try:
        #     price = response.xpath('//div[@class="price"]/span/text()')[0].extract()
        #     print('price', price)
        # except:
        #     print('price', price)
        # item['price'] = str(price)
        #
        # # `title`,
        res_title = ''
        try:
            res_title = response.xpath('/html/body/div[4]/div[3]/div[2]/div[1]/div/h3/span/text()')[0].extract()
            res_title = res_title.strip()
            print('标题：', res_title)
        except:
            print('没有')
        item['title'] = str(res_title)

        # # # `way`
        # if price != '':
        #     way = '0'
        # else:
        #     way = '1'
        # print('way', way)
        # item['way'] = way
        #
        # res_detail_html = response.text
        # try:
        #     soup = BeautifulSoup(res_detail_html, 'lxml')
        #     # detail = soup.select('#main > .main > .pro_list > .pro_content')[0]
        #     detail = soup.find('div', class_='member-info fr')
        #     # print('detail', detail)
        # except Exception as e:
        #     raise e
        # item['detail'] = str(detail)
        #
        # # # # 28. `units`,
        # units = ''
        # item['units'] = str(units)
        #
        # # # 40. `linkman`
        # link_man = ''
        # try:
        #     link_man = response.xpath('//div[@class="member-company fl"]/ul/li[3]/a/text()')[0].extract()
        #     if link_man == '':
        #         link_man = '孙经理'
        #     print('man:', link_man)
        # except:
        #     print('man:', link_man)
        # item['linkman'] = str(link_man)
        #
        # # # 41. `mobile`,
        # mobile = ''
        # try:
        #     mobile = response.xpath('//div[@class="member-company fl"]/ul/li[4]/span[2]/text()')[0].extract()
        #     print('mobile', mobile)
        # except:
        #     print('mobile', mobile)
        # item['mobile'] = str(mobile)
        #
        # # # 求购数量
        # # # 41. `num`,
        # num = '不限'
        # try:
        #     # num = re.findall('<li><b>产品数量：</b>(.*?)</li>', response.text, re.S)[0].strip()
        #     num = response.xpath('//span[@class="fota"]/text()')[0].extract()
        #     print('num', num)
        # except:
        #     print('num', num)
        # item['num'] = str(num)
        #
        # item['list_img'] = ''
        # item['imgs'] = ''
        #
        # # print('数据完成..')
        #
        # # # 随机时间
        # days = random.randint(120, 360)
        #
        # now = datetime.datetime.now()
        # delta = datetime.timedelta(days=days)
        # n_days = now + delta
        # item['end_time'] = n_days.strftime('%Y-%m-%d %H:%M:%S')
        # print(item['end_time'])

