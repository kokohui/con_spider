import json
import requests
import pymysql
from lxml import etree

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance_20190806',
                       port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


def translate(word):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    response = requests.post(url, data=key)
    if response.status_code == 200:
        return response.text
    else:
        print("翻译失败...")
        return None


def get_reuslt(repsonse):
    result = json.loads(repsonse)
    # print("输入的词为：%s" % result['translateResult'][0][0]['src'])
    # print("翻译结果为：%s" % result['translateResult'][0][0]['tgt'])
    trans_text = result['translateResult'][0][0]['tgt']
    # print(trans_text)
    return trans_text


def sql_query():
    conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance_20190806',
                           port=3306,
                           charset='utf8')

    cur = conn.cursor()  # 获取一个游标
    sql = "select id, name, shls, detail   from bus_new_release "

    try:
        rows = cur.execute(sql)
        data = cur.fetchall()
        return data, id
    except:
        conn.rollback()





def main(word):
    list_trans = translate(word)
    trans_text = get_reuslt(list_trans)

    return trans_text


if __name__ == '__main__':
    word_list = sql_query()
    print(word_list)
    # for word in word_list:
        # sql_id = word[0]
        # name_chinese = word[1]
        # shls_chinese = word[2]
        # detail_chiese = word[3]
        #
        # name_trans = main(name_chinese)
        # shls_trans = main(shls_chinese)
        # # detail_trans = main(detail_chiese)
        #
        #
        # try:
        #     sql = "update bus_new_release_en set name = '{}', shls = '{}' where id = '{}'" .format(name_trans, shls_trans, sql_id)
        #
        #     data = cur.execute(sql)
        #     conn.commit()
        # except Exception as e:
        #     raise e

cur.close()
conn.close()