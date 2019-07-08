# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuiCongGongItem(scrapy.Item):
    create_date = scrapy.Field()  # 创建时间
    list_img = scrapy.Field()  # 图片1
    price = scrapy.Field()  # 价格
    title = scrapy.Field()  # 标题
    way = scrapy.Field()  # way
    one_level_id = scrapy.Field()  # 一级id
    two_level_id = scrapy.Field()  # 二级id
    three_level_id = scrapy.Field()  # 三级id
    keywords = scrapy.Field()
    imgs = scrapy.Field()
    detail = scrapy.Field()
    units = scrapy.Field()
    com_name = scrapy.Field()
    linkman = scrapy.Field()
    mobile = scrapy.Field()
    address = scrapy.Field()
    summary = scrapy.Field()
    scopes = scrapy.Field()
    com_keyword = scrapy.Field()

    one_class_name = scrapy.Field()
    one_class_id = scrapy.Field()
    two_class_name = scrapy.Field()
    two_class_id = scrapy.Field()
    tree_class_name = scrapy.Field()
    tree_class_id = scrapy.Field()
