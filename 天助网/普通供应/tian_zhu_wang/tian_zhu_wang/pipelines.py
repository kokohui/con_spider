import pymysql


class TianZhuWangPipeline(object):
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

            # 数据库最大id查询
            res_num = 0
            try:
                sql_1 = 'select max(id) from bus_user'
                self.cur.execute(sql_1)
                res_num = int(self.cur.fetchone()[0]) + 1
                print('res.......................', res_num)
            except:
                print('查询错误.')

            # 进行存储
            try:
                sql = 'insert into `bus_user`(' \
                      '`id`,`name`, `logo`, `phone`, `password`, `source`, `type`, `state`, `plate_visit_num`, `plate_visit_pnum`,' \
                      ' `product_visit_num`, `balance`, `growth`, `status`, `company_name`, `linkman`, `mobile`, `number`, `url`, `submit_date`,' \
                      ' `by_date`, `domain_name`, `is_del`, `create_by`, `create_date`, `province_id`, `province_name`, `city_id`, `city_name`, `county_id`,' \
                      ' `county_name`, `address`, `sub_summary`, `summary`, `sub_scopes`, `scopes`, `minglu_img`, `company_img`, `mapx`, `mapy`,' \
                      ' `zip_code`, `email`, `qq`, `tel`, `website`, `total_fee`, `send_num`, `refresh_num`, `supply_inquiry_num`, `purchase_inquiry_num`,' \
                      ' `ad_price`, `openid`, `provider_id`, `provider_name`, `channel_duty_id`, `channel_open_id`, `service_id`, `keywords`, `is_cx`) ' \
                      'VALUE' \
                      '(%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                self.cur.execute(sql, (
                    res_num, item['com_name'], item['list_img'], item['mobile'], '123456', 'pc', 'supply', '1', 0, 0,
                    0, 0, 0, '0', item['com_name'], item["linkman"], item['mobile'], '', '', item['create_date'],
                    item['create_date'], '', '0', '5fc530f6b8574e03b6f13794ec64c1f8', item['create_date'], '', '', '',
                    '', '',
                    '', item['address'], '', item['summary'], '', item['scopes'], item['list_img'], item['list_img'],
                    '', '',
                    '', '', 123456, item['mobile'], '', 0, 0, 0, 0, 0,
                    0, '', '75cebe2e19434dcd9c4586f4621e6f9c', '', '', '', '', item['keywords'], 0))

                sql_in_2 = "insert into `bus_user_industry` (`create_by`, `one_level_id`, `two_level_id`, `three_level_id`, `sort`, `is_del`) values(%s,%s,%s,%s,%s,%s)"
                self.cur.execute(sql_in_2, (
                    res_num, item['one_level_id'], item['two_level_id'], item['three_level_id'], '1', '0'))

                sql_in = "INSERT INTO `bus_product` (`create_by`, `create_date`, `is_del`, `list_img`, `price`, `title`,`way`,`one_level_id`, `two_level_id`, `three_level_id`, `custom_id`, `keywords`,`models`,`standards`, `imgs`, `sort`, `update_time`, `state`, `is_verify`, `verify_remark`,`verify_time`, `verify_by`, `detail`, `types`, `start_time`, `end_time`, `num`, `units`,`money_units`, `province_id`, `province_name`, `city_id`, `city_name`, `view_count`,`inquiry_count`,`provider_id`, `provider_name`, `is_import`, `com_name`, `linkman`,`mobile`, `add_by`) VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                self.cur.execute(sql_in, (
                    res_num, item['create_date'], '0', item['list_img'], item['price'], item['title'], item['way'],
                    item['one_level_id'], item['two_level_id'], item['three_level_id'], 0, item['keywords'], '',
                    '', item['imgs'], '1', item['create_date'], '1', '1', 0,
                    item['create_date'], '', item['detail'], '0', item['create_date'], item['create_date'], 1,
                    item['units'],
                    '元', '', '', '', '', '0', '0',
                    '1ec40ecd3cf64908941b5f7679f19d2b', '', '0', item['com_name'], item['linkman'], item['mobile'],
                    '43e9737882af413095f612ef34412a8f'))  # 单条插入

                print('.......................................')
            except Exception as e:
                self.conn.rollback()  # 事务回滚
                print('事务处理失败')
                raise e
            else:
                self.conn.commit()  # 事务提交
                print('数据添加成功')
            return item

    def close_spider(self, spider):
        sql_id = "SELECT id FROM bus_spider_data WHERE source = '天助网' and  TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        self.cur.execute(sql_id)
        res_all_list = self.cur.fetchall()
        id = res_all_list[0][0]
        sql_insert = "UPDATE ktcx_buschance.bus_spider_data SET isuse='1' WHERE id={}".format(id)
        print(sql_insert)

        self.cur.execute(sql_insert)
        self.conn.commit()

        print('爬虫结束>>>>>>>>')
        self.cur.close()
        self.conn.close()
