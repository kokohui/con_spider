# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import NpicpItem
import pymysql
import time
import os
import random
import re
import requests
from bs4 import BeautifulSoup
import datetime
from lxml import etree
import chardet

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'
    start_urls = ['https://www.npicp.com/buy/16-572-0-0-0-1.html']

    def parse(self, response):
        res_url_list = response.xpath('/html/body/div[6]/div/div[1]/div[3]/ul/li/div/div[1]/div/div[1]/a/@href').extract()
        for res_url in res_url_list:
            print(res_url)
            yield Request(url=res_url, callback=self.detail_parse)


    def detail_parse(self, response):
        item = NpicpItem()

        mobile = ''
        com_name = ''
        result_count = 0
        try:
            mobile = response.xpath('/html/body/div[5]/div/div[1]/div[2]/div[2]/div[6]/span/text()')[0].extract().strip()
            com_name = str(response.xpath('/html/body/div[5]/div/div[1]/div[2]/div[2]/div[1]/a/text()').extract()[0]).strip()
            # sql_count = "select count(0) from bus_user where company_name='{}'".format(com_name)
            # cur.execute(sql_count)
            # result = cur.fetchall()
            # result_count = int(result[0][0])
        except:
            print('没有手机号或公司重复')
        item['com_name'] = com_name
        item['mobile'] = mobile

        if mobile != '':
            print('................................................')

        #     # 数据库获取id
        #     sql_id = "SELECT one_level,two_level,three_level,keyword  FROM bus_spider_data WHERE source = '找商网' and  TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        #     cur.execute(sql_id)
        #     print('sql_id?????????????', sql_id)
        #     res_all_list = cur.fetchall()
        #     for res_all in res_all_list:
        #         one_level = res_all[0]
        #         item['one_level_id'] = str(one_level)
        #         print('id.........', item['one_level_id'])
        #
        #         two_level = res_all[1]
        #         item['two_level_id'] = str(two_level)
        #         print('id.........', item['two_level_id'])
        #
        #         three_level = res_all[2]
        #         item['three_level_id'] = str(three_level)
        #         print('id.........', item['three_level_id'])
        #
        #         keywords = res_all[-1]
        #         item['keywords'] = str(keywords)
        #

            # 创建时间
            create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
            item['create_date'] = create_date

            # 价格
            price = '面议'
            try:
                price = str(
                    response.xpath('/html/body/div[5]/div/div[1]/div[2]/div[2]/div[4]/span/text()').extract()[
                        0].strip())
                price = re.findall(r'\d+', str(price), re.S)
                price = price[0] + '.' + price[1]
                print('price', price)
            except:
                print('price', price)
            item['price'] = price

            # 标题
            title = ''
            try:
                title = str(response.xpath('//h1/text()').extract()[0])
                print('title', title)
            except:
                print('title', title)
            item['title'] = title

            # way
            if price != '':
                way = '0'
            else:
                way = '1'
            item['way'] = way

            res_detail_html = response.text
            try:
                soup = BeautifulSoup(res_detail_html, 'lxml')
                html_1 = str(soup.find('div', class_="xiangqing-left-line4"))

                strinfo = re.compile('<img.*?>')
                html_all = strinfo.sub('', html_1)
            except Exception as e:
                raise e
            item['detail'] = str(html_all)

            # units
            units = ''
            item['units'] = units

            # # 求购数量
            # # 41. `num`,
            num = '不限'
            item['num'] = num

            item['list_img'] = ''
            item['imgs'] = ''


            # linkman
            linkman = ''
            try:
                # linkman = re.findall('<span.*?>联系人：</span><span.*?>(.*?)</span>', response.text)[0]
                linkman = response.xpath('/html/body/div[5]/div/div[1]/div[2]/div[2]/div[3]/span/text()').extract()[0]
                linkman = linkman.split('：')[-1]
                print('linkman', linkman)
            except:
                print('linkman', linkman)
            item['linkman'] = linkman

            # address
            address = ''
            try:
                address = response.xpath('/html/body/div[5]/div/div[1]/div[2]/div[2]/div[2]/text()').extract()[0]
                address = address.split('：')[-1]
                print('address', address)
            except:
                print('address', address)
            item['address'] = address

            # 随机时间
            days = random.randint(120, 360)

            now = datetime.datetime.now()
            delta = datetime.timedelta(days=days)
            n_days = now + delta
            item['end_time'] = n_days.strftime('%Y-%m-%d %H:%M:%S')
            print(item['end_time'])

            con_url = response.xpath('/html/body/div[5]/div/div[1]/div[2]/div[2]/div[1]/a/@href')[0].extract()
            print(con_url)
            self.detail_con(con_url, item)

        #
        #     yield item

    @classmethod
    def detail_con(self, con_url, item):
        print('...........', con_url)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        }
        con_text = requests.get(url='https://www.npicp.com/company/li7568948', headers=headers, verify=False).text
        tree = etree.HTML(con_text)

        scopes = '-'
        try:
            scopes = tree.xpath('/html/body/div[5]/div[1]/div[1]/div[3]/ul/li[4]/text()')[0]
            print('scopes', scopes.encodeing("utf-8"))
        except:
            print('scopes', scopes)
        item['scopes'] = scopes

        summary = ''
        try:
            summary = tree.xpath('/html/body/div[5]/div[2]/div[1]/div[2]/text()')[0]
            # print('summary>>>>>>>>>>>>>>>', summary.encode("utf-8"))
        except:
            print('summary', summary)
        item['summary'] = summary

