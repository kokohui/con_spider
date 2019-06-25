# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import random
import time
import os
import requests
from ..items import SouHaoHuoItem
import pymysql
import re
import json
from bs4 import BeautifulSoup

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class DianShangSpider(scrapy.Spider):
    name = 'dian_shang'

    d_id_3 = '185'
    keywords_name = '大码女装'
    start_url = 'http://www.912688.com/chanpin/59277801597388C5-orderBymultiple-aoddesc-viewlist-page{}.html'
    num_2 = 1


    def start_requests(self):
        for num in range(2, 100):
            start_url = self.start_url.format(str(num))
            print('开始爬取第{}条数据'.format(num))
            yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        product_url_list = response.xpath( '//div[@class="product-left-new clearfix"]/ul/li/div[@class="clearfix"]/div[@class="sm-list-l-img-new"]/a/@href')
        for product_url in product_url_list:
            product_url = product_url.extract()
            yield scrapy.Request(url=str(product_url), callback=self.parse_detail)

    def parse_detail(self, response):
        print('parse_detail>>>>>')
        # print('------------------------',response.text)\\
        item = SouHaoHuoItem()

        # `com_name`, \
        try:
            res_dizhi = response.xpath('/html/body/div[5]/div[5]/div[2]/ul/li[4]/span[3]/text()')[0].extract()
            # print('res_dizhi', res_dizhi)
        except:
            print('没有')
        # str(res_dizhi)

        # 执行查询sql语句
        try:
            # 执行sql语句，进行查询
            sql = "SELECT COUNT(0) FROM bus_product WHERE three_level_id = '{}' AND com_name = '{}'AND is_del = '0'".format(
                self.d_id_3, str(res_dizhi))
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
                print('爬--------------------------------------')
                shuju(response, item, d_id_3_3, keywords_name_2)
                print('恭喜您,爬取{}成功,真是太厉害了!!!!!!'.format(self.num_2))
                self.num_2 += 1
                return item

        except:
            print('沒有这条数据')


def shuju(response, item, d_id_3_3, keywords_name_2):

    # 保存商品图片
    try:
        os_img_1 = []
        str_ran = str(random.randint(0, 999999))
        os_img_1.append(str_ran)
        os.makedirs('d:\\b2b_new\\{}'.format(str_ran))
        #     将图片链接保存到硬盘
        res_img = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[1]/div[1]/div/ul/li/img/@src')

        os_img_2_list = []
        # os_img_2_list
        for img_url in res_img:
            img_url = img_url.extract()
            img_url = img_url.strip()
            code_img = requests.get(url=img_url).content
            img_name = str(random.randint(1, 999999))
            with open('d:\\b2b_new\\{}\\{}.jpg'.format(str_ran, img_name), 'wb') as f:
                f.write(code_img)
            os_img_2 = 'http://img.ktcx.cn/b2b/' + '{}/{}.jpg'.format(str_ran, img_name)
            os_img_2_list.append(os_img_2)
        #
        os_img_2_str_1 = os_img_2_list[0]
        os_img_2_str = ','.join(os_img_2_list)
        # item['os_img_2_str_1'] = os_img_2_str_1
        # item['os_img_2_str'] = os_img_2_str

        # print('图片ok', os_img_2_list)
    except:
        print('图片错误.')

    # 1. `create_by`,\

    # 2. `create_date`, \
    # 获取当前时间
    create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
    item['create_date'] = create_date
    # print('create_date', type(create_date), create_date)
    # create_date

    # 3. `is_del`, \

    # 4. `list_img`, ........................
    # str(os_img_2_str_1)
    item['list_img'] = str(os_img_2_str_1)

    # 5. `price`, \
    try:
        price_list = []
        res_price = response.xpath(
            '/html/body/div[3]/div/div[1]/div[2]/div[2]/table//tr[@class="price"]/td[2]/div/span/text()').extract()
        for price in res_price:
            price = price.replace('\r', '').replace('\n', '').replace('\t', '')
            price_list.append(price)
            # print('价格', price_list[-1])
    except:
        print('没有')
    # str(price_list[-1])   价格字段
    item['price'] = str(price_list[-1])

    # 6. `title`,
    try:
        res_title = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/h1/text()')[0].extract()
        # print('标题：', res_title)
    except:
        print('没有')
    # str(res_title)
    item['title'] = str(res_title)

    # 7. `way`, \
    if price_list[-1]:
        way = '0'
    else:
        way = '1'
    item['way'] = way

    # 9. `two_level_id`, \
    sql = "SELECT parent_id FROM bus_industry_category WHERE id = {}".format(d_id_3_3)
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        # 遍历结果
        for row in results:
            two_level_id = row[0]
            # print('two_level_id', two_level_id)
        # 遍历结果
    except Exception as e:
        raise e
    item['two_level_id'] = two_level_id

    # 8. `one_level_id`, \
    sql = "SELECT parent_id FROM bus_industry_category WHERE id = {}".format(two_level_id)
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        # 遍历结果
        for row in results:
            one_level_id = row[0]
            # print('one_level_id', one_level_id)
        # 遍历结果
    except Exception as e:
        raise e
    item['one_level_id'] = one_level_id

    # 10. `three_level_id`,\
    # d_id_3
    item['three_level_id'] = d_id_3_3

    # 11. `custom_id`,

    # 12. `keywords`, \
    # [{\"id\":\"3\",\"keyword\":\"\\u4e2d\\u957f\\u6b3e\\u6bdb\\u5462\\u5916\\u5957\"}]
    keywords_list = []
    keywords_dict = {}
    keywords_dict['id'] = ''
    keywords_dict['keyword'] = keywords_name_2
    keywords_list.append(keywords_dict)
    keywords_json = json.dumps(keywords_list)
    item['keywords'] = keywords_json
    # keywords_json

    # 13. `models`, \

    # 14. `standards`,\

    # 15. `imgs`,\
    # os_img_2_str_json = json.dumps(os_img_2_str)
    # os_img_2_str
    item['imgs'] = os_img_2_str

    # 16. `sort`, \????????

    # 17. `update_time`, \
    update_time = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
    # update_time

    # 18. `state`,
    # '1'

    # 19. `is_verify`, \
    # '1'

    # 20. `verify_remark`,\

    # 21. `verify_time`, \

    # 22. `verify_by`,\

    # 23. `detail`, \
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
    # str(hebing_)
    item['detail'] = str(hebing_)

    # 24. `types`,
    # '0'

    # 25. `start_time`, \
    # 26. `end_time`, \
    # 27. `num`, \

    # 28. `units`,
    try:
        res_danwei = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/table//tr[2]/td[2]/div/text()')[
            0].extract()
        # print('res_danwei:', res_danwei)
    except:
        print('没有')
    # str(res_danwei)
    item['units'] = str(res_danwei)

    # 29. `money_units`, \
    # '元'

    # 30. `province_id`, \
    # 31. `province_name`,
    # 32. `city_id`, \
    # 33. `city_name`,\
    # 34. `view_count`, \
    # 35. `inquiry_count`, \

    # 36. `provider_id`, \
    # 37. `provider_name`,

    # 38. `is_import`, \
    # '1'

    # 39. `com_name`, \
    try:
        res_dizhi = response.xpath('/html/body/div[5]/div[5]/div[2]/ul/li[4]/span[3]/text()')[0].extract()
        # print('res_dizhi', res_dizhi)
    except:
        print('没有')
    # str(res_dizhi)
    item['com_name'] = str(res_dizhi)

    # 40. `linkman`,
    try:
        res_man = response.xpath('/html/body/div[5]/div[5]/div[2]/ul/li[3]/span[3]/text()')[0].extract()
        man = res_man[0:6].split(' ')[0]
        # print('man:', man)
    except:
        print('没有')
    # str(man)
    item['linkman'] = str(man)

    # 41. `mobile`,
    try:
        res_phone = response.xpath('/html/body/div[5]/div[5]/div[2]/ul/li[1]/span[3]/text()')[0].extract()
    except:
        print('没有')
    # str(res_phone)
    item['mobile'] = str(res_phone)

    # 42. `add_by`

    print('数据完成..')
















