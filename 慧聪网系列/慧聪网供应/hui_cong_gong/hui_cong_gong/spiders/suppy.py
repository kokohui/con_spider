# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import re
from ..items import HuiCongGongItem
import os
import random
import requests
import pymysql
import time
from lxml import etree
import re
from time import sleep

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SuppySpider(scrapy.Spider):
    name = 'suppy'

    def start_requests(self):

        sql_id = "SELECT url FROM bus_spider_data WHERE source = '慧聪网' and   TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        url = res_all_list[0][0]
        for num in range(1, 11):
            url_2 = url.format(num)
            print(url_2)
            yield Request(url=url_2, callback=self.parse_1)

    def parse_1(self, response):
        """
        获取商品详情页url
        """
        item = HuiCongGongItem()
        try:
            res_li_list = response.xpath('//div[@class="wrap-grid"]//li[@class="grid-list"]')

            for res_li in res_li_list:
                res_url = 'https:' + res_li.xpath('./div[@class="NewItem"]/div[@class="picmid pRel"]/a/@href')[0].extract()
                print('res_url', res_url)
                yield Request(url=res_url, callback=self.parse_2, meta={'item': item})
        except:
            print('此res_li_list没有解析到~~')

    def parse_2(self, respone):
        """
        获取商品详情页信息
        :param respone:
        :return:
        """
        item = respone.meta['item']

        mobile = ''
        com_url = ''
        result_count = 0
        try:
            mobile = respone.xpath('//*[@id="dialogCorMessage"]/div[@class="p tel2"]/em/text()').extract()[0]
            mobile = mobile[1:]

            com_url = respone.xpath('/html/body/div[7]/div/table/tbody/tr/td[5]/a/@href')[0].extract()

            com_name = str(respone.xpath('//*[@id="dialogCorMessage"]/div[@class="p sate"]/em/text()').extract()[0])
            com_name = com_name[1:]
            sql_count = "select count(0) from bus_user where company_name='{}'".format(com_name)
            cur.execute(sql_count)
            result = cur.fetchall()
            result_count = int(result[0][0])
        except:
            print('没有手机号或公司重复')

        if mobile != '' and com_url != '' and result_count == 0:
            print('................................................')

            # 数据库获取id
            sql_id = "SELECT one_level,two_level,three_level,keyword  FROM bus_spider_data WHERE source = '慧聪网' and  TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
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

            # 保存商品图片
            os_img_2_list = []
            try:
                str_ran = str(random.randint(0, 999999))
                os.makedirs('/home/imgServer/hc/{}'.format(str_ran))
                #     将图片链接保存到硬盘
                res_img = respone.xpath('//*[@id="thumblist"]/li/div/a/img/@src')
                for img_url in res_img:
                    img_url = img_url.extract()
                    # img_url = 'https:' + img_url.strip().replace('..100x100.jpg', '')
                    img_url = 'https:' + img_url.strip()
                    img_url = re.sub('\.\.\d+x\d+.jpg', '', img_url)
                    print('img_url>>>>>>>>>>>>><<<<<<<<<<<<<<<<<::::::', img_url)


                    code_img = requests.get(url=img_url).content
                    img_name = str(random.randint(1, 999999))
                    with open('/home/imgServer/hc/{}/{}.jpg'.format(str_ran, img_name), 'wb') as f:
                        f.write(code_img)
                    os_img_2 = 'http://img.youkeduo.com.cn/hc/' + '{}/{}.jpg'.format(str_ran, img_name)
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
                price = str(respone.xpath('//*[@id="oriPriceTop"]/text()').extract()[0].strip())
                if price.startswith('¥'):
                    price = price[1:]
                if not price:
                    price = '面议'
                print('price', price)
            except:
                print('price', price)
            item['price'] = price

            # 标题
            title = ''
            try:
                title = str(respone.xpath('//*[@id="comTitle"]/text()').extract()[0])
                # title = title[1:]
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

            # detail详情
            res_detail_html = respone.text
            try:
                soup = BeautifulSoup(res_detail_html, 'lxml')
                html = str(soup.find('div', id="pdetail"))
                # print(html)

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
                html_all = html_4 + '\n' + div_str
            except Exception as e:
                raise e
            item['detail'] = str(html_all)

            # units
            units = ''
            try:
                units = re.findall('<em class="number"> | 共<i id="totalNumber">.*?</i>(.*?)</em>', respone.text, re.S)[
                    -1]
                if not units:
                    units = ''
                print('units', units)
            except:
                print('units', units)
            item['units'] = units

            # com_name
            com_name = ''
            try:
                com_name = str(respone.xpath('//*[@id="dialogCorMessage"]/div[@class="p sate"]/em/text()').extract()[0])
                com_name = com_name[1:]
                print('com_name', com_name)
            except:
                print('com_name', com_name)
            item['com_name'] = com_name

            # linkman
            linkman = ''
            try:
                linkman = respone.xpath('//*[@id="dialogCorMessage"]/div[@class="p name"]/em/text()').extract()[0]
                linkman = str(linkman[1:]).replace(u'\xa0', u' ')
                print('linkman', linkman)
            except:
                print('linkman', linkman)
            item['linkman'] = linkman

            # mobile
            mobile = ''
            try:
                mobile = respone.xpath('//*[@id="dialogCorMessage"]/div[@class="p tel2"]/em/text()').extract()[0]
                mobile = mobile[1:]
                # if not mobile:
                #     mobile = '_'
                print('mobile', mobile)
            except:
                print('mobile', mobile)
            item['mobile'] = mobile

            # address
            address = ''
            try:
                address = respone.xpath('//*[@id="dialogCorMessage"]/div[@class="p sate"]/em/text()').extract()[0]
                address = address[1:]
                print('address', address)
            except:
                print('address', address)
            item['address'] = address

            # 公司url
            try:
                com_url = respone.xpath('/html/body/div[7]/div/table/tbody/tr/td[5]/a/@href')[0].extract()
                print('com_url.........', com_url)
                self.parse_con(com_url, respone, item)

            except:
                print('此公司url错误')

            yield item

    @staticmethod
    def parse_con(com_url, response, item):
        """
        获取部分企业信息
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        response_text = requests.get(url=com_url, headers=headers).text
        tree = etree.HTML(response_text)

        summary = ''
        try:
            summary = tree.xpath('/html/body/div[4]/div/div[2]/div/div[3]/div[2]/p/text()')[0]
            print('summary', summary)
        except:
            print('summary', summary)
        item['summary'] = summary

        scopes = '-'
        try:
            scopes = tree.xpath('//div[@class="profileTab"]/table//tr[1]/td[1]/a/text()')
            scopes = str(scopes).strip('[').strip(']').replace("'", "")
            if not scopes:
                scopes = '-'
            print('scopes', scopes)
        except:
            print('scopes', scopes)
        item['scopes'] = scopes
