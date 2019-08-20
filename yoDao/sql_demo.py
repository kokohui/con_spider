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
APP_KEY = '05d75b8083faae9a'
APP_SECRET = 'JW7cD7E6hC4v5hfNwrjT5oC3Y1cydnXl'


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

    sql = 'select id, content  from bus_help_core where  content is not null and content != ""'

    try:
        cur.execute(sql)
        data = cur.fetchall()
        return data
    except:
        conn.rollback()


if __name__ == '__main__':
    word_list = sql_query()
    for word in word_list:
        sql_id = word[0]
        detail_chinese = word[1]

        soup = BeautifulSoup(str(detail_chinese), 'lxml')
        tree = etree.HTML(detail_chinese)

        img_p = ''
        try:
            img_list = soup.find_all('img')
            print(img_list)
            for img in img_list:
                img_p += str(img)
        except:
            print('没有图片')
        img_p_2 = "<p>" + img_p + "</p>"
        img_p_2 = str(img_p_2).replace('"', "'")
        print(img_p_2)

        name_trans_all = ''
        try:
            detail_text_list = tree.xpath('//p//text()')
            print("detail_text_list", detail_text_list)
            for detail_text in detail_text_list:
                name_trans = connect(detail_text)
                name_trans_all += str(name_trans)
        except:

            print('没有文字')
        name_trans_all_2 = "<p>" + name_trans_all + "</p>"
        print("name_trans_all_2:", name_trans_all_2)

        test_all = name_trans_all_2 + img_p_2
        test_all = test_all.replace('"', "'")
        try:
            sql = 'update bus_help_core set  content_en  = "{}"where id = "{}"' .format(test_all, sql_id)
            print(sql)
            data = cur.execute(sql)
            conn.commit()
        except:
            print('此处有个错')

        # break

cur.close()
conn.close()