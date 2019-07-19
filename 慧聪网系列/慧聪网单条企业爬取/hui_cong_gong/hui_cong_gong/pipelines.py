import pymysql
import json

item_pro_list = []
item_con_dict = {}
item_url_dict = {}


class HuiCongGongPipeline(object):
    cursor = None
    cur = None
    conn = None

    def open_spider(self, spdier):
        print('爬虫开始》》》》')
        self.conn = pymysql.Connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance',
                                    port=3306,
                                    charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):

        print('process_item>>>>>>>>>>>>>>>>>>>>>>>')
        item_dict = dict(item)
        item_dict.pop('com_name')
        item_dict.pop('address')
        item_dict.pop('summary')
        item_dict.pop('scopes')
        item_dict.pop('linkman')
        item_dict.pop('mobile')
        item_dict.pop('start_url')
        item_dict.pop('lun_imgs')

        item_pro_list.append(item_dict)
        item_con_dict['com_name'] = item['com_name']
        item_con_dict['address'] = item['address']
        item_con_dict['summary'] = item['summary']
        item_con_dict['scopes'] = item['scopes']
        item_con_dict['linkman'] = item['linkman']
        item_con_dict['mobile'] = item['mobile']
        item_con_dict['lun_imgs'] = item['lun_imgs']
        item_con_dict['logo'] = item['list_img']

        item_url_dict['start_url'] = item['start_url']
        item_url_dict['create_date'] = item['create_date']

    def close_spider(self, spider):
        print('爬虫结束, 开始存储>>>>>>>>')
        dict_data = {}
        dict_data['item_con_dict'] = item_con_dict
        dict_data['item_pro_list'] = item_pro_list
        item_json = json.dumps(dict_data)
        create_by = str(item_url_dict['start_url'])
        create_date = item_url_dict['create_date']

        # 进行存储
        try:
            sql_in_2 = "insert into `bus_spider_list` (`create_by`,`create_date`,`is_del`, `json_str`) values(%s, %s, %s, %s)"
            self.cur.execute(sql_in_2, (create_by, create_date, '0', item_json))

        except Exception as e:
            self.conn.rollback()  # 事务回滚
            print('事务处理失败')
            raise e
        else:
            self.conn.commit()  # 事务提交
            print('数据添加成功')

        self.cur.close()
        self.conn.close()
