# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import re
from ..items import HuiCongGongItem
import os
import random
import requests
from time import sleep


class SuppySpider(scrapy.Spider):
    name = 'suppy'

    def start_requests(self):
        """初始url"""
        start_url = 'https://s.hc360.com/seller/search.html?kwd=%E6%9C%8D%E8%A3%85&c=&F=&G=&nselect=1&pnum=1&ee=2'
        yield Request(url=start_url, callback=self.parse)

    def parse(self, response):
        """
        获取商品详情页url
        :param response:
        :return:
        """
        res_li_list = response.xpath('//div[@class="wrap-grid"]//li[@class="grid-list"]')
        for res_li in res_li_list:
            res_url = 'https:' + res_li.xpath('./div[@class="NewItem"]/div[@class="picmid pRel"]/a/@href')[0].extract()
            yield Request(url=res_url, callback=self.parse_2)

    def parse_2(self, respone):
        """
        获取商品详情页信息
        :param respone:
        :return:

        """
        item = HuiCongGongItem()
        # # 保存商品图片
        try:
            os_img_1 = []
            str_ran = str(random.randint(0, 999999))
            os_img_1.append(str_ran)
            os.makedirs('/home/imgServer/spiders/{}'.format(str_ran))
            #     将图片链接保存到硬盘
            res_img = respone.xpath('//*[@id="thumblist"]/li/div/a/img/@href')
            print(res_img)

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
            item['list_img'] = os_img_2_str_1
            item['imgs'] = os_img_2_str

            print('图片ok', os_img_2_list)
        except:
            print('图片错误.')


        create_date = scrapy.Field()  # 创建时间
        item['create_date'] = create_date

        # list_img = scrapy.Field()  # 图片1

        #价格
        price = '-'
        try:
            price = respone.xpath('//*[@id="oriPriceTop"]/text()').extract()[0]
            price = price.strip()
            if not price:
                price = '-'
            print('price', price)
        except:
            print('price', price)
        item['price'] = price

        # 标题
        title = '-'
        try:
            title = respone.xpath('//*[@id="comTitle"]/text()').extract()[0]
            print('title', title)
        except:
            print('title', title)
        item['title'] = title

        # way
        if price != '-':
            way = '0'
        else:
            way = '1'
        item['way'] = way


        # one_level_id = scrapy.Field()  # 一级id
        # two_level_id = scrapy.Field()  # 二级id
        # three_level_id = scrapy.Field()  # 三级id
        # keywords = scrapy.Field()
        # imgs = scrapy.Field()

        # detail详情
        res_detail_html = respone.text
        try:
            soup = BeautifulSoup(res_detail_html, 'lxml')
            html = str(soup.find('div', id="pdetail"))
            # print(html)

        except Exception as e:
            raise e
        item['detail'] = str(html)

        # units = scrapy.Field()
        units = '-'
        try:
            units = re.findall('<em class="number"> | 共<i id="totalNumber">.*?</i>(.*?)</em>', respone.text, re.S)[-1]
            if not units:
                units = '_'
            print('units', units)
        except:
            print('units', units)
        item['units'] = units


        # com_name
        com_name = '-'
        try:
            com_name = respone.xpath('//*[@id="dialogCorMessage"]/div[@class="p sate"]/em/text()').extract()[0]
            print('com_name', com_name)
        except:
            print('com_name', com_name)
        item['com_name'] = com_name

        # linkman = scrapy.Field()
        linkman = '-'
        try:
            linkman = respone.xpath('//*[@id="dialogCorMessage"]/div[@class="p name"]/em/text()').extract()[0]
            print('linkman', linkman)
        except:
            print('linkman', linkman)
        item['linkman'] = linkman

        # mobile = scrapy.Field()
        mobile = '-'
        try:
            mobile = respone.xpath('//*[@id="dialogCorMessage"]/div[@class="p tel2"]/em/text()').extract()[0]
            mobile = mobile.replace(':', '')
            # if not mobile:
            #     mobile = '_'
            print('mobile', mobile)
        except:
            print('mobile', mobile)
        item['mobile'] = mobile

        # address
        address = '-'
        try:
            address = respone.xpath('//*[@id="dialogCorMessage"]/div[@class="p sate"]/em/text()').extract()[0]
            address = address.replace(':', '')
            print('address', address)
        except:
            print('address', address)
        item['address'] = address

        # 公司url
        com_url = respone.xpath('/html/body/div[7]/div/table/tbody/tr/td[5]/a/@href')[0].extract()
        print('com_url.........', com_url)
        yield Request(url=com_url, callback=self.parse_con, meta={'item': item})

    def parse_con(self, response):
        """
        获取部分企业信息
        :param response:
        :return:
        """
        item = response.meta['item']
        summary = '-'
        try:
            summary = response.xpath('/html/body/div[4]/div/div[2]/div/div[3]/div[2]/p/text()')[0].extract()
            print('summary', summary)
        except:
            print('summary', summary)
        item['summary'] = summary

        scopes = '-'
        try:
            scopes = response.xpath('//div[@class="profileTab"]/table//tr[1]/td[1]/text()')[0].extract()
            scopes = re.findall('<a href=".*?" onmousedown=".*?" target="_blank" style="font-family: ">(.*?)</a>', response.text, re.S)
            scopes = str(scopes).strip('[').strip(']')
            if not scopes:
                scopes = '-'
            print('scopes', scopes)
        except:
            print('scopes', scopes)
        item['scopes'] = scopes

        sleep(1)

