import requests
import json

import json
import requests
import pymysql
from lxml import etree

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance_20190806',
                       port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


def translate(word):
    url = "http://fanyi.so.com/index/search?eng=0&validate=&ignore_trans=0&query=%E8%BF%98%E5%9C%A8%E4%B8%8B%E9%9B%A8%0A"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }

    formdata = {
        "eng": "0",
        "validate": "",
        "ignore_trans": "0",
        "query": word,
    }

    response = requests.post(url=url, data=formdata, headers=headers)

    print('1111111', response)
    if response.status_code == 200:
        print(response.text)
        return response.text
    else:
        print("翻译失败...")
        return None


def get_reuslt(repsonse):
    result = json.loads(repsonse)
    trans_text = result['data']['fanyi']
    return trans_text


def sql_query():

    sql = "select id, title  from bus_product"

    try:
        cur.execute(sql)
        data = cur.fetchall()
        return data
    except:
        conn.rollback()


def main(word):
    list_trans = translate(word)
    trans_text = get_reuslt(list_trans)

    return trans_text


if __name__ == '__main__':
    word_list = sql_query()
    for word in word_list:
        sql_id = word[0]
        name_chinese = word[1]
    #     shls_chinese = word[2]
    #     detail_chiese = word[3]

        name_trans = main(name_chinese)

    #     shls_trans = main(shls_chinese)
    #     # detail_trans = main(detail_chiese)

        try:
            sql = 'update bus_product_en set title = "{}" where id = "{}"' .format(name_trans, sql_id)
            print(sql)
            data = cur.execute(sql)
            conn.commit()
        except Exception as e:
            raise e

        # break

cur.close()
conn.close()


