# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy import Request
import time
import random
import os
import requests
from bs4 import BeautifulSoup
from ..items import LazadaGongYingItem
import pymysql
conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'
    start_urls = ['https://www.lazada.com.my/catalog/?spm=a2o4k.home.search.1.75f824f6CLLXzu&q=%E8%80%B3%E6%9C%BA&_keyori=ss&from=search_history&sugg=%E8%80%B3%E6%9C%BA_0_1']

    def parse(self, response):
        # print(response.text)

        res_json = re.findall(r'<script>window.pageData=(.*?)</script>', response.text, re.S)[0]
        res_data = json.loads(res_json)
        productUrl_list = res_data["mods"]["listItems"]
        for productUrl in productUrl_list:
            productUrl = "https:" + productUrl["productUrl"]
            # print(productUrl, '2222222222222222222222')
            print('productUrl--->ok<')
            yield Request(url=productUrl, callback=self.parse_detail)

    def parse_detail(self, response):

        item = LazadaGongYingItem()

        # response_json = response.text.strip('app.run(').strip(')')
        # # print(response_json)
        # response_data = json.loads(response_json)
        # print(response_data)

        title = ''
        try:
            title = response.xpath('//title/text()').extract()[0]
            print('title', title)
        except:
            print('title', title)
        item['title'] = title

        price = ''
        try:
            price = re.findall('"salePrice":{"text":"(.*?)","value":(.*?)}}', response.text, re.S)[0][0]
            print('price:', price)
        except:
            print('price:', price)
        item['price'] = price

        # way
        if price != '':
            way = '0'
        else:
            way = '1'
        item['way'] = way

        # units
        units = ''
        item['units'] = units

        # 创建时间
        create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
        item['create_date'] = create_date

        # # 保存商品图片
        # os_img_2_list = []
        # div_str = ''
        # try:
        #     str_ran = str(random.randint(0, 999999))
        #     os.makedirs('/home/imgServer/hc/{}'.format(str_ran))
        #     #     将图片链接保存到硬盘
        #     img_url_list = re.findall('"poster":"(.*?)","src":".*?","type":".*?"', response.text, re.S)
        #     img_url_list = list(set(img_url_list))
        #     for img_url in img_url_list:
        #         img_url = "https:" + img_url
        #         # print('img_url', img_url)
        #         code_img = requests.get(url=img_url).content
        #         img_name = str(random.randint(1, 999999))
        #         with open('/home/imgServer/hc/{}/{}.jpg'.format(str_ran, img_name), 'wb') as f:
        #             f.write(code_img)
        #         os_img_2 = 'http://img.youkeduo.com.cn/hc/' + '{}/{}.jpg'.format(str_ran, img_name)
        #         os_img_2_list.append(os_img_2)
        #     os_img_2_str_1 = os_img_2_list[0]
        #     os_img_2_str = ','.join(os_img_2_list)
        #
        #     item['list_img'] = os_img_2_str_1
        #     item['imgs'] = os_img_2_str
        #
        #     print('图片ok', os_img_2_list)
        # except:
        #     print('图片错误.')
        #
        # # 产品详情
        # html = ''
        # try:
        #     # soup = BeautifulSoup(res_detail_html, 'lxml')
        #     html = re.findall(r'"desc":"(.*?)",', response.text, re.S)[0]
        #     print("html_1:", html)
        #
        #     strinfo = re.compile('<img.*?>')
        #     html_2 = strinfo.sub('', html)
        #
        #     strinfo = re.compile('<br.*?>')
        #     html_3 = strinfo.sub('', html_2)
        #
        #     strinfo = re.compile('慧聪网')
        #     html_4 = strinfo.sub('优客多', html_3)
        #     # 把下载图片添加到html
        #     div_list = ['<div id="img_detail">', '</div>']
        #     for os_img_2_url in os_img_2_list:
        #         os_img_2_url = '<img alt="{}" src="{}">'.format(title, os_img_2_url)
        #         div_list.insert(1, os_img_2_url)
        #     div_str = '\n'.join(div_list)
        #     print(div_str)
        # except :
        #     print("html_1:", html)
        # item['detail'] = str(div_str)

        try:
            con_url = re.findall('"sisUrl":"(.*?)",', response.text, re.S)[0]
            con_url = 'https:' + str(con_url)

            yield Request(url=con_url, callback=self.con_detail, meta={"item": item})
        except:
            print('公司错误')

    def con_detail(self, response):

        item = response.meta['item']
        print(item)
        con_name = response.xpath('//title/text()')[0].extract()
        print(con_name,type(con_name))
        item['com_name'] = str(con_name)


        yield item
