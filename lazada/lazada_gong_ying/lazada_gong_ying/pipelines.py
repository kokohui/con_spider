import pymysql
import json


class LazadaGongYingPipeline(object):
    cursor = None  # mysql游标对象声明
    cur = None  # 获取一个游标

    def open_spider(self, spdier):
        print('爬虫开始》》》》')
        self.conn = pymysql.Connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance',
                                    port=3306,
                                    charset='utf8')
        self.cur = self.conn.cursor()  # 获取一个游标

    def process_item(self, item, spider):

        print('process_item>>>>>>>>>>>>>>>>>>>>>>>')
        # 查询公司存储个数, 如果没有则存储~
        sql_count = "select count(0) from bus_user where company_name='{}'".format(item['com_name'])
        self.cur.execute(sql_count)
        result = self.cur.fetchall()
        result_count = int(result[0][0])
        if result_count == 0:

            # dict_data = {
            #     "con_info": {"create_date": item['create_date'], "com_name": item["com_name"],
            #                  "linkman": item["linkman"], "mobile": item["mobile"], "address": item["address"],
            #                  "summary": item["summary"], "scopes": item["scopes"], "logo": item['list_img']},
            #     "pro_info": {"create_date": item['create_date'], "price": item['price'], "title": item['title'],
            #                  "way": item['way'], "one_level_id ": item['one_level_id'],
            #                  "two_level_id": item['two_level_id'], "three_level_id": item['three_level_id'],
            #                  "keywords": item['keywords'], "list_img": item['list_img'], "imgs": item['imgs'],
            #                  "detail": item['detail'], "units": item['units']}}

            dict_data = {
                "con_info": {"com_name": item["com_name"]},
                "pro_info": {"create_date": item['create_date'], "price": item['price'], "title": item['title'],
                             "way": item['way']}

            }

            json_data = json.dumps(dict_data)

            try:
                sql = 'insert into `bus_spider_product_list`(`create_date`, `detail`) value (%s, %s)'
                self.cur.execute(sql, (item['create_date'], json_data))
            except Exception as e:
                self.conn.rollback()
                print('事务处理失败')
                raise e
            else:
                self.conn.commit()
                print('数据添加成功')

            return item

    def close_spider(self, spider):
        # sql_id = "SELECT id FROM bus_spider_data WHERE source = '找商网' and  TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        # self.cur.execute(sql_id)
        # res_all_list = self.cur.fetchall()
        # id = res_all_list[0][0]
        # sql_insert = "UPDATE ktcx_buschance.bus_spider_data SET isuse='1' WHERE id={}".format(id)
        # print(sql_insert)
        #
        # self.cur.execute(sql_insert)
        # self.conn.commit()

        print('爬虫结束>>>>>>>>')
        self.cur.close()
        self.conn.close()
