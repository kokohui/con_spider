import pymysql
conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


sql_id = "SELECT url,id FROM bus_spider_data WHERE source='慧聪网'AND TYPE = 'huicong_gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 2 "
cur.execute(sql_id)
res_all_list = cur.fetchall()
for res_one_list in res_all_list:
    print(res_one_list[0])