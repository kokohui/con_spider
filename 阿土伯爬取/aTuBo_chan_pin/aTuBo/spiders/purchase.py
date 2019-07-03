# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import time
from time import sleep
from ..items import AtuboItem
import re
from bs4 import BeautifulSoup
import random
import datetime
import pymysql
import os
import requests

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class PurchaseSpider(scrapy.Spider):
    name = 'purchase'
    # allowed_domains = ['http://www.atobo.com/Buys']
    start_urls = ['http://www.atobo.com/Products']

    def parse(self, response):

        """
        获取网站一级id 名字, 二级id, 名字
        :param response:
        :return:
        """
        item = AtuboItem()
        try:
            res_ul_list = response.xpath('//div[@class="filterlist"]/ul')
            for res_url in res_ul_list:
                one_class_name = res_url.xpath('./li[@class="title"]/a/text()').extract()[0]
                item['one_class_name'] = one_class_name
                one_class_id = res_url.xpath('./li[@class="title"]/a/@href').extract()[0].split('/')[-2]
                item['one_class_id'] = one_class_id
                print('one_class_name', one_class_name)
                print('one_class_id', one_class_id)
                res_two_li_list = res_url.xpath('./li[@class="alist"]/div/ul/li')
                for res_two_li in res_two_li_list:
                    res_url = 'http://www.atobo.com' + res_two_li.xpath('./a/@href').extract()[0]
                    print('res_url', res_url)
                    two_class_name = res_two_li.xpath('./a/text()').extract()[0]
                    print('two_class_name', two_class_name)
                    item['two_class_name'] = two_class_name
                    two_class_id = res_url.split('/')[-2]
                    item['two_class_id'] = two_class_id
                    print('two_class_id', two_class_id)

                    # sleep(1)
                    yield Request(url=res_url, callback=self.parse_0, meta={'item': item})
        except:
            print('超出~')

    def parse_0(self, response):
        """
        获取网站三级id, 名字, url
        :param response:
        :return:
        """
        item = response.meta['item']
        res_tree_li_list = response.xpath('//div[@id="filterCate"]/ul/li')
        for res_tree_li in res_tree_li_list:
            tree_class_url = res_tree_li.xpath('./a/@href')[0].extract()
            tree_class_id = tree_class_url.split('/')[-2]
            tree_class_name = res_tree_li.xpath('./a/text()')[0].extract()
            item['tree_class_id'] = tree_class_id
            item['tree_class_name'] = tree_class_name
            # print(tree_class_url)
            # print(tree_class_id)
            # print(tree_class_name)

            yield Request(url=tree_class_url, callback=self.parse_1)

    def parse_1(self, response):
        """
        商品列表详情页url
        :param response:
        :return:
        """
        print(response)
        item = response.meta['item']
        res_pro_list_url = response.xpath('//li[@class="pp_name"]//a/@href')
        for res_pro_url in res_pro_list_url:
            res_pro_url = res_pro_url.extract()
            res_pro_url = 'http://www.atobo.com' + res_pro_url
            print(res_pro_url)
            # sleep(2)
            yield Request(url=res_pro_url, callback=self.parse_2, meta={'item': item})

    # def start_requests(self):
    #
    #     yield Request(url='http://www.atobo.com/Products/8339971.html', callback=self.parse_2)

    def parse_2(self, response):
        """
        详情页内容解析
        :param response:
        :return:
        """

        item = AtuboItem()

        mobile = ''
        result_count = 0
        try:
            mobile = re.findall('<li class="header-info-mobile">手机：<strong>(.*?)</strong></li>', response.text, re.S)[0]
            # 查询公司存储个数, 如果没有则存储~
            com_name = response.xpath('//li[@class="right-context"]/div[1]/ul[1]/li/a/text()').extract()[0]
            sql_count = "select count(0) from bus_user where company_name='{}'".format(com_name)
            cur.execute(sql_count)
            result = cur.fetchall()
            result_count = int(result[0][0])
        except:
            print('没有手机号或公司重复')

        if mobile != ''and result_count < 1:
            print('................................................')

            # # 保存商品图片
            os_img_2_list = []
            try:
                os_img_1 = []
                str_ran = str(random.randint(0, 9999999))
                os_img_1.append(str_ran)
                os.makedirs('C:\\atubo_img\\{}'.format(str_ran))
                #     将图片链接保存到硬盘
                res_img = response.xpath('//*[@id="mycarousel"]/li/img/@src')

                # os_img_2_list = []
                # os_img_2_list
                for img_url in res_img:
                    img_url = img_url.extract()
                    img_url = 'http:' + img_url.strip()
                    code_img = requests.get(url=img_url).content
                    img_name = str(random.randint(1, 9999999))
                    with open('C:\\atubo_img\\{}\\{}.jpg'.format(str_ran, img_name), 'wb') as f:
                        f.write(code_img)
                    os_img_2 = 'http://img.ktcx.cn/atubo_img/' + '{}/{}.jpg'.format(str_ran, img_name)
                    os_img_2_list.append(os_img_2)

                os_img_2_str_1 = os_img_2_list[0]
                os_img_2_str = ','.join(os_img_2_list)
                item['list_img'] = os_img_2_str_1
                item['imgs'] = os_img_2_str

                print('图片ok', os_img_2_list)
            except:
                print('图片错误.')

            # # 数据库获取id
            # sql_id = "SELECT one_level,two_level,three_level, keyword  FROM bus_spider_data WHERE TYPE = 'qiugou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
            # cur.execute(sql_id)
            # print('sql_id?????????????', sql_id)
            # res_all_list = cur.fetchall()
            # for res_all in res_all_list:
            #     one_level = res_all[0]
            item['one_level_id'] = '1'
            #     print('id.........', item['one_level_id'])
            #
            #     two_level = res_all[1]
            item['two_level_id'] = '2'
            #     print('id.........', item['two_level_id'])
            #
            #     three_level = res_all[2]
            item['three_level_id'] = '3'
            #     print('id.........', item['three_level_id'])
            #
            #     keywords = res_all[-1]
            item['keywords'] = ''

            # 2. `create_date`
            create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
            item['create_date'] = create_date

            # 5. `price`
            res_price = '-'
            try:
                res_price = re.findall('<ul><li class="para-left">价格：</li><li class="para-right price".*?>(.*?)</li>', response.text, re.S)[0]
                if res_price.startswith('￥'):
                    res_price = re.findall('\d+', res_price, re.S)[0]
                print('res_price:', res_price)
            except:
                print('res_price:', res_price)
            item['price'] = str(res_price)

            # 6. `title`,
            res_title = '-'
            try:
                res_title = response.xpath('//li[@class="product-title"]/text()')[0].extract()
                print('标题：', res_title)
            except:
                print('标题：', res_title)
            item['title'] = str(res_title)

            # 7. `way`
            if res_price:
                way = '0'
            else:
                way = '1'
            item['way'] = way

            # # 23. `detail`
            res_detail_html = response.text
            try:
                soup = BeautifulSoup(res_detail_html, 'lxml')
                res_delia = str(soup.find('div', id="Intro_Div_0"))

                strinfo = re.compile('<img.*?>')
                html_2 = strinfo.sub('', res_delia)

                strinfo = re.compile('<br>')
                html_3 = strinfo.sub('', html_2)

                strinfo = re.compile('慧聪网')
                html_4 = strinfo.sub('优客多', html_3)
                # print(html_4)

                # 把下载图片添加到html
                div_list = ['<div id="img_detail">', '</div>']
                for os_img_2_url in os_img_2_list:
                    os_img_2_url = '<img alt="{}" src="{}">'.format(res_title, os_img_2_url)
                    div_list.insert(1, os_img_2_url)
                div_str = '<br>\n'.join(div_list)

                html_all = html_4 + '\n' + div_str
                # print(html_all)
            except Exception as e:
                raise e
            item['detail'] = str(res_delia)

            # # 28. `units`,
            res_danwei = ''
            try:
                res_price = re.findall('<ul><li class="para-left">价格：</li><li class="para-right price".*?>(.*?)</li>', response.text, re.S)[0]
                if res_price.startswith('￥'):
                    res_danwei = str(res_price).split('/')[-1]
                print('res_danwei>>>>>>>>>>>>>:', res_danwei)
            except:
                print('res_danwei:', res_danwei)
            item['units'] = str(res_danwei)

            # # 39. `com_name`
            com_name = ''
            try:
                com_name = response.xpath('//li[@class="right-context"]/div[1]/ul[1]/li/a/text()').extract()[0]
                print('com_name', com_name)
            except:
                print('com_name', com_name)
            item['com_name'] = str(com_name)

            # # 40. `linkman`
            link_man = ''
            try:
                link_man = re.findall('<ul><li class="rc-left">联系：</li><li class="rc-right">(.*?)</li>', response.text, re.S)[0]
                print('man:', link_man)
            except:
                print('man:', link_man)
            item['linkman'] = str(link_man)

            # # 41. `mobile`,
            mobile = ''
            try:
                mobile = re.findall('<li class="header-info-mobile">手机：<strong>(.*?)</strong></li>', response.text, re.S)[0]
                print(mobile)
            except:
                print('没有')
            item['mobile'] = str(mobile)
            # print('数据完成..')

            # # 公司简介
            summary = ''
            try:
                summary = response.xpath('//div[@id="Intro_Div_1"]/text()').extract()[0].strip()
                print('summary', summary)
            except:
                print('summary', summary)
            item['summary'] = summary

            # # 经营范围
            scopes = ''
            try:
                scopes = re.findall('<ul><li class="rc-left">主营：</li><li class="rc-right">.*?<a .*?>(.*?)</a>.*?</li>', response.text, re.S)[0].strip()
                print('scopes', scopes)
            except:
                print('scopes', scopes)
            item['scopes'] = scopes

            # # 地址
            address = ''
            try:
                address = re.findall('<ul><li class="rc-left">地址：</li><li class="rc-right">(.*?)</li></ul>', response.text, re.S)[0]
                print('address', address)
            except:
                print('address', address)
            item['address'] = str(address)

            # # 求购数量
            # # 41. `num`,
            num = '0'
            try:
                num = re.findall('<ul><li class="para-left">库存数量：</li><li class="para-right">(.*?)</li>', response.text, re.S)[0].strip()
                print('num', num)
            except:
                print('num', num)
            item['num'] = str(num)


            # # 随机时间
            days = random.randint(120, 360)
            now = datetime.datetime.now()
            delta = datetime.timedelta(days=days)
            n_days = now + delta
            item['end_time'] = n_days.strftime('%Y-%m-%d %H:%M:%S')
            print(item['end_time'])
            # item['one_class_name'] = '1'
            # item['one_class_id'] = '2'
            # item['two_class_name'] = '3'
            # item['two_class_id'] = '4'
            # item['tree_class_name'] = '5'
            # item['tree_class_id'] = '6'

            item['list_img'] = ''
            item['imgs'] = ''

            print('数据完成..')
    #
    #         # sleep(2)
            yield item



