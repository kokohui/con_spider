import pymysql
conn = pymysql.Connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')
cur = conn.cursor()  # 获取一个游标


# 数据库最大mulu查询
# sql_id = "SELECT * FROM bus_spider_data WHERE TYPE = 'chengxin' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
# cur.execute(sql_id)
# res_all_list = cur.fetchall()

sql_id = "SELECT * FROM bus_spider_data WHERE TYPE = 'chengxin' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
cur.execute(sql_id)
res_all_list = cur.fetchall()
for res_all in res_all_list:
    one_level = res_all[4]
    print('id.........', one_level)

    two_level = res_all[5]
    print('id.........', two_level)

    three_level = res_all[6]
    print('id.........', three_level)

cur.close()
conn.close()
