# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
from ..items import ChuanZhongItem


class HuangYeSpider(scrapy.Spider):
    name = 'huang_ye'
    # allowed_domains = ['http://www.czvv.com/jichuang/']
    # start_urls = ['http://http://www.czvv.com/jichuang//']
    url = 'http://www.czvv.com/zhongshanzhuangtangzhuangminzufuzhuang/'

    def start_requests(self):

        start_url = self.url
        print(start_url)
        time.sleep(1)
        yield Request(url=start_url, callback=self.parse_url)

        try:
            for num in range(2, 11):
                start_url = self.url + '{}'.format(num)
                print(start_url)
                time.sleep(1)
                yield Request(url=start_url, callback=self.parse_url)
        except:
            print('没有')


    def parse_url(self, respose):
        print('parse_url:>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        try:
            url_list = respose.xpath(
                '//*[@id="Thebox"]/div[@class="container"]/div[@class="inbox"]/div[@class="leftblock"]/div[@class="company-mesage"]')
            for url_p in url_list:
                url_p = url_p.xpath('./div[@class="row right"]/a/@href').extract()[0]
                print(url_p)
                time.sleep(2)
                yield Request(url=url_p, callback=self.parse)
        except:
            print('url_list出错')

    def parse(self, response):
        print('parse:>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        res_text = response.text
        item = ChuanZhongItem()

        # 4.手机号
        tel = '-'
        try:
            tel = re.findall('<span.*?手机：</span>(.*?)</span>', res_text, re.S)[0]
            print(tel)
        except:
            print(tel)
        if tel == '-':
            pass
        else:


            # 1.公司名称
            title = '-'
            try:
                title = response.xpath('//*[@id="content"]/div/div/div[1]/div[1]/h2/text()').extract()[0]
                print(title)
            except:
                print(title)
            item['title'] = title

            # 2.企业简介
            brief = '-'
            try:
                brief = response.xpath('//*[@id="aboutbox"]/div[@class="word"]/div/text()').extract()
                brief = ''.join(brief).replace(' ', '').replace('\t', '').strip()
                print(brief)
            except:
                print(brief)
            item['brief'] = brief


            # 3.联系人
            man = '-'
            try:
                man = re.findall('<span.*?联系人：</span>(.*?)</span>', res_text, re.S)[0]
                print(man)
            except:
                print(man)
            item['man'] = man

            # 4.手机号
            tel = '-'
            try:
                tel = re.findall('<span.*?手机：</span>(.*?)</span>', res_text, re.S)[0]
                print(tel)
            except:
                print(tel)
            item['tel'] = tel

            # 5.电话
            tel_2 = '-'
            try:
                tel_2 = re.findall('<span.*?电话：</span>(.*?)</span>', res_text, re.S)[0]
                print(tel_2)
            except:
                print(tel_2)
            item['tel_2'] = tel_2


            # 6.传真
            fax = '-'
            try:
                fax = re.findall('<span.*?传真：</span>(.*?)</span>', res_text, re.S)[0]
                print(fax)
            except:
                print(fax)
            item['fax'] = fax

            # 7.qq
            tel_qq = '-'
            try:
                tel_qq = re.findall('<span.*?QQ：</span>(.*?)</span>', res_text, re.S)[0]
                print(tel_qq)
            except:
                print(tel_qq)
            item['tel_qq'] = tel_qq

            # 8.邮编
            post_code = '-'
            try:
                post_code = re.findall('<span.*?邮编：</span>(.*?)</span>', res_text, re.S)[0]
                print(post_code)
            except:
                print(post_code)
            item['post_code'] = post_code

            # 9.注册资金
            register = '-'
            try:
                register = re.findall('<span.*?注册资金：</span>(.*?)</span>', res_text, re.S)[0].replace(' ', '').replace('\n', '').strip()
                print(register)
            except:
                print(register)
            item['register'] = register

            # 10.商铺
            ad_url = '-'
            try:
                ad_url = re.findall('<span.*?商铺.*?href="(.*?)".*?</a>', res_text, re.S)[0]
                print(ad_url)
            except:
                print(ad_url)
            item['ad_url'] = ad_url

            # 11.地址
            addres = '-'
            try:
                addres = re.findall('<span.*?地址：</span>(.*?)</span>', res_text, re.S)[0]
                print(addres)
            except:
                print(addres)
            item['addres'] = addres

            # 12.营业状态
            forms = '-'
            try:
                forms = re.findall('<div.*?经营状态.*?<div.*?>(.*?)</div>', res_text, re.S)[0]
                print(forms)
            except:
                print(forms)
            item['forms'] = forms

            # 13.成立时间
            com_time = '-'
            try:
                com_time = re.findall('<div.*?成立日期：.*?<div.*?>(.*?)</div>', res_text, re.S)[0]
                print(com_time)
            except:
                print(com_time)
            item['com_time'] = com_time


            # 14.公司类型
            com_type = '-'
            try:
                com_type = re.findall('<div.*?公司类型：.*?<div.*?>(.*?)</div>', res_text, re.S)[0]
                print(com_type)
            except:
                print(com_type)
            item['com_type'] = com_type

            # 15.征信
            zheng_xin = '-'
            try:
                zheng_xin = re.findall('<div.*?传众征信：.*?<div.*?><a.*?href="(.*?)".*?target="_blank">.*?</a></div>', res_text, re.S)[0]
                print(zheng_xin)
            except:
                print(zheng_xin)
            item['zheng_xin'] = zheng_xin

            # 16.经营范围
            scope = '-'
            try:
                scope = response.xpath('//*[@id="job"]/p/text()').extract()
                scope = ''.join(scope).replace(' ', '').replace('\t', '').replace('\n', '').strip()
                print(scope)
            except:
                print(scope)
            item['scope'] = scope

            # 17.公司类型
            product = '-'
            try:
                product = response.xpath('//*[@id="product"]/div[2]//text()').extract()
                product = ''.join(product).replace(' ', '').replace('\t', '').replace('\n', '').strip()
                print(product)
            except:
                print(product)
            item['product'] = product


            time.sleep(2)
            return item



