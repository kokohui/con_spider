# -*- coding: utf-8 -*-
import uuid
import hashlib
import time
import requests
import pymysql
import asyncio

from lxml import etree
from bs4 import BeautifulSoup

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance_20190806',
                       port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标

YOUDAO_URL = 'http://openapi.youdao.com/api'
APP_KEY = '4acec3be94933473'
APP_SECRET = 'rUnL8EC2piDimVArrV85zZGaTPX9vdxh'


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
    print('状态:', response.status_code)

    test = response.json()["translation"][0]
    error_code = response.json()["errorCode"]
    print(response.text)
    print('error_code:', error_code)
    if error_code == "0":
        return test
    else:
        print('状态出错:', error_code)


def sql_query():

    sql = 'select id, address from bus_user_en where   address is not null and address != "" and id > 98119'

    try:
        cur.execute(sql)
        data = cur.fetchall()
        print("data", data)
        return data
    except:
        conn.rollback()


async def main():
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

            if name_trans != '':
                test_all = str(name_trans).replace('"', "'")

                try:
                    sql = 'update bus_user_en set  address  = "{}" where id = "{}"'.format(test_all, sql_id)
                    print(sql)
                    data = cur.execute(sql)
                    conn.commit()
                except:
                    print('此处有个错')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())




cur.close()
conn.close()