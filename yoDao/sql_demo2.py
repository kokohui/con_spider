# -*- coding: utf-8 -*-
import uuid
import hashlib
import time
import requests
import pymysql

from lxml import etree
from bs4 import BeautifulSoup

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance_20190806',
                       port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标

YOUDAO_URL = 'http://openapi.youdao.com/api'
APP_KEY = '1ed4a7c384866571'
APP_SECRET = 'DJKSDSmPKpw49z9ychpnsw9Je9mobZay'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(q):

    data = {}
    data['from'] = 'zh-CHS'
    data['to'] = 'EN'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    test = response.json()["translation"][0]
    return test


def sql_query():

    # sql = "select id, title  from bus_product whenever ttt='0'"
    sql = 'select id, name from bus_user_en where ttt="0" and name !="" and name is not null '

    try:
        cur.execute(sql)
        data = cur.fetchall()
        print("data", data)
        return data
    except:
        conn.rollback()


if __name__ == '__main__':
    word_list = sql_query()
    for word in word_list:
        sql_id = word[0]
        standards_chinese = word[1]
        print(standards_chinese)

        name_trans = ''
        try:
            name_trans = connect(standards_chinese)
            print(name_trans)
        except:
            print('没有文字')

        test_all = str(name_trans).replace('"', "'").replace("(", "").replace(")", "")
        try:
            sql = 'update bus_user_en set  name  = "{}", ttt = "1" where id = "{}"' .format(test_all, sql_id)
            # sql = 'instert into bus_product_quality_en()' .format(name_trans, sql_id)
            print(sql)
            data = cur.execute(sql)
            conn.commit()
        except:
            print('此处有个错')

        # break

cur.close()
conn.close()