# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import random
import time
import os
import requests
import pymysql
import re
from bs4 import BeautifulSoup
from lxml import etree
from ..items import SouZhengXinItem

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标

# 'http://s.912688.com/prod/dy/search?kw=%E8%A1%A3%E6%9C%8D&pageSize=20&page={}'
class ZhengXinSpider(scrapy.Spider):
    name = 'zheng_xin'

    def start_requests(self):
        """
        处理初始url
        :return:
        """
        sql_id = "SELECT url FROM bus_spider_data WHERE TYPE = 'chengxin' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        url = res_all_list[0][0]
        for num in range(1, 2):
            url_2 = url.format(num)
            print(url_2)
            print('...........................................')
            yield Request(url=url_2, callback=self.parse)

    def parse(self, response):
        """
        获取公司页url, 并返回
        :param response:
        :return:
        """
        # print(response.text)
        com_url = response.xpath('//div[@class="product-left-new clearfix"]/ul/li[1]/div[@class="clearfix"]/div[@class="sm-list-information-new"]/p[@class="enterprise-name-n"]/a/@href')[0].extract()
        yield Request(url=com_url, callback=self.parse_2)

    def parse_2(self, response):
        com_j_url = response.xpath('//div[@class="shopcon-nav shopcon-nav-red z-f10"]/div/ul/li[3]/a/@href')[0].extract()
        print(com_j_url)
        yield Request(url=com_j_url, callback=self.parse_2_j)


    def parse_2_j(self, response):
        com_p_url = response.xpath('//div[@class="shopcon-nav shopcon-nav-red z-f10"]/div/ul/li[2]/a/@href')[0].extract()
        print(com_p_url)
        yield Request(url=com_p_url, callback=self.parse_2_p)
        print('1111111111111111111')

    def parse_2_p(self, response):
        print('2222222222222222222222222')
        # '/html/body/div[5]/div[2]/div[2]/div/div[2]/ul[2]/li[1]'
        # pao_deail_url_list = response.xpath('/html/body/div[5]/div[2]/div[2]/div/div[2]/ul[2]/li/div/a/@href').extract()[0]
        pao_deail_url_list = response.xpath('/html/body/div[5]/div[2]/div[2]/div/div[2]/ul[2]/li')
        for pao_deail_url in pao_deail_url_list:
            pao_deail_url = pao_deail_url.xpath('./div/a/@href')[0].extract()
            print('pao_deail_url:::::::::::::::::::::::::::::::::::::', pao_deail_url)

            yield Request(url=pao_deail_url_list, callback=self.parse_p_2, )

    # def parse_p_2(self, response):
    #     item = SouZhengXinItem()
    #     shuju(response, item)
    #     print('爬取成功>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')


# def shuju(response, item):
#
#             # 保存商品图片
#             try:
#                 os_img_1 = []
#                 str_ran = str(random.randint(0, 999999))
#                 os_img_1.append(str_ran)
#                 os.makedirs('/home/imgServer/spiders/{}'.format(str_ran))
#                 #     将图片链接保存到硬盘
#                 res_img = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[1]/div[1]/div/ul/li/img/@src')
#
#                 os_img_2_list = []
#                 # os_img_2_list
#                 for img_url in res_img:
#                     img_url = img_url.extract()
#                     img_url = img_url.strip()
#                     code_img = requests.get(url=img_url).content
#                     img_name = str(random.randint(1, 999999))
#                     with open('/home/imgServer/spiders/{}/{}.jpg'.format(str_ran, img_name), 'wb') as f:
#                         f.write(code_img)
#                     os_img_2 = 'http://img.ktcx.cn/spiders/' + '{}/{}.jpg'.format(str_ran, img_name)
#                     os_img_2_list.append(os_img_2)
#                 #
#                 os_img_2_str_1 = os_img_2_list[0]
#                 os_img_2_str = ','.join(os_img_2_list)
#                 # item['os_img_2_str_1'] = os_img_2_str_1
#                 # item['os_img_2_str'] = os_img_2_str
#
#                 print('图片ok', os_img_2_list)
#             except:
#                 print('图片错误.')
#
#             # 数据库获取id
#             sql_id = "SELECT one_level,two_level,three_level, keyword  FROM bus_spider_data WHERE TYPE = 'chengxin' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
#             cur.execute(sql_id)
#             print('sql_id?????????????', sql_id)
#             res_all_list = cur.fetchall()
#             for res_all in res_all_list:
#                 one_level = res_all[0]
#                 item['one_level_id'] = str(one_level)
#                 print('id.........', item['one_level_id'])
#
#                 two_level = res_all[1]
#                 item['two_level_id'] = str(two_level)
#                 print('id.........', item['two_level_id'])
#
#                 three_level = res_all[2]
#                 item['three_level_id'] = str(three_level)
#                 print('id.........', item['three_level_id'])
#
#                 keywords = res_all[-1]
#                 item['keywords'] = str(keywords)
#
#             # 2. `create_date`
#             create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
#             item['create_date'] = create_date
#
#             # 4. `list_img`
#             item['list_img'] = str(os_img_2_str_1)
#
#             # 5. `price`
#             try:
#                 price_list = []
#                 res_price = response.xpath(
#                     '/html/body/div[3]/div/div[1]/div[2]/div[2]/table//tr[@class="price"]/td[2]/div/span/text()').extract()
#                 for price in res_price:
#                     price = price.replace('\r', '').replace('\n', '').replace('\t', '')
#                     price_list.append(price)
#                     print('价格', price_list[-1])
#             except:
#                 print('没有')
#             item['price'] = str(price_list[-1])
#
#             # 6. `title`,
#             try:
#                 res_title = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/h1/text()')[0].extract()
#                 print('标题：', res_title)
#             except:
#                 print('没有')
#             item['title'] = str(res_title)
#
#             # 7. `way`
#             if price_list[-1]:
#                 way = '0'
#             else:
#                 way = '1'
#             item['way'] = way
#
#             # 15. `imgs`
#             item['imgs'] = os_img_2_str
#
#             # 23. `detail`
#             res_detail_html = response.text
#             try:
#                 soup = BeautifulSoup(res_detail_html, 'lxml')
#                 html = str(soup.select('#three-data > .table')[0])
#                 res_delia_HTML = str(soup.find('div', id="prodDetailDiv"))
#
#                 a = res_delia_HTML
#                 strinfo = re.compile('<p style="(.*?)".*?>.*?</p>')
#                 hh = strinfo.sub('', a)
#
#                 d = hh
#                 strinfo = re.compile('<div class="note">')
#                 hhh = strinfo.sub('', d)
#
#                 e = hhh
#                 strinfo = re.compile('<br.*?>')
#                 hhhh = strinfo.sub('', e)
#
#                 # b = hhhh
#                 # strinfo = re.compile('<img.*?src=.*?/>')
#                 # res_delia_html = strinfo.sub(' ', b)
#
#                 hebing_ = str(html) + '<br/><br/>' + str(hhhh)
#                 # print(hebing_)
#             except Exception as e:
#                 raise e
#             item['detail'] = str(hebing_)
#
#             # 28. `units`,
#             res_danwei = '-'
#             try:
#                 res_danwei = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/table//tr[2]/td[2]/div/text()')[
#                     0].extract()
#                 print('res_danwei:', res_danwei)
#             except:
#                 print('res_danwei:', res_danwei)
#             item['units'] = str(res_danwei)
#
#             # 39. `com_name`
#
#             # 40. `linkman`
#             link_man = '-'
#             try:
#                 link_man = re.findall('<li>.*?联系姓名：</span><a.*?>(.*?)</a></li>', response.text, re.S)[0]
#                 print('man:', link_man)
#             except:
#                 print('man:', link_man)
#             item['linkman'] = str(link_man)
#
#             # 41. `mobile`,
#             mobile = ''
#             try:
#                 mobile = response.xpath('/html/body/div[6]/div[5]/div[2]/ul/li[1]/span[3]/text()').extract()[0]
#                 print(mobile)
#             except:
#                 print('没有')
#             item['mobile'] = str(mobile)
#             print('数据完成..')