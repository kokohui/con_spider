# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import random
import os
import requests
import time
from bs4 import BeautifulSoup
from ..items import LeYuItem
import pymysql

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SitongSpider(scrapy.Spider):
    name = 'sitong'
    # allowed_domains = ['http://www.sitongzixun.com/channel_Buy/i14717.html.html']
    # start_urls = ['http://http://www.sitongzixun.com/channel_Buy/i14717.html.html/']

    def start_requests(self):

        sql_id = "SELECT url,id FROM bus_spider_data WHERE TYPE = 'qiugou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        url_pag = res_all_list[0][0]
        # url_pag = 'http://www.sitongzixun.com/channel_Buy/i14717.html.html?page={}&rows=16780'



        for num in range(1, 3):
            url = url_pag.format(num)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        res_li_list = response.xpath('//div[@class="chelist fl"]/div[@class="imglist"]/ul/li')[15:]
        for res_li in res_li_list:
            res_url = 'http:' + res_li.xpath('./span/a/@href')[0].extract()
            # print(res_url)
            yield Request(url=res_url,callback=self.parse_2)

    def parse_2(self, response):

        item = LeYuItem()

        mobile = re.findall('<li.*?><span.*?>手机</span>.*?>(.*?)</span>', response.text, re.S)
        if mobile:
            print('................................................')

            # 数据库获取id
            sql_id = "SELECT one_level,two_level,three_level, keyword  FROM bus_spider_data WHERE TYPE = 'qiugou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
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

            # 公司简介
            summary = '-'
            try:
                summary = response.xpath('//*[@id="main"]/div[2]/div[1]/div[2]/table/tbody/tr[10]/td/a/text()').extract()
                summary = ''.join(summary).strip()
                print('summary', summary)
            except:
                print('summary', summary)
            item['summary'] = str(summary)

            # # 经营范围
            scopes = '-'
            try:
                scopes = response.xpath('//*[@id="main"]/div[2]/div[1]/div[2]/table/tbody/tr[10]/td/a/text()').extract()
                scopes = ''.join(scopes).strip()
                print('scopes', scopes)
            except:
                print('scopes', scopes)
            item['scopes'] = scopes

            # # 地址
            address = '-'
            try:
                # address = re.findall('<tr>.*?公司地址:(.*?)</td>', response.text, re.S)
                address = response.xpath('//*[@id="main"]/div[2]/div[1]/div[2]/table/tbody/tr[7]/td/text()').extract()[0]
                print('address', address)
            except:
                print('address', address)
            item['address'] = str(address)

            # # 公司名称
            com_name = '-'
            try:
                # com_name = re.findall('<tr.*?公司名称.*?<td.*?>(.*?)</td>', response.text, re.S)[0].strip()
                com_name = response.xpath('/html/body/div[@class="com_nav divc"]/div[@class="comname fl"]/a/@title').extract()[0]

                print('com_name', com_name)
            except:
                print('com_name', com_name)
            item['com_name'] = str(com_name)

            # `create_date`
            create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
            item['create_date'] = create_date


            # 商品价格
            try:
                price_list = []
                res_price = response.xpath('//*[@id="main"]/div[1]/div[2]/div[1]/div/div[3]/div[2]/div/span[1]/b/text()').extract()
                for price in res_price:
                    price = price.replace('\r', '').replace('\n', '').replace('\t', '').strip()
                    price_list.append(price)
                    print('价格........', price_list[-1])
            except:
                print('没有')
            item['price'] = str(price_list[-1])

            # `title`,
            res_title = '-'
            try:
                res_title = response.xpath('//*[@id="main"]/div[1]/div[2]/div[1]/div/div[1]/h1/text()')[0].extract()
                res_title = res_title.strip()
                print('标题：', res_title)
            except:
                print('没有')
            item['title'] = str(res_title)

            # `way`
            if price_list[-1]:
                way = '0'
            else:
                way = '1'
            print('way', way)
            item['way'] = way

            res_detail_html = response.text
            try:
                soup = BeautifulSoup(res_detail_html, 'lxml')
                detail = soup.select('.box > div >.text')[0]
                # print('detail', detail)
            except Exception as e:
                raise e
            item['detail'] = str(detail)

            # 28. `units`,
            units = ''
            item['units'] = str(units)

            # 40. `linkman`
            link_man = '-'
            try:
                link_man = re.findall('<li class="clearfix"><span class="span_icon icon_f">联系人</span><span class="span_txt">(.*?)</span></li>', response.text, re.S)[0]
                if link_man == '':
                    link_man = '孙经理'
                print('man:', link_man)
            except:
                print('man:', link_man)
            item['linkman'] = str(link_man)

            # 41. `mobile`,
            mobile = ''
            try:
                mobile = re.findall('<li.*?><span.*?>手机</span>.*?>(.*?)</span>', response.text, re.S)[0].strip()
                print('mobile', mobile)
            except:
                print('mobile', mobile)
            item['mobile'] = str(mobile)

            # 求购数量
            # 41. `mobile`,
            num = ''
            try:
                num = re.findall('<li.*?><span.*?>求购数量</span>.*?>(.*?)</span>', response.text, re.S)[0].strip()
                print('num', num)
            except:
                print('num', num)
            item['num'] = str(num)


            item['list_img'] = ''
            item['imgs'] = ''

            print('数据完成..')
            # return item