# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import scrapy
from scrapy import Request
import re
import random
import os
import requests
import time
from bs4 import BeautifulSoup
from ..items import HundredZhaoShangItem
import pymysql
import datetime
from lxml import etree

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'

    def start_requests(self):
        item = HundredZhaoShangItem()

        sql_id = "SELECT url, id FROM bus_spider_data WHERE source = '100招商网' and TYPE = 'caigou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        url = res_all_list[0][0]
        spdier_data_id = res_all_list[0][-1]
        print('spdier_data_id:::', spdier_data_id)
        item['spdier_data_id'] = spdier_data_id
        for num in range(1, 10):
            start_url = url + str(num)

            yield Request(url=start_url, callback=self.parse, meta={"item": item})

    def parse(self, response):
        item = response.meta["item"]

        detail_url_list = response.xpath('/html/body/div[5]/ul/li/a[2]/@href').extract()
        for detail_url in detail_url_list:
            detail_url = 'http://www.zhaoshang100.com' + detail_url
            yield Request(url=detail_url, callback=self.detail_parse, meta={"item": item})

    def detail_parse(self, response):
        item = response.meta["item"]

        # `mobile`,
        mobile = ''
        try:
            mobile = response.xpath('//div[@class="personal_bottom"]/span/text()').extract()[0]
            print('mobile', mobile)
        except:
            print('mobile', mobile)
        item['mobile'] = str(mobile)

        com_name = response.xpath('//*[@id="product-detail"]/div[2]/div[2]/ul/li[1]/a/text()').extract()[0]
        print('com_name:', com_name)
        sql_count = "select count(0) from bus_user where company_name='{}'".format(com_name)
        cur.execute(sql_count)
        result = cur.fetchall()
        result_count = int(result[0][0])
        print(result_count)

        #`title`,
        res_title = '-'
        try:
            res_title = response.xpath('//*[@id="title"]/text()')[0].extract()
            res_title = res_title.strip()
            print('标题：', res_title)
        except:
            print('没有')
        item['title'] = str(res_title)

        if res_title != '-' and mobile and result_count == 0:
            print('...............')

            # 数据库获取id
            sql_id = "SELECT one_level,two_level,three_level, keyword  FROM bus_spider_data WHERE source = '100招商网' and TYPE = 'caigou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
            cur.execute(sql_id)
            print('sql_id?????????????', sql_id)
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

            # 经营范围
            scopes = '-'
            try:
                scopes = response.xpath('//*[@id="product-detail"]/div[3]/div[1]/div[1]/ul/li[4]/text()').extract()[-1]
                print('scopes', scopes)
            except:
                print('scopes', scopes)
            item['scopes'] = scopes

            # # # 地址
            address = '-'
            try:
                address = response.xpath('//*[@id="product-detail"]/div[2]/div[2]/ul/li[2]/span/text()').extract()[0]
                print('address', address)
            except:
                print('address', address)
            item['address'] = str(address)

            # 公司名称
            com_name = '-'
            try:
                com_name = response.xpath('//*[@id="product-detail"]/div[2]/div[2]/ul/li[1]/a/text()').extract()[0]
                print('com_name', com_name)
            except:
                print('com_name', com_name)
            item['com_name'] = str(com_name)

            # # `create_date`
            create_date = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
            item['create_date'] = create_date

            # # 商品价格
            res_price = ''
            try:
                res_price = re.findall('<em>￥</em>(.*?)<em>', response.text, re.S)
                res_price = response.xpath('//*[@id="product-detail"]/div[2]/div[2]/dl/dd/ul/li/p[1]/span/text()').extract()[1]
                print(res_price)
            except:
                print('没有')
            item['price'] = str(res_price)

            # # `way`
            if res_price[-1]:
                way = '0'
            else:
                way = '1'
            print('way', way)
            item['way'] = way

            res_detail_html = response.text
            try:
                soup = BeautifulSoup(res_detail_html, 'lxml')
                detail = soup.find('div', id="content_tag")
                # print('detail', detail)
            except Exception as e:
                raise e
            item['detail'] = str(detail)

            # `units`,
            units = ''
            item['units'] = str(units)

            # # 40. `linkman`
            link_man = '-'
            try:
                link_man = response.xpath('//*[@id="product-detail"]/div[2]/div[2]/div[3]/div[2]/div/span/text()').extract()[0]
                if link_man == '':
                    link_man = '孙经理'
                print('man:', link_man)
            except:
                print('man:', link_man)
            item['linkman'] = str(link_man)

            # # 求购数量
            # # 41. `num`,
            num = '不限'
            item['num'] = num

            item['list_img'] = ''
            item['imgs'] = ''


            # 随机时间
            days = random.randint(120, 360)

            now = datetime.datetime.now()
            delta = datetime.timedelta(days=days)
            n_days = now + delta
            item['end_time'] = n_days.strftime('%Y-%m-%d %H:%M:%S')
            print(item['end_time'])

            com_url = response.xpath('//*[@id="product-detail"]/div[2]/div[2]/ul/li[1]/a/@href').extract()[0]
            print('......', com_url)

            item = self.con_detail(com_url, item)


            yield item

    @staticmethod
    def con_detail(com_url, item):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        response_text = requests.get(url=com_url, headers=headers)

        response_text.encoding = 'GBK'
        response_text = response_text.text
        tree = etree.HTML(response_text)

        # 公司简介
        summary = '-'
        try:
            summary = tree.xpath('//*[@id="bodyright"]/table//tr/td[1]/text()')[0].strip()[:-1]
            print('summary', summary)
        except:
            print('summary', summary)
        item['summary'] = str(summary)

        return item


