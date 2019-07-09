# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import random
import time
import os
import requests
from ..items import SouHaoHuoPag1Item
import pymysql
import re
from bs4 import BeautifulSoup
from lxml import etree

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class GongSiSpider(scrapy.Spider):
    name = 'gong_si'
    num_2 = 1

    def start_requests(self):
        """
        处理初始url
        :return:
        """
        # sql_id = "SELECT url FROM bus_spider_data WHERE TYPE = 'chengxin' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        # cur.execute(sql_id)
        # res_all_list = cur.fetchall()
        # url = res_all_list[0][0]
        # for num in range(1, 2):
        #     url_2 = url.format(num)
        url_2 = 'http://s.912688.com/prod/dy/search?kw=%E5%AE%A0%E7%89%A9%E8%8D%AF%E5%93%81&pageSize=20&page=1'
        yield Request(url=url_2, callback=self.parse_2)

    def parse_2(self, response):
        """
        获取直接进去的产品详情页
        :param response:
        :return:
        """
        li_list_one = response.xpath('//div[@class="product-left-new clearfix"]//li/a/@href')[0].extract()
        yield Request(url=li_list_one, callback=self.parse_3)

    def parse_3(self, response):
        """
        公司详情url和产品列表url
        :param response:
        :return:
        """
        print('parse_3>>>>>>>>>>>>>>>>>')
        con_url = response.xpath('/html/body/div[2]/div[3]/div/ul/li[3]/a/@href')[0].extract()
        print(con_url)
        yield Request(url=con_url, callback=self.parse_c)

    def parse_c(self, response):
        """
        公司详情页解析
        :param response:
        :return:
        """
        item = SouHaoHuoPag1Item()
        com_name = re.findall('<tr.*?公司名称.*?<td.*?>(.*?)</td>', response.text, re.S)[0].strip()
        print(com_name)
        sql_count = "select count(0) from bus_user where company_name='{}'".format(com_name)
        cur.execute(sql_count)
        result = cur.fetchall()
        result_count = int(result[0][0])
        if result_count == 0:

            # 公司简介
            summary = '-'
            try:
                summary = response.xpath('//div[@class="shop-section mb10"]/div[@class="shop-comp-ins textarea-content"]/text()').extract()[0].strip()
                print('summary', summary)
            except:
                print('summary', summary)
            item['summary'] = summary

            # 经营范围
            scopes = '-'
            try:
                scopes = re.findall('<tr.*?经营范围.*?<td.*?>(.*?)</td>', response.text, re.S)[0].strip()
                print('scopes', scopes)
            except:
                print('scopes', scopes)
            item['scopes'] = scopes

            # 地址
            address = '-'
            try:
                address = re.findall('<tr.*?经营地址.*?<td.*?>(.*?)</td>', response.text, re.S)[0].strip()
                print('address', address)
            except:
                print('address', address)
            item['address'] = str(address)

            # 公司名称
            com_name = '-'
            try:
                com_name = re.findall('<tr.*?公司名称.*?<td.*?>(.*?)</td>', response.text, re.S)[0].strip()
                print('com_name', com_name)
            except:
                print('com_name', com_name)
            item['com_name'] = str(com_name)


            # tree = etree.HTML(response.text)
            detail_list_url = response.xpath('/html/body/div[4]/div/ul/li[2]/a/@href')[0].extract()
            # print('detail_list_url', detail_list_url)

            yield Request(url=detail_list_url, callback=self.parse_p_1, meta={'item': item})

        else:
            print('企业重复!!!')

    def parse_p_1(self, response):
        """
        商品详情url
        :param response:
        :return:
        """
        item = response.meta['item']
        pao_deail_url_list = response.xpath('/html/body/div[5]/div[2]/div[2]/div/div[2]/ul[2]/li/div/a/@href').extract()
        for pao_deail_url in pao_deail_url_list:

            # print('pao_deail_url', pao_deail_url)

            yield Request(url=pao_deail_url, callback=self.parse_p_2, meta={'item':item})

    def parse_p_2(self, response):
        """
        商品详情解析
        :param response:
        :return:
        """
        item = response.meta['item']
        item = self.shuju(response, item)
        print('爬取成功>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        yield item


    @staticmethod
    def shuju(response, item):

        # 保存商品图片
        try:
            os_img_1 = []
            str_ran = str(random.randint(0, 999999))
            os_img_1.append(str_ran)
            os.makedirs('/home/imgServer/spiders/{}'.format(str_ran))
            #     将图片链接保存到硬盘
            res_img = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[1]/div[1]/div/ul/li/img/@src')

            os_img_2_list = []
            # os_img_2_list
            for img_url in res_img:
                img_url = img_url.extract()
                img_url = img_url.strip()
                code_img = requests.get(url=img_url).content
                img_name = str(random.randint(1, 999999))
                with open('/home/imgServer/spiders/{}/{}.jpg'.format(str_ran, img_name), 'wb') as f:
                    f.write(code_img)
                os_img_2 = 'http://img.ktcx.cn/spiders/' + '{}/{}.jpg'.format(str_ran, img_name)
                os_img_2_list.append(os_img_2)
            #
            os_img_2_str_1 = os_img_2_list[0]
            os_img_2_str = ','.join(os_img_2_list)
            # item['os_img_2_str_1'] = os_img_2_str_1
            # item['os_img_2_str'] = os_img_2_str

            print('图片ok', os_img_2_list)
        except:
            print('图片错误.')

        # 数据库获取id
        sql_id = "SELECT one_level,two_level,three_level,keyword  FROM bus_spider_data WHERE TYPE = 'chengxin' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
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

        # 2. `create_date`
        create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
        item['create_date'] = create_date

        # 4. `list_img`
        item['list_img'] = str(os_img_2_str_1)

        # 5. `price`
        try:
            price_list = []
            res_price = response.xpath(
                '/html/body/div[3]/div/div[1]/div[2]/div[2]/table//tr[@class="price"]/td[2]/div/span/text()').extract()
            for price in res_price:
                price = price.replace('\r', '').replace('\n', '').replace('\t', '')
                price_list.append(price)
                print('价格', price_list[-1])
        except:
            print('没有')
        item['price'] = str(price_list[-1])

        # 6. `title`,
        try:
            res_title = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/h1/text()')[0].extract()
            print('标题：', res_title)
        except:
            print('没有')
        item['title'] = str(res_title)

        # 7. `way`
        if price_list[-1]:
            way = '0'
        else:
            way = '1'
        item['way'] = way

        # 15. `imgs`
        item['imgs'] = os_img_2_str

        # 23. `detail`
        res_detail_html = response.text
        try:
            soup = BeautifulSoup(res_detail_html, 'lxml')
            html = str(soup.select('#three-data > .table')[0])
            res_delia_HTML = str(soup.find('div', id="prodDetailDiv"))

            a = res_delia_HTML
            strinfo = re.compile('<p style="(.*?)".*?>.*?</p>')
            hh = strinfo.sub('', a)

            d = hh
            strinfo = re.compile('<div class="note">')
            hhh = strinfo.sub('', d)

            e = hhh
            strinfo = re.compile('<br.*?>')
            hhhh = strinfo.sub('', e)

            # b = hhhh
            # strinfo = re.compile('<img.*?src=.*?/>')
            # res_delia_html = strinfo.sub(' ', b)

            hebing_ = str(html) + '<br/><br/>' + str(hhhh)
            # print(hebing_)
        except Exception as e:
            raise e
        item['detail'] = str(hebing_)

        # 28. `units`,
        # res_danwei = '-'
        # try:
        #     res_danwei = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/table//tr[2]/td[2]/div/text()')[0].extract()
        #     print('res_danwei:', res_danwei)
        # except:
        #     print('res_danwei:', res_danwei)
        # item['units'] = str(res_danwei)

        res_danwei = ''
        try:
            res_danwei = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]//tr[2]/td[2]/div/text()')[0].extract().strip()
            res_danwei = res_danwei.replace('\n', '').replace('\t', '')
            print('res_danwei>>>>>>>>>>>>>:', res_danwei)
        except:
            print('res_danwei:', res_danwei)
        item['units'] = str(res_danwei)

        # 39. `com_name`


        # 40. `linkman`
        link_man = '-'
        try:
            link_man = re.findall('<li>.*?联系姓名：</span><a.*?>(.*?)</a></li>', response.text, re.S)[0]
            print('man:', link_man)
        except:
            print('man:', link_man)
        item['linkman'] = str(link_man)

        # 41. `mobile`,
        mobile = ''
        try:
            mobile = response.xpath('/html/body/div[6]/div[5]/div[2]/ul/li[1]/span[3]/text()').extract()[0]
            print(mobile)
        except:
            print('没有')
        item['mobile'] = str(mobile)
        print('数据完成..')

        # return item
# cur.close()
# conn.close()









