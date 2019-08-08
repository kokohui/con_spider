from ..items import TianZhuWangItem
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import os
import random
import pymysql
import time
import re
import requests
from lxml import etree
conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'

    def start_requests(self):
        sql_id = "SELECT url FROM bus_spider_data WHERE source = '天助网' and   TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        url = res_all_list[0][0]
        for num in range(1, 3):
            url_2 = 'http://www.tz1288.com/selloffer/search.html?keyword={}&pageIndex={}'.format(url, num)
            print(url_2)
            yield Request(url=url_2, callback=self.parse)

    def parse(self, response):
        detail_url_list = response.xpath('//*[@id="itemBox"]/li/a/@href').extract()
        for detail_url in detail_url_list:
            yield Request(url=detail_url, callback=self.detail_parse)

    def detail_parse(self, response):

        item = TianZhuWangItem()

        mobile = ''
        result_count = 0
        try:
            mobile = re.findall('<p><strong>电话：</strong><span>(.*?)</span>', response.text, re.S)[0]
            com_name = str(
                response.xpath('//*[@id="companySidebarInfo"]/p/a/text()').extract()[0]).strip()
            sql_count = "select count(0) from bus_user where company_name='{}'".format(com_name)

            cur.execute(sql_count)
            result = cur.fetchall()
            result_count = int(result[0][0])
        except:
            print('没有手机号或公司重复')

        if mobile != '' and result_count == 0:
            print('................................................')

            # 数据库获取id
            sql_id = "SELECT one_level,two_level,three_level,keyword  FROM bus_spider_data WHERE source = '天助网' and  TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
            cur.execute(sql_id)
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

            # 保存商品图片
            os_img_2_list = []
            try:
                str_ran = str(random.randint(0, 999999999))
                os.makedirs('/home/imgServer/img_tian/{}'.format(str_ran))
                #     将图片链接保存到硬盘
                res_img_list_11 = response.xpath('//*[@id="productImagesEnlargement"]/a/@href').extract()

                for img_url in res_img_list_11:
                    img_url = img_url.strip()
                    img_url = re.sub('_100x100', '_800x800', img_url)
                    print('img_url>>>>>>>>>>>>><<<<<<<<<<<<<<<<<::::::', img_url)

                    code_img = requests.get(url=img_url).content
                    img_name = str(random.randint(1, 999999999))
                    with open('/home/imgServer/img_tian/{}/{}.jpg'.format(str_ran, img_name), 'wb') as f:
                        f.write(code_img)
                    os_img_2 = 'http://img.youkeduo.com.cn/img_tian/' + '{}/{}.jpg'.format(str_ran, img_name)
                    os_img_2_list.append(os_img_2)
                os_img_2_str_1 = os_img_2_list[0]
                os_img_2_str = ','.join(os_img_2_list)
                item['list_img'] = os_img_2_str_1
                item['imgs'] = os_img_2_str
                print('图片ok', os_img_2_list)
            except:
                print('图片错误.')


            # 创建时间
            create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
            item['create_date'] = create_date

            # 价格
            price = ''
            try:
                # price = str(response.xpath('//table[@class="prices"]//tr[2]/td[2]/span/text()').extract()[0].strip())
                # if not price:
                price = '电议'
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
                html_1 = str(soup.find('div', class_="pcProDetailInfoList"))
                html = str(soup.find('div', class_="pcProDetailIntro clearfix aline"))

                strinfo = re.compile('<img.*?>')
                html_2 = strinfo.sub('', html)

                strinfo = re.compile('<br.*?>')
                html_3 = strinfo.sub('', html_2)

                strinfo = re.compile('慧聪网')
                html_4 = strinfo.sub('优客多', html_3)
                # 把下载图片添加到html
                div_list = ['<div id="img_detail">', '</div>']
                for os_img_2_url in os_img_2_list:
                    os_img_2_url = '<img alt="{}" src="{}">'.format(title, os_img_2_url)
                    div_list.insert(1, os_img_2_url)
                div_str = '\n'.join(div_list)
                html_all = html_1 + html_4 + '\n' + div_str
            except Exception as e:
                raise e
            item['detail'] = str(html_all)

            # units
            units = ''
            try:
                print('units', units)
            except:
                print('units', units)
            item['units'] = units

            # com_name
            com_name = '个体'
            try:
                com_name = str(
                    response.xpath('//*[@id="companySidebarInfo"]/p/a/text()').extract()[0]).strip()
                print('com_name', com_name)
            except:
                print('com_name', com_name)
            item['com_name'] = com_name

            # linkman
            linkman = ''
            try:
                linkman = response.xpath('//*[@id="companyContacthtml"]/div/dl/dd/ul/li[1]/span/strong/text()').extract()[0]
                print('linkman', linkman)
            except:
                print('linkman', linkman)
            item['linkman'] = linkman

            # mobile
            mobile = ''
            try:
                mobile = re.findall('<p><strong>电话：</strong><span>(.*?)</span>', response.text, re.S)[0]
                print('mobile', mobile)
            except:
                print('mobile', mobile)
            item['mobile'] = mobile

            # address
            address = ''
            try:
                address = re.findall('<p><strong>地址：</strong>(.*?)</p>',response.text)[0]
                print('address', address)
            except:
                print('address', address)
            item['address'] = address

            try:
                com_url = response.xpath('/html/body/div[3]/div[1]/ul/li[2]/a/@href').extract()[0]
                print(com_url)
                self.detail_con(com_url, item)
            except:
                print('没有公司详情')

            yield item

    @classmethod
    def detail_con(self, com_url, item):
        res_text = requests.get(url=com_url).text
        tree = etree.HTML(res_text)

        summary = ''
        try:
            summary = tree.xpath('/html/body/div[4]/div[2]/div[1]/div[2]/div[2]/text()')[0].strip()
            print('summary>>>>>>>>>>>>>>>', summary)
        except:
            print('summary', summary)
        item['summary'] = summary

        scopes = '-'
        try:
            scopes = tree.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[1]/td[2]/text()')[0]
            print('scopes', scopes)
        except:
            print('scopes', scopes)
        item['scopes'] = scopes

