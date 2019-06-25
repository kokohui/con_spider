# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class SouHaoHuoPipeline(object):
    cursor = None  # mysql游标对象声明
    cur = None  # 获取一个游标

    def open_spider(self, spdier):
        print('爬虫开始》》》》')
        self.conn = pymysql.Connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')
        self.cur = self.conn.cursor()  # 获取一个游标

    def process_item(self, item, spider):

        # # 执行查询sql语句
        # try:
        #     with self.conn.cursor() as cursor:
        #         # 执行sql语句，进行查询
        #         sql = "SELECT COUNT(0) FROM bus_product WHERE three_level_id = '' AND com_name = '' AND is_del = '0'"
        #         cursor.execute(sql)
        #         # 获取查询结果
        #         result = cursor.fetchall()
        #         print(result)
        #     # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        #     cursor.commit()
        # except Exception as e:
        #     raise e

        # 数据库储存
        try:
            sql_in = "INSERT INTO `bus_product_new` (`create_by`, `create_date`, `is_del`, `list_img`, `price`, `title`,`way`,`one_level_id`, `two_level_id`, `three_level_id`, `custom_id`, `keywords`,`models`,`standards`, `imgs`, `sort`, `update_time`, `state`, `is_verify`, `verify_remark`,`verify_time`, `verify_by`, `detail`, `types`, `start_time`, `end_time`, `num`, `units`,`money_units`, `province_id`, `province_name`, `city_id`, `city_name`, `view_count`,`inquiry_count`,`provider_id`, `provider_name`, `is_import`, `com_name`, `linkman`,`mobile`, `add_by`) VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # print('sql', sql)
            data = self.cur.execute(sql_in, ('1', item['create_date'], '0', item['list_img'], item['price'], item['title'], item['way'],
                item['one_level_id'], item['two_level_id'], item['three_level_id'], 0, item['keywords'], '',
                '', item['imgs'], '1', item['create_date'], '1', '1', 0,
                item['create_date'], '', item['detail'], '0', item['create_date'], item['create_date'], 1, item['units'],
                '元', '', '', '', '', '0', '0',
                '1ec40ecd3cf64908941b5f7679f19d2b', '', '1', item['com_name'], item['linkman'], item['mobile'], '43e9737882af413095f612ef34412a8f'))  # 单条插入
            print('.......................................')
            print('data', data)

            self.conn.commit()  # 提交
            print('添加成功')
        except Exception as e:
            raise e
        return item

    def close_spider(self, spider):
        print('爬虫结束>>>>>>>>')
        self.cursor.close()
        self.conn.close()
