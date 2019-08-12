# -*- coding: utf-8 -*-
import uuid
import requests
import hashlib
import time


YOUDAO_URL = 'http://openapi.youdao.com/api'
APP_KEY = '5565ae3f839e772e'
APP_SECRET = '6TCWA8dEp65uljPtI4vKITklTO6dLult'


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
    # print(response.json()["translation"])
    test = response.json()["translation"][0]
    return test


if __name__ == '__main__':
    q = '今天雨很大'
    test = connect(q)
    print(test)