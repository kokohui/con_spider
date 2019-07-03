# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import time
from bs4 import BeautifulSoup
import re
import random
import os
import requests
import pymysql
import json
from ..items import HuiCongWangItem

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class DataSpider(scrapy.Spider):
    name = 'data'

    d_id_3 = '185'
    keywords_name = '冷库'
    # start_url = 'http://www.912688.com/chanpin/59277801597388C5-orderBymultiple-aoddesc-viewlist-page{}.html'
    num_2 = 1

    def start_requests(self):
        url = 'https://s.hc360.com/seller/search.html?kwd=%E5%A4%A7%E7%A0%81%E5%A5%B3%E8%A3%85&pnum=1&ee=1'

        yield Request(url=url, callback=self.parse, )

    def parse(self, response):
        try:
            li_list = response.xpath('//div[@class="cont-left"]/div[@class="wrap-grid"]//li')
            for li in li_list:
                li_url = li.xpath('./div[@class="NewItem"]/div[@class="picmid pRel"]/a/@href').extract()[0]
                detail_url = "https:" + li_url
                print('/////////////////////////', detail_url)
                yield Request(url=detail_url, callback=self.detail_parse)
        except:
            print('有点错~')

    def detail_parse(self, response):
        print('parse_detail>>>>>')
        # print('------------------------',response.text)\\
        item = HuiCongWangItem()

        # 获取公司的名字
        com_name = '-'
        try:
            com_name = response.xpath('//div[@class="comply-name"]/p/a/text()')[0].extract()
            print(com_name)
        except:
            print(com_name)

        # 调用函数,执行sql语句
        try:
            # 执行sql语句，进行查询
            sql = "SELECT COUNT(0) FROM bus_product WHERE three_level_id = '{}' AND com_name = '{}'AND is_del = '0'".format(
                self.d_id_3, str(com_name))
            cur.execute(sql)
            # 获取查询结果
            result = cur.fetchall()
            result_count = int(result[0][0])
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', result_count)
            # conn.connect()

            d_id_3_3 = self.d_id_3
            keywords_name_2 = self.keywords_name

            if result_count > 0:
                print('重复了')
            else:
                mobile = response.xpath('//*[@id="dialogCorMessage"]//em/text()')[0].extract()
                mobile = re.findall(r'\d+', mobile, re.S)[0]
                print('mobile..........', mobile)
                if mobile:
                    print('爬--------------------------------------')

                    # shuju(response, item, d_id_3_3, keywords_name_2)
                    shuju(response, item, d_id_3_3, keywords_name_2)
                    print('爬++++++++++++++++++++++++++++++++++++++')
                    print('恭喜您,爬取{}成功,真是太厉害了!!!!!!'.format(self.num_2))
                    self.num_2 += 1
                    # return item
                else:
                    print('没有电话不爬取')

        except:
            print('沒有这条数据')


def shuju(response, item, d_id_3_3, keywords_name_2):
    print('detail_p>>>>>>>>>>>>>>>>>')

    # 保存图片信息
    try:
        os_img_1 = []
        str_ran = str(random.randint(0, 999999))
        os_img_1.append(str_ran)
        os.makedirs('d:\\b2b\\{}'.format(str_ran))
        #     将图片链接保存到硬盘
        res_img = response.xpath(
            '//div[@class="tab-content-container"]//li/div[@class="vertical-img zoomThumbActive"]//img/@src').extract()

        os_img_2_list = []
        for img_url in res_img:
            img_url = 'https:' + img_url
            code_img = requests.get(url=img_url).content
            img_name = str(random.randint(1, 999999))
            with open('d:\\b2b\\{}\\{}.jpg'.format(str_ran, img_name), 'wb') as f:
                f.write(code_img)
            os_img_2 = 'http://img.ktcx.cn/b2b/' + '{}/{}.jpg'.format(str_ran, img_name)
            os_img_2_list.append(os_img_2)
        os_img_2_str_1 = os_img_2_list[0]
        os_img_2_str = ','.join(os_img_2_list)
        item['list_img'] = os_img_2_str_1
        item['imgs'] = os_img_2_str
        print('保存图片ok..')
    except:
        print('图片错误.')

    # create_date = scrapy.Field()  # 创建时间
    create_date = '_'
    try:
        create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
        print(create_date)
    except:
        print(create_date)
    item['create_date'] = create_date

    # list_img = scrapy.Field()  # 图片1

    # price = scrapy.Field()  # 价格
    price = '-'
    try:
        price = response.xpath('//div[@id="oriPriceTop"]/text()').extract()[0].replace(' ', '').replace('\t', '').strip()
        print(price)
    except:
        print(price)
    item['price'] = price

    # title = scrapy.Field()  # 标题
    title = '-'
    try:
        title = response.xpath('//*[@id="comTitle"]/text()').extract()[0].replace(' ', '').replace('\t', '').strip()
        print(title)
    except:
        print(title)
    item['title'] = title

    # way = scrapy.Field()  # way
    if price != '_':
        way = '0'
    else:
        way = '1'
    print('way', way)
    item['way'] = way

    # two_level_id = scrapy.Field()  # 二级id
    two_level_id = '-'
    sql = "SELECT parent_id FROM bus_industry_category WHERE id = {}".format(d_id_3_3)
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        # 遍历结果
        for row in results:
            two_level_id = row[0]
            print('two_level_id', two_level_id)
        # 遍历结果
    except Exception as e:
        raise e
    item['two_level_id'] = two_level_id

    # one_level_id = scrapy.Field()  # 一级id
    one_level_id = '-'
    sql = "SELECT parent_id FROM bus_industry_category WHERE id = {}".format(two_level_id)
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        # 遍历结果
        for row in results:
            one_level_id = row[0]
            print('one_level_id', one_level_id)
        # 遍历结果
    except Exception as e:
        raise e
    item['one_level_id'] = one_level_id

    # three_level_id = scrapy.Field()  # 三级id
    item['three_level_id'] = d_id_3_3

    # keywords = scrapy.Field()
    keywords_list = []
    keywords_dict = {}
    keywords_dict['id'] = ''
    keywords_dict['keyword'] = keywords_name_2
    keywords_list.append(keywords_dict)
    keywords_json = json.dumps(keywords_list)
    item['keywords'] = keywords_json
    print('keywords_json', keywords_json)

    # imgs = scrapy.Field()

    # detail = scrapy.Field()
    html = '-'
    res_detail_html = response.text
    try:
        soup = BeautifulSoup(res_detail_html, 'lxml')
        html = str(soup.find('div', id="pdetail"))
        # print('html,,,,,,,,,,', html)
    except:
        print('_____')
        # print(html)
    item['detail'] = html

    # units = scrapy.Field()
    units = '-'
    try:
        # units = response.xpath('//div[@class="detail-right-con"]/div[@class="item-row-w"]/span[@class="supply-numb"]/text()')[0].extract()
        # units = re.findall('[\u4e00-\u9fa5]+', units, re.S)[0]
        print('units', units)
    except:
        print('units', units)
    print('units', units)
    item['units'] = units

    # com_name = scrapy.Field()
    com_name = '-'
    try:
        com_name = response.xpath('//div[@class="comply-name"]/p/a/text()')[0].extract()
        print('com_name', com_name)
    except:
        print(com_name)
    item['com_name'] = com_name

    # linkman = scrapy.Field()
    linkman = '-'
    try:
        linkman = response.xpath('//*[@id="dialogCorMessage"]/div[@class="p name"]/em/text()')[0].extract()
        linkman = re.findall('[\u4e00-\u9fa5]+', linkman, re.S)[0]
        print('linkman', linkman)
    except:
        print(linkman)
    item['linkman'] = linkman

    # mobile = scrapy.Field()
    mobile = '-'
    try:
        mobile = response.xpath('//*[@id="dialogCorMessage"]//em/text()')[0].extract()
        mobile = re.findall(r'\d+', mobile, re.S)[0]
        print('mobile', mobile)
    except:
        print(mobile)
    item['mobile'] = mobile
