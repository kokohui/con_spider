# -*- coding: utf-8 -*-
import uuid
import hashlib
import time
import requests
import pymysql
import asyncio
import json
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

    sql = 'select id, title from bus_help_core where  title is not null and title != ""'

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
            standards_chinese_list = word[1]
            try:
                standards_chinese_list = json.loads(word[1])
                standards_trans_list = []
                for standards_chinese_dict in standards_chinese_list:
                    standards_chinese = standards_chinese_dict['keyword']
                    print(standards_chinese)
                    name_trans = ''

                    try:
                        name_trans = connect(standards_chinese)
                        standards_chinese_dict['keyword'] = name_trans
                        standards_trans_list.append(standards_chinese_dict)
                        print(name_trans)
                    except:
                        print('没有文字')
            except:
                print('不是json')

            if name_trans != '':
                test_all = str(standards_trans_list).replace('"', "'")
                test_all = json.dumps(test_all).replace('"', "'")
                print("test_all", test_all)

                try:
                    sql = 'update bus_help_core set  title  = "{}" where id = "{}"'.format(test_all, sql_id)
                    print(sql)
                    data = cur.execute(sql)
                    conn.commit()
                except Exception as e:
                    raise e
                    print('此处有个错')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    # sql_query()

cur.close()
conn.close()