import requests
from lxml import etree
import random
import pymysql
import asyncio

conn = pymysql.Connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance',
                                    port=3306,
                                    charset='utf8')
cur = conn.cursor()  # 获取一个游标

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}


def getIp(url):
    res_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(res_text)

    tr_list = tree.xpath('//*[@id="ip_list"]//tr')[1:]
    for tr in tr_list:
        try:
            ip_list = tr.xpath('./td[2]/text()')[0]
            print(ip_list)

            port_list = tr.xpath('./td[3]/text()')[0]
            print(port_list)

            type_list = tr.xpath('./td[6]/text()')[0]
            print(type_list)

            adress_list = tr.xpath('./td[4]/a/text()')[0]
            print(adress_list)

            # 进行存储
            try:

                # 第三表
                sql_in_2 = "insert into `ip_list` (`ip`, `port`, `type`, `adress`) values(%s,%s,%s,%s)"
                cur.execute(sql_in_2, (
                    ip_list, port_list, type_list, adress_list))

            except Exception as e:
                conn.rollback()  # 事务回滚
                print('事务处理失败')
                raise e
            else:
                conn.commit()  # 事务提交
                print('数据添加成功')
        except:
            print('错误')


url_list = 'https://www.xicidaili.com/nn'
for num in range(0, 3752):
    url = 'https://www.xicidaili.com/nn/{}'.format(num)
    getIp(url)







