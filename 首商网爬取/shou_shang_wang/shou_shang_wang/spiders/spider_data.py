import scrapy
from scrapy import Request
import re
import random
import os
import requests
import time
from bs4 import BeautifulSoup
from ..items import ShouShangWangItem
import pymysql
import datetime

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'
    # start_urls = ['http://www.sooshong.com/s-5-189p2']

    def start_requests(self):
        """初始url"""
        sql_id = "SELECT url FROM bus_spider_data WHERE TYPE = 'qiugou' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        # url = res_all_list[0][0]
        # url = 'http://www.sooshong.com/s-5-189p{}'
        url = 'http://so.sooshong.com/sale/search.jsp?offset={}0&rows=10&keywords=%E7%94%B5%E8%84%91&searchby=0&sortby=0&beforafter=1&days=180&categoryid=0&b2b=0&searchandor=0'
        for num in range(1, 2):
            start_url = url.format(str(num))
            # start_url = 'http://www.sooshong.com/s-5-189p2'

            yield Request(url=start_url, callback=self.parse)

    def parse(self, response):
        res_list_li = response.xpath('//div[@class="list_li"]/ul/li//div[@class="title"]/a/@href')
        for res_li in res_list_li:
            res_li = 'http://www.sooshong.com' + res_li.extract()
            yield Request(url=res_li, callback=self.parse_2)

    def parse_2(self, response):

        item = ShouShangWangItem()

        mobile = re.findall('<p><b>手机：</b><strong>(.*?)</strong></p>', response.text, re.S)[0].strip()
        # 查询公司存储个数, 如果没有则存储~
        com_name = re.findall('<p><b>企业名称：</b>(.*?)</p>', response.text, re.S)[0].strip()
        sql_count = "select count(0) from bus_user where company_name='{}'".format(com_name)
        cur.execute(sql_count)
        result = cur.fetchall()
        result_count = int(result[0][0])
        if mobile and result_count == 0:
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

            # # 公司简介
            summary = '-'
            try:
                summary = response.xpath('//div[@class="pro_content"]//text()').extract()
                summary = ''.join(summary).strip().replace('\t', '').replace('\n', '').replace('\r', '')
                print('summary', summary)
            except:
                print('summary', summary)
            item['summary'] = str(summary)

            # # # 经营范围
            scopes = '-'
            try:
                scopes = response.xpath('//*[@id="main"]/div[2]/div[4]/ul/p/text()').extract()[0]
                print('scopes', scopes)
            except:
                print('scopes', scopes)
            item['scopes'] = scopes

            # # # 地址
            address = '-'
            try:
                address = re.findall(r'<p><b>联系地址：</b>(.*?)</p>', response.text, re.S)[0]
                print('address', address)
            except:
                print('address', address)
            item['address'] = str(address)

            # # # 公司名称
            com_name = '-'
            try:
                com_name = re.findall('<p><b>企业名称：</b>(.*?)</p>', response.text, re.S)[0].strip()
                # com_name = response.xpath('/html/body/div[@class="com_nav divc"]/div[@class="comname fl"]/a/@title').extract()[0]

                print('com_name', com_name)
            except:
                print('com_name', com_name)
            item['com_name'] = str(com_name)

            # # `create_date`
            create_date = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
            item['create_date'] = create_date

            # # 商品价格
            try:
                price_list = []
                res_price = re.findall('<li><b>价格说明：</b>(.*?)</li>', response.text, re.S)
                for price in res_price:
                    price = price.replace('\r', '').replace('\n', '').replace('\t', '').strip()
                    price_list.append(price)
                    print('价格........', price_list[-1])
            except:
                print('没有')
            item['price'] = str(price_list[-1])

            # # `title`,
            res_title = '-'
            try:
                res_title = response.xpath('//div[@class="pro_infos"]/h1/text()')[0].extract()
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

            res_detail_html = response.text
            try:
                soup = BeautifulSoup(res_detail_html, 'lxml')
                detail = soup.select('#main > .main > .pro_list > .pro_content')[0]
                # print('detail', detail)
            except Exception as e:
                raise e
            item['detail'] = str(detail)

            # # 28. `units`,
            units = ''
            item['units'] = str(units)

            # # 40. `linkman`
            link_man = '-'
            try:
                link_man = re.findall('<p><b>联系人：</b> <em>(.*?)</em>.*?</p>', response.text, re.S)[0]
                if link_man == '':
                    link_man = '孙经理'
                print('man:', link_man)
            except:
                print('man:', link_man)
            item['linkman'] = str(link_man)

            # # 41. `mobile`,
            mobile = ''
            try:
                mobile = re.findall('<p><b>手机：</b><strong>(.*?)</strong></p>', response.text, re.S)[0].strip()
                print('mobile', mobile)
            except:
                print('mobile', mobile)
            item['mobile'] = str(mobile)

            # # 求购数量
            # # 41. `num`,
            num = 0
            try:
                num = re.findall('<li><b>产品数量：</b>(.*?)</li>', response.text, re.S)[0].strip()
                if num  == '不限':
                    num = 0
                print('num', num)
            except:
                print('num', num)
            item['num'] = num

            item['list_img'] = ''
            item['imgs'] = ''

            print('数据完成..')

            # # 随机时间
            days = random.randint(120, 360)

            now = datetime.datetime.now()
            delta = datetime.timedelta(days=days)
            n_days = now + delta
            item['end_time'] = n_days.strftime('%Y-%m-%d %H:%M:%S')
            print(item['end_time'])

            # return item


# 'http://so.sooshong.com/sale/search.jsp?offset=20&rows=10&keywords=%E7%94%B5%E8%84%91&searchby=0&sortby=0&beforafter=1&days=180&categoryid=0&b2b=0&searchandor=0'
# 'http://so.sooshong.com/sale/search.jsp?offset=30&rows=10&keywords=%E7%94%B5%E8%84%91&searchby=0&sortby=0&beforafter=1&days=180&categoryid=0&b2b=0&searchandor=0'
# 'http://so.sooshong.com/sale/search.jsp?offset=10&rows=10&keywords=%E9%9E%8B%E5%AD%90&searchby=0&sortby=0&beforafter=1&days=180&categoryid=0&b2b=0&searchandor=0'