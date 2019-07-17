# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import CailiaowangItem
from bs4 import BeautifulSoup
import re
import datetime
import random
import time
import pymysql

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'
    # start_urls = ['http://www.cailiao.com/frontend/Search/index?keyword=%E7%94%B5%E8%84%91&search_type=purchase']
    # start_urls = ['http://www.cailiao.com/frontend/Search/index?keyword=电脑&search_type=purchase']

    def start_requests(self):
        sql_id = "SELECT url,id FROM bus_spider_data WHERE  source='材料网' and TYPE = 'caigou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        url_pag = res_all_list[0][0]
        for num in range(1, 20):
            url = url_pag.format(num)
            yield Request(url=url, callback=self.parse)



    def parse(self, response):

        detail_url_list = response.xpath('//div[@class="product_main clearfix mt20"]//li/a/@href')
        for detail_url in detail_url_list:
            detail_url = detail_url.extract()
            yield Request(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = CailiaowangItem()

        mobile = response.xpath('//div[@class="member-company fl"]/ul/li[4]/span[2]/text()')[0].extract()
        # 查询公司存储个数, 如果没有则存储~
        com_name = response.xpath('//div[@class="member-company fl"]/ul/li[1]/a/text()')[0].extract()
        sql_count = "select count(0) from bus_user where company_name='{}'".format(com_name)
        cur.execute(sql_count)
        result = cur.fetchall()
        result_count = int(result[0][0])
        if mobile and result_count == 0:
            print('................................................')

            # 数据库获取id
            sql_id = "SELECT one_level,two_level,three_level, keyword  FROM bus_spider_data WHERE  source='材料网' and  TYPE = 'caigou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
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



            # # 公司简介
            summary = ''
            try:
                summary = response.xpath('//*[@id="index-page"]/body/div[3]/div[3]/div[2]/ul/li[6]/span[2]/text()')[0].extract()
                print('summary', summary)
            except:
                print('summary', summary)
            item['summary'] = str(summary)

            # # # 经营范围
            scopes = ''
            try:
                scopes = response.xpath('//*[@id="index-page"]/body/div[3]/div[3]/div[2]/ul/li[7]/span[2]/text()').extract()[0]
                print('scopes', scopes)
            except:
                print('scopes', scopes)
            item['scopes'] = scopes

            # # # 地址
            address = ''
            try:
                address = response.xpath('//span[@class="val"]/text()')[0].extract()
                print('address', address)
            except:
                print('address', address)
            item['address'] = str(address)

            # # # 公司名称
            com_name = ''
            try:
                com_name = response.xpath('//div[@class="member-company fl"]/ul/li[1]/a/text()')[0].extract()
                print('com_name', com_name)
            except:
                print('com_name', com_name)
            item['com_name'] = str(com_name)

            # # `create_date`
            create_date = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
            item['create_date'] = create_date

            # # 商品价格
            price = ''
            try:
                price = response.xpath('//div[@class="price"]/span/text()')[0].extract()
                print('price', price)
            except:
                print('price', price)
            item['price'] = str(price)

            # # `title`,
            res_title = ''
            try:
                res_title = response.xpath('//div[@class="main-data-param fr"]/h1/text()')[0].extract()
                res_title = res_title.strip()
                print('标题：', res_title)
            except:
                print('没有')
            item['title'] = str(res_title)

            # # `way`
            if price != '':
                way = '0'
            else:
                way = '1'
            print('way', way)
            item['way'] = way

            res_detail_html = response.text
            try:
                soup = BeautifulSoup(res_detail_html, 'lxml')
                # detail = soup.select('#main > .main > .pro_list > .pro_content')[0]
                detail = soup.find('div', class_='member-info fr')
                # print('detail', detail)
            except Exception as e:
                raise e
            item['detail'] = str(detail)

            # # # 28. `units`,
            units = ''
            item['units'] = str(units)

            # # 40. `linkman`
            link_man = ''
            try:
                link_man = response.xpath('//div[@class="member-company fl"]/ul/li[3]/a/text()')[0].extract()
                if link_man == '':
                    link_man = '孙经理'
                print('man:', link_man)
            except:
                print('man:', link_man)
            item['linkman'] = str(link_man)

            # # 41. `mobile`,
            mobile = ''
            try:
                mobile = response.xpath('//div[@class="member-company fl"]/ul/li[4]/span[2]/text()')[0].extract()
                print('mobile', mobile)
            except:
                print('mobile', mobile)
            item['mobile'] = str(mobile)

            # # 求购数量
            # # 41. `num`,
            num = '不限'
            try:
                # num = re.findall('<li><b>产品数量：</b>(.*?)</li>', response.text, re.S)[0].strip()
                num = response.xpath('//span[@class="fota"]/text()')[0].extract()
                print('num', num)
            except:
                print('num', num)
            item['num'] = str(num)

            item['list_img'] = ''
            item['imgs'] = ''

            # print('数据完成..')

            # # 随机时间
            days = random.randint(120, 360)

            now = datetime.datetime.now()
            delta = datetime.timedelta(days=days)
            n_days = now + delta
            item['end_time'] = n_days.strftime('%Y-%m-%d %H:%M:%S')
            print(item['end_time'])

            yield item




