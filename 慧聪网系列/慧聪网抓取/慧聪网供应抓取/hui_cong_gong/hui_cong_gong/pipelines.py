import pymysql


class HuiCongGongPipeline(object):
    cursor = None  # mysql游标对象声明
    cur = None  # 获取一个游标

    def open_spider(self, spdier):
        print('爬虫开始》》》》')
        self.conn = pymysql.Connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance',
                                    port=3306,
                                    charset='utf8')
        self.cur = self.conn.cursor()  # 获取一个游标

    def process_item(self, item, spider):
            # 进行存储
            try:
                # 第三表
                sql_in_2 = "insert into `tree_s` (`one_class_name`, `two_class_name`,`tree_class_name`, `tree_class_id`) values(%s,%s,%s,%s)"
                self.cur.execute(sql_in_2, (item['one_class_name'], item['two_class_name'], item['tree_class_name'], item['tree_class_id']))
            except Exception as e:
                self.conn.rollback()  # 事务回滚
                print('事务处理失败')
                raise e
            else:
                self.conn.commit()  # 事务提交
                print('数据添加成功')
            return item

    def close_spider(self, spider):

        print('爬虫结束>>>>>>>>')
        self.cur.close()
        self.conn.close()
