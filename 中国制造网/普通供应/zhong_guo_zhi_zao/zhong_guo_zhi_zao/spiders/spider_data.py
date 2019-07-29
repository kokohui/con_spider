from ..items import ZhongGuoZhiZaoItem
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import os
import random
import pymysql
import time
import re
import requests
import jieba.analyse
from lxml import html
import json

etree = html.etree
conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'

    def start_requests(self):
        sql_id = "SELECT url FROM bus_spider_data WHERE source = '中国制造网' and   TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        url = res_all_list[0][0]
        for num in range(1, 3):
            url_2 = 'https://cn.made-in-china.com/market/{}-{}.html'.format(url, num)
            print(url_2)
            yield Request(url=url_2, callback=self.parse)

    def parse(self, response):
        detail_url_list = response.xpath('//*[@id="inquiryForm"]/li/div[1]/div[1]/div/div/div/a/@href')
        for detail_url in detail_url_list:
            detail_url = detail_url.extract()
            yield Request(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = ZhongGuoZhiZaoItem()

        mobile = ''
        result_count = 0
        try:
            mobile = response.xpath('//ul[@class="contactInfo"]/li[2]/strong[1]/text()').extract()[0].strip()
            com_name = str(response.xpath('//div[@class="company-info"]/div[@class="company-hd clear"]/h2/text()').extract()[0]).strip()
            sql_count = "select count(0) from bus_user where company_name='{}'".format(com_name)
            cur.execute(sql_count)
            result = cur.fetchall()
            result_count = int(result[0][0])
        except:
            print('没有手机号或公司重复')

        if mobile != '' and result_count == 0:
            print('................................................')

            # 数据库获取id
            sql_id = "SELECT one_level,two_level,three_level,keyword  FROM bus_spider_data WHERE source = '中国制造网' and  TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
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

                # keywords = res_all[-1]
                # item['keywords'] = str(keywords)



            # 保存商品图片
            os_img_2_list = []
            try:
                str_ran = str(random.randint(0, 999999))
                os.makedirs('/home/imgServer/hc/{}'.format(str_ran))
                #     将图片链接保存到硬盘

                res_img_list_11 = response.xpath('//div[@class="big-pic"]/a//img/@src').extract()
                if res_img_list_11 == []:
                    for img_num in range(0, 6):
                        res_img = response.xpath('//*[@id="small_{}"]/img/@src'.format(img_num))[0].extract()
                        res_img_list_11.append(res_img)

                for img_url in res_img_list_11:
                    img_url = img_url.strip()
                    img_url = re.sub('_100x100', '_800x800', img_url)
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
                price = str(response.xpath('//table[@class="prices"]//tr[2]/td[2]/span/text()').extract()[
                                0].strip())
                if not price:
                    price = '面议'
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

            # 关键字
            keywords_all_data = '-'
            try:
                setence = title
                keywords = jieba.analyse.extract_tags(setence, topK=30, withWeight=True, allowPOS=('n', 'nr', 'ns'))
                keywords_1 = keywords[0][0]
                keywords_2 = keywords[1][0]
                keywords_all = keywords_1 + ',' + keywords_2
                keywords_all_data = [{"id": 0, "keyword": "{}".format(keywords_all)}]
                print('keywords', keywords_all)
            except:
                print('没有提取到关键字')
            item['keywords'] = json.dumps(keywords_all_data)



            # way
            if price != '':
                way = '0'
            else:
                way = '1'
            item['way'] = way

            res_detail_html = response.text
            try:
                soup = BeautifulSoup(res_detail_html, 'lxml')
                html = str(soup.find('div', class_="description"))
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
                # print(html_all)
            except Exception as e:
                raise e
            item['detail'] = str(html_all)

            # units
            units = ''
            try:
                units = response.xpath('//table[@class="prices"]//tr[1]/th[1]/text()').extract()[0]
                units = re.findall('.*?（(.*?)）', units, re.S)[0]
                print('units', units)
            except:
                print('units', units)
            item['units'] = units

            # com_name
            com_name = '个体'
            try:
                com_name = str(response.xpath('//div[@class="company-info"]/div[@class="company-hd clear"]/h2/text()').extract()[0]).strip()
                print('com_name', com_name)
            except:
                print('com_name', com_name)
            item['com_name'] = com_name

            # linkman
            linkman = ''
            try:
                linkman_1 = response.xpath('//ul[@class="contactInfo"]/li[1]/strong/text()').extract()[0]
                linkman_2 = response.xpath('//ul[@class="contactInfo"]/li[1]/text()').extract()[-1]
                linkman_2 = re.findall(r'[\u4e00-\u9fa5]+', linkman_2, re.S)[0]
                linkman = linkman_1 + linkman_2
                print('linkman', linkman)
            except:
                print('linkman', linkman)
            item['linkman'] = linkman

            # mobile
            mobile = ''
            try:
                mobile = response.xpath('//ul[@class="contactInfo"]/li[2]/strong[1]/text()').extract()[0].strip()
                print('mobile', mobile)
            except:
                print('mobile', mobile)
            item['mobile'] = mobile

            # address
            address = ''
            try:
                address = re.findall('<li><span class="contact-tit">地址：</span> <span class="contact-bd">(.*?)</span> </li>', response.text)[0]
                print('address', address)
            except:
                print('address', address)
            item['address'] = address

            summary = ''
            try:
                summary = response.xpath('//div[@class="company-info"]/p/span/text()').extract()[0]
                print('summary>>>>>>>>>>>>>>>', summary)
            except:
                print('summary', summary)
            item['summary'] = summary

            try:
                com_url = 'https:' + response.xpath('//ul[@class="top_nav"]/li[5]/a/@href').extract()[0]
                print(com_url)
                self.detail_con(com_url, item)
            except:
                print('没有公司详情')

            yield item

    @classmethod
    def detail_con(self, com_url, item):
        res_text = requests.get(url=com_url).text
        scopes = '-'
        try:
            scopes = re.findall('<th>业务范围：</th>.*?<td>(.*?)</td>', res_text, re.S)[0]
            print('scopes', scopes)
        except:
            print('scopes', scopes)
        item['scopes'] = scopes

