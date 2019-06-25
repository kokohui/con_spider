import pymysql
import os
import re
import shutil

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


def data_query():
    try:
        with conn.cursor() as cursor:
            # 执行sql语句，进行查询
            # 找出数据库中  同一个类目下每个公司出现的次数
            sql = "SELECT imgs  FROM bus_product_new group by three_level_id, com_name having count(com_name)=1"
            cursor.execute(sql)
            # 获取查询结果
            result = cursor.fetchall()
            img_name_list = []
            for i in result:
                img_utl_str = i[0]
                # print(img_utl_str)
                img_name = re.findall('/b2b/(.*?)/', img_utl_str, re.S)
                # print(img_name)
                for name in img_name:
                    img_name_list.append(name)
            # print(img_name_list)

        # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        # cursor.commit()
    except Exception as e:
        raise e
    return img_name_list


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(dirs)
        return dirs


if __name__ == '__main__':
    img_url_list = data_query()
    root_name = file_name(r'd:\b2b_new')
    print(img_url_list)
    print(root_name)

    for ro in root_name:
        # print(ro)
        if ro not in img_url_list:

            path = os.path.join(r'd:\b2b_new', ro)
            print(path)
            shutil.rmtree(path)




