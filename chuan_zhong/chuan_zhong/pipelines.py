# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class ChuanZhongPipeline(object):
    cursor = None  # mysql游标对象声明
    cur = None  # 获取一个游标

    def open_spider(self, spdier):
        print('爬虫开始》》》》')
        self.conn = pymysql.Connect(host='47.92.197.127', user='root', passwd='zhangxing888', db='ktcx_file',
                                    port=3306,
                                    charset='utf8')
        self.cur = self.conn.cursor()  # 获取一个游标

    def process_item(self, item, spider):
        # 数据库储存
        try:
            sql_in = "INSERT INTO `bus_comm` (`title`, `brief`,`man`, `tel`, `tel_2`, `fax`, `tel_qq`, `post_code`, `register`,`ad_url`, `addres`, `forms`, `com_time`, `com_type`, `zheng_xin`, `scope`, `product`) VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # print('sql', sql)
            data = self.cur.execute(sql_in, (item['title'], item['brief'],  item['man'],item['tel'],item['tel_2'],item['fax'],item['tel_qq'],item['post_code'],item['register'],item['ad_url'],item['addres'],item['forms'],item['com_time'],item['com_type'],item['zheng_xin'],item['scope'],item['product'],))  # 单条插入
            print('.......................................')
            print('data', data)
            # '`title`, `brief`,`man`, `tel`, `tel_2`, `fax`, `tel_qq`, `post_code`, `register`,`ad_url`, `addres`, `forms`, `com_time`, `com_type`, `zheng_xin`, `scope`, `product`'

            self.conn.commit()  # 提交
            print('添加成功')
        except Exception as e:
            raise e
        return item

    def close_spider(self, spider):
        print('爬虫结束>>>>>>>>')
        self.cur.close()
        self.conn.close()
