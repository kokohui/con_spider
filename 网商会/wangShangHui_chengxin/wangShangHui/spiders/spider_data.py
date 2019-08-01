# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import WangshanghuiItem
import time
import datetime
import random
import re
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'

    # start_urls = ['http://so.7wsh.com/?page=1&kw=%E6%89%8B%E6%9C%BA&type=buy']

    def start_requests(self):
        sql_id = "SELECT url,id FROM bus_spider_data WHERE  source='网商汇' and TYPE = 'caigou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        url_pag = res_all_list[0][0]
        for num in range(1, 20):
            url = url_pag.format(num)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        detail_url = response.xpath('/html/body/div[4]/div[3]/div[1]/ul/li/dl/dd[1]/h3/a/@href')[0]

        yield Request(url=detail_url, callback=self.detail_url)

    def detail_url(self, response):
        item = WangshanghuiItem()

        mobile = response.xpath('//span[@id="spanPhone"]/text()')[0].extract()
        # 查询公司存储个数, 如果没有则存储~
        com_name = response.xpath('//h3[@id="spanCompany"]/text()')[0].extract()
        sql_count = "select count(0) from bus_user where company_name='{}'".format(com_name)
        cur.execute(sql_count)
        result = cur.fetchall()
        result_count = int(result[0][0])
        if mobile and result_count == 0:
            print('................................................')

            # 数据库获取id
            sql_id = "SELECT one_level,two_level,three_level, keyword  FROM bus_spider_data WHERE  source='网商汇' and  TYPE = 'caigou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
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

            # # # 经营范围
            scopes = ''
            try:
                scopes = response.xpath('/html/body/div[4]/div[3]/div[2]/div[2]/dl/dd[1]/span[4]/text()').extract()[0]
                print('scopes', scopes)
            except:
                print('scopes', scopes)
            item['scopes'] = scopes

            # # # 地址
            address = ''
            try:
                address = \
                re.findall('<dd><span class="in_gray">联系地址</span><span id="spanadress">(.*?)</span>', response.text,
                           re.S)[0]
                print('address', address)
            except:
                print('address', address)
            item['address'] = str(address)

            # # # 公司名称
            com_name = ''
            try:
                com_name = response.xpath('//h3[@id="spanCompany"]/text()')[0].extract()
                print('com_name', com_name)
            except:
                print('com_name', com_name)
            item['com_name'] = str(com_name)

            # # `create_date`
            create_date = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
            item['create_date'] = create_date

            # # 商品价格
            price = '面议'
            try:
                price = response.xpath('//span[@class="itemPrice"]/text()')[0].extract()
                print('price', price)
            except:
                print('price', price)
            item['price'] = str(price)

            # # `title`,
            res_title = ''
            try:
                res_title = response.xpath('/html/body/div[4]/div[3]/div[2]/div[1]/div/h3/span/text()')[0].extract()
                res_title = res_title.strip()
                print('标题：', res_title)
            except:
                print('没有')
            item['title'] = str(res_title)

            # # `way`
            if price != '面议':
                way = '0'
            else:
                way = '1'
            print('way', way)
            item['way'] = way

            res_detail_html = response.text
            try:
                soup = BeautifulSoup(res_detail_html, 'lxml')
                # detail = soup.select('#main > .main > .pro_list > .pro_content')[0]
                detail = soup.find('div', class_='introduce')
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
                link_man = response.xpath('//span[@id="spanRealName"]/text()')[0].extract()
                if link_man == '':
                    link_man = '孙经理'
                print('man:', link_man)
            except:
                print('man:', link_man)
            item['linkman'] = str(link_man)

            # # 41. `mobile`,
            mobile = ''
            try:
                mobile = response.xpath('//span[@id="spanPhone"]/text()')[0].extract()
                print('mobile', mobile)
            except:
                print('mobile', mobile)
            item['mobile'] = str(mobile)

            # # 求购数量
            # # 41. `num`,
            num = '不限'
            try:
                # num = re.findall('<li><b>产品数量：</b>(.*?)</li>', response.text, re.S)[0].strip()
                # num = response.xpath('//span[@class="fota"]/text()')[0].extract()
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

            # 公司详情url
            con_url = ''
            try:
                con_url = response.xpath('/html/body/div[4]/div[3]/div[2]/div[3]/div[1]/ul/li[1]/a/@href')[0].extract()
                print('con_url', con_url)
            except Exception as e:
                print(e)

            yield Request(url=con_url, callback=self.con_parse, meta={'item': item})

    def con_parse(self, response):
        item = response.meta['item']
        # # 公司简介
        summary = ''
        try:
            summary = response.xpath('//div[@class="company_introduce_descript"]/p/text()')[0].extract()
            print('summary', summary)
        except:
            print('summary', summary)
        item['summary'] = str(summary)

        yield item
