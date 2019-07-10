# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import re
from ..items import HuiCongWangItem
import os
import random
import requests
from time import sleep
import pymysql
import time
from lxml import etree
from bs4 import BeautifulSoup

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class CaiJiSpider(scrapy.Spider):
    name = 'cai_ji'

    def start_requests(self):
        """初始url"""
        # sql_id = "SELECT url FROM bus_spider_data WHERE TYPE = 'qiugou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        # cur.execute(sql_id)
        # res_all_list = cur.fetchall()
        # url = res_all_list[0][0]
        # for num in res_all_list:
        #     start_url = url.format(str(num))
        #
        #     print(start_url)
        #
        #     # start_url = 'https://s.hc360.com/seller/search.html?kwd=%E6%9C%8D%E8%A3%85&c=&F=&G=&nselect=1&pnum={}&ee=2'

        start_url = 'https://s.hc360.com/buyer/search.html?kwd=%E7%94%B5%E8%84%91&pnum=2'
        yield Request(url=start_url, callback=self.parse)

    def parse(self, response):
        """
        获取采购商品详情页url
        :param response:
        :return:
        """
        res_url_list = response.xpath('//div[@class="titBox"]/a/@href')
        for res_url in res_url_list:
            res_url = res_url.extract()

            yield Request(url=res_url, callback=self.parse_2)

    def parse_2(self, response):

        item = HuiCongWangItem()

        # 数据库获取id
        sql_id = "SELECT one_level,two_level,three_level, keyword  FROM bus_spider_data WHERE TYPE = 'qiugou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        for res_all in res_all_list:
            one_level = res_all[0]
            item['one_level_id'] = str(one_level)
            print('id.........', item['one_level_id'])

            two_level = res_all[1]
            item['two_level_id'] = str(two_level)
            print('id.........', item['two_level_id'])

            three_level = res_all[2]
            item['three_level_id'] = str(three_level)
            print('id.........', item['three_level_id'])

            keywords = res_all[-1]
            item['keywords'] = str(keywords)

        # # 公司简介
        # summary = '-'
        # try:
        #     summary = response.xpath('//*[@id="main"]/div[2]/div[1]/div[2]/table/tbody/tr[10]/td/a/text()').extract()
        #     summary = ''.join(summary).strip()
        #     print('summary', summary)
        # except:
        #     print('summary', summary)
        # item['summary'] = str(summary)
        #
        # # # 经营范围
        # scopes = '-'
        # try:
        #     scopes = response.xpath('//*[@id="main"]/div[2]/div[1]/div[2]/table/tbody/tr[10]/td/a/text()').extract()
        #     scopes = ''.join(scopes).strip()
        #     print('scopes', scopes)
        # except:
        #     print('scopes', scopes)
        # item['scopes'] = scopes
        #
        # # 地址
        address = '-'
        try:
            # address = re.findall('<tr>.*?公司地址:(.*?)</td>', response.text, re.S)
            # address = response.xpath('//*[@id="main"]/div[2]/div[1]/div[2]/table/tbody/tr[7]/td/text()').extract()[0]
            address = re.findall('<div class="comp-every">所在地区：(.*?)</div>', response.text, re.S)[0]
            print('address', address)
        except:
            print('address', address)
        item['address'] = str(address)


        # # 公司名称
        com_name = '-'
        try:
            # com_name = re.findall('<tr.*?公司名称.*?<td.*?>(.*?)</td>', response.text, re.S)[0].strip()
            # com_name = response.xpath('/html/body/div[@class="com_nav divc"]/div[@class="comname fl"]/a/@title').extract()[0]
            com_name = re.findall('<div class="comp-name comp-every">(.*?)</div>', response.text, re.S)[0]
            print('com_name', com_name)
        except:
            print('com_name', com_name)
        item['com_name'] = str(com_name)

        # # `create_date`
        create_date = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        item['create_date'] = create_date

        # # 商品价格
        price_list = []
        try:

            res_price = response.xpath('/html/body/div[5]/div[1]/div[2]/div[1]/div[2]/div[1]/ul/li[2]/span/i/text()').extract()
            for price in res_price:
                price = price.replace('¥', '').replace('\n', '').replace('\t', '').strip()
                price_list.append(price)
                print('价格........', price_list[-1])
        except:
            print('没有')
        item['price'] = str(price_list[-1])

        # # `title`,
        res_title = '-'
        try:
            res_title = response.xpath('//div[@class="bj-top"]/div/@href')[0].extract()
            res_title = res_title.strip()
            print('标题：', res_title)
        except:
            print('没有')
        item['title'] = str(res_title)

        # # `way`
        if price_list[-1]:
            way = '0'
        else:
            way = '1'
        print('way', way)
        item['way'] = way
        #
        # res_detail_html = response.text
        # try:
        #     soup = BeautifulSoup(res_detail_html, 'lxml')
        #     detail = soup.select('.box > div >.text')[0]
        #     # print('detail', detail)
        # except Exception as e:
        #     raise e
        # item['detail'] = str(detail)

        #
        # # 28. `units`,
        # # 商品价格
        res_price = ''
        try:
            res_price = response.xpath('/html/body/div[5]/div[1]/div[2]/div[1]/div[2]/div[1]/ul/li[1]/span/i/text()').extract()[0]
            res_price = re.findall('(\w+)', str(res_price), re.S)[-1]
            print(res_price)
        except:
            print(res_price)

        #
        # # 40. `linkman`
        link_man = '-'
        try:
            link_man = re.findall(
                '<li class="clearfix"><span class="span_icon icon_f">联系人</span><span class="span_txt">(.*?)</span></li>',
                response.text, re.S)[0]
            if link_man == '':
                link_man = '孙经理'
            print('man:', link_man)
        except:
            print('man:', link_man)
        item['linkman'] = str(link_man)


        #
        # # 41. `mobile`,
        # mobile = ''
        # try:
        #     mobile = re.findall('<li.*?><span.*?>手机</span>.*?>(.*?)</span>', response.text, re.S)[0].strip()
        #     print('mobile', mobile)
        # except:
        #     print('mobile', mobile)
        # item['mobile'] = str(mobile)
        #
        # # 求购数量
        # # 41. `mobile`,
        # num = ''
        # try:
        #     num = re.findall('<li.*?><span.*?>求购数量</span>.*?>(.*?)</span>', response.text, re.S)[0].strip()
        #     print('num', num)
        # except:
        #     print('num', num)
        # item['num'] = str(num)
        #
        # item['list_img'] = ''
        # item['imgs'] = ''
        #
        # print('数据完成..')
        #
        # # 随机时间
        # days = random.randint(120, 360)
        #
        # now = datetime.datetime.now()
        # delta = datetime.timedelta(days=days)
        # n_days = now + delta
        # item['end_time'] = n_days.strftime('%Y-%m-%d %H:%M:%S')
        # print(item['end_time'])
