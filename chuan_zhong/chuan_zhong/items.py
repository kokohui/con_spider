# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChuanZhongItem(scrapy.Item):
    title = scrapy.Field()
    brief = scrapy.Field()
    man = scrapy.Field()
    tel = scrapy.Field()
    tel_2 = scrapy.Field()
    fax = scrapy.Field()
    tel_qq = scrapy.Field()
    post_code = scrapy.Field()
    register = scrapy.Field()
    ad_url = scrapy.Field()
    addres = scrapy.Field()
    forms = scrapy.Field()
    com_time = scrapy.Field()
    com_type = scrapy.Field()
    zheng_xin = scrapy.Field()
    scope = scrapy.Field()
    product = scrapy.Field()

    # (item['title'], item['brief'],item['man'],item['tel'],item['tel_2'],item['fax'],item['tel_qq'],item['post_code'],item['register'],item['ad_url'],item['addres'],item['forms'],item['com_time'],item['com_type'],item['zheng_xin'],item['scope'],item['product'],)