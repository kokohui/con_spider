import requests
from lxml import etree
import re
import time
import pymysql  # 导入pymysql包
import random
import os
import json

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


# 1. 获取详情页url列表
def res_11(url_url):
    res_list_url = []
    for num in range(2, 3):
        # 'http://www.912688.com/chanpin/5F2F5934-orderBymultiple-aoddesc-viewlist-page{}.html'.format(str(num)
        # 'http://www.912688.com/chanpin/9488523A65E07EBA5E03-orderBymultiple-aoddesc-viewlist-page{}.html'

        url = url_url.format(str(num))
        res_html = requests.get(url=url, headers=headers).text

        tree = etree.HTML(res_html)
        res_url_1ist = tree.xpath(
            '//div[@class="product-left-new clearfix"]/ul/li/div[@class="clearfix"]/div[@class="sm-list-l-img-new"]/a/@href')
        for res_url in res_url_1ist:
            res_list_url.append(res_url)
        print('..........................启动程序{}................'.format(num))

    return res_list_url


def res_22(res_list_url, d_id_3, keywords_name):
    num_num = 1
    for res_li in res_list_url:
        res_detail_html = requests.get(url=res_li, headers=headers).text
        tree = etree.HTML(res_detail_html)

        # 保存商品图片
        try:
            os_img_1 = []
            str_ran = str(random.randint(0, 999999))
            os_img_1.append(str_ran)
            os.makedirs('d:\\project_img\\{}'.format(str_ran))
            #     将图片链接保存到硬盘
            res_img = tree.xpath('/html/body/div[3]/div/div[1]/div[2]/div[1]/div[1]/div/ul/li/img/@src')

            os_img_2_list = []

            for img_url in res_img:
                img_url = img_url.strip()
                code_img = requests.get(url=img_url, headers=headers).content
                img_name = str(random.randint(1, 999999))
                with open('d:\\project_img\\{}\\{}.jpg'.format(str_ran, img_name), 'wb') as f:
                    f.write(code_img)
                print('ok')
                os_img_2 = '{}/{}.jpg'.format(str_ran, img_name)
                os_img_2_list.append(os_img_2)

            os_img_2_str_1 = os_img_2_list[0]
            os_img_2_str = ','.join(os_img_2_list)

            # print('图片ok', os_img_2_list)
        except:
            print('图片错误.')

        # 12. 保存商品详情页图片
        # 需要图片的路径名字
        # try:
        #     img_dict = {}
        #     delia_img_1 = []  # 详情图片的文件夹名字
        #     str_ran_2 = str(random.randint(0, 999999))
        #     delia_img_1.append(str_ran_2)
        #     os.makedirs('d:\\newnew33\\{}'.format(str_ran_2))
        #     res_delia_img = tree.xpath('//*[@id="prodDetailDiv"]/p/img/@src')
        #     delia_img_2 = []  # 详情图片名字
        #     for delia_img in res_delia_img:
        #         delia_img = delia_img.strip()
        #         code_img = requests.get(url=delia_img).content
        #         name = str(random.randint(1, 100))
        #         # print('name', name)
        #         delia_img_2.append(name + '.jpg')
        #         with open('d:\\newnew33\\{}\\{}.jpg'.format(str_ran_2, name), 'wb') as f:
        #             f.write(code_img)
        #         print('详情ok')
        #
        #     print('delia_img_2', delia_img_2)
        #     delia_img_2_str = ','.join(delia_img_2)
        #     print('详情', delia_img_2_str)
        #     img_dict['delia_img_1'] = delia_img_1
        #     img_dict['delia_img_2'] = delia_img_2

        # except:
        #     print('详情图保存错误')
        #

        # 1. `create_by`,\

        # 2. `create_date`, \
        # 获取当前时间
        create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
        print('create_date', type(create_date), create_date)
        # create_date

        # 3. `is_del`, \

        # 4. `list_img`, ........................
        # str(os_img_2_str_1)

        # 5. `price`, \
        #     6.价格
        try:
            price_list = []
            res_price = tree.xpath(
                '/html/body/div[3]/div/div[1]/div[2]/div[2]/table//tr[@class="price"]/td[2]/div/span/text()')
            for price in res_price:
                price = price.replace('\r', '').replace('\n', '').replace('\t', '')
                price_list.append(price)
        except:
            print('没有')
        # str(price_list[-1])   价格字段

        # 6. `title`,
        try:
            res_title = tree.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/h1/text()')[0]
        except:
            print('没有')
        # str(res_title)

        # 7. `way`, \
        if price:
            wey = '0'
        else:
            wey = '1'

        # 9. `two_level_id`, \
        sql = "SELECT parent_id FROM bus_industry_category WHERE id = {}".format(d_id_3)
        try:
            cur.execute(sql)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
            # 遍历结果
            for row in results:
                two_level_id = row[0]
                print('two_level_id', two_level_id)
            # 遍历结果
        except Exception as e:
            raise e

        # 8. `one_level_id`, \
        sql = "SELECT parent_id FROM bus_industry_category WHERE id = {}".format(two_level_id)
        try:
            cur.execute(sql)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
            # 遍历结果
            for row in results:
                one_level_id = row[0]
                print('one_level_id', one_level_id)
            # 遍历结果
        except Exception as e:
            raise e

        # 10. `three_level_id`,\
        # d_id_3

        # 11. `custom_id`,

        # 12. `keywords`, \
        # [{\"id\":\"3\",\"keyword\":\"\\u4e2d\\u957f\\u6b3e\\u6bdb\\u5462\\u5916\\u5957\"}]
        keywords_list = []
        keywords_dict = {}
        keywords_dict['id'] = ''
        keywords_dict['keyword'] = keywords_name
        keywords_list.append(keywords_dict)
        keywords_json = json.dumps(keywords_list)
        print('keywords_json', type(keywords_json), keywords_json)
        # keywords_json

        # 13. `models`, \

        # 14. `standards`,\

        # 15. `imgs`,\
        # os_img_2_str_json = json.dumps(os_img_2_str)
        # os_img_2_str

        # 16. `sort`, \????????

        # 17. `update_time`, \
        update_time = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
        # update_time

        # 18. `state`,
        # '1'

        # 19. `is_verify`, \
        # '1'

        # 20. `verify_remark`,\

        # 21. `verify_time`, \

        # 22. `verify_by`,\

        # 23. `detail`, \
        try:
            html = re.findall('<div class="table".*?(<table.*?</table>).*?</div>', res_detail_html, re.S)[0]

            # res_delia_HTML = re.findall('<div id="prodDetailDiv".*?<p>.*?</div>', res_detail_html, re.S)[0]
            res_delia_HTML = re.findall('<div id="prodDetailDiv".*?<div class="note">', res_detail_html, re.S)[0]

            #             print(res_delia_HTML)
            a = res_delia_HTML
            strinfo = re.compile('<p style="(.*?)".*?>.*?</p>')
            hh = strinfo.sub('', a)

            d = hh
            strinfo = re.compile('<div class="note">')
            hhh = strinfo.sub('', d)

            e = hhh
            strinfo = re.compile('<br.*?>')
            hhhh = strinfo.sub('', e)

            # .....................................
            img_de_list = re.findall('<img.*?src=.*?/>', hhhh, re.S)
            img_de_src_list = re.findall('<img.*?src="(.*?)".*?/>', hhhh, re.S)

            str_ran_2 = str(random.randint(0, 999999))
            os.makedirs('d:\\newnew33\\{}'.format(str_ran_2))

            print('img_de_list.........................', len(img_de_list), img_de_list)
            print('img_de_src_list.........................', len(img_de_src_list), img_de_src_list)
            for inx, delia_img in enumerate(img_de_src_list):
                print('delia_img...................', delia_img)
                print('inx...................', inx)
                # delia_img = delia_img.strip()
                code_img = requests.get(url=delia_img).content
                name = str(random.randint(1, 100))
                # print('name', name)
                delia_img_2.append(name + '.jpg')
                with open('d:\\newnew33\\{}\\{}.jpg'.format(str_ran_2, name), 'wb') as f:
                    f.write(code_img)
                print('详情ok')

                xx = img_de_list[inx]
                strinfo = re.compile('<img.*?src="(.*?)".*?/>')
                strinfo.sub('http:' + '/' + str_ran_2 + '/' + name, xx)
                # print(res_delia_html)
            print('//////////////////////////////////////////////')
            print('hhhhhhhhhhhhhhhhhhhhhhhhhh>>>>>>>>>>>>>>>>>>>>>', hhhh)

            # ......................................

            # b = hhhh
            # strinfo = re.compile('<img.*?src=.*?/>')
            # res_delia_html = strinfo.sub(' ', b)
            res_delia_html = hhhh

            hebing_ = str(html) + '<br/><br/>' + str(res_delia_html)
        except:
            print('没有')
        # str(hebing_)

        # 24. `types`,
        # '0'

        # 25. `start_time`, \
        # 26. `end_time`, \
        # 27. `num`, \

        # 28. `units`,
        try:
            res_danwei = tree.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/table//tr[2]/td[2]/div/text()')[0]
        except:
            print('没有')
        # str(res_danwei)

        # 29. `money_units`, \
        # '元'

        # 30. `province_id`, \
        # 31. `province_name`,
        # 32. `city_id`, \
        # 33. `city_name`,\
        # 34. `view_count`, \
        # 35. `inquiry_count`, \

        # 36. `provider_id`, \
        # 37. `provider_name`,

        # 38. `is_import`, \
        # '1'

        # 39. `com_name`, \
        try:
            res_dizhi = tree.xpath('/html/body/div[5]/div[5]/div[2]/ul/li[4]/span[3]/text()')[0]
        except:
            print('没有')
        # str(res_dizhi)

        # 40. `linkman`,
        try:
            res_man = tree.xpath('/html/body/div[5]/div[5]/div[2]/ul/li[3]/span[3]/text()')[0]
            man = res_man[0:6].split(' ')[0]
        except:
            print('没有')
        # str(man)

        # 41. `mobile`,
        try:
            res_phone = tree.xpath('/html/body/div[5]/div[5]/div[2]/ul/li[1]/span[3]/text()')[0]
        except:
            print('没有')
        # str(res_phone)

        # 42. `add_by`

        # 数据库储存
        try:
            sql_in = "INSERT INTO `bus_product` (`create_by`, `create_date`, `is_del`, `list_img`, `price`, `title`,`way`,`one_level_id`, `two_level_id`, `three_level_id`, `custom_id`, `keywords`,`models`,`standards`, `imgs`, `sort`, `update_time`, `state`, `is_verify`, `verify_remark`,`verify_time`, `verify_by`, `detail`, `types`, `start_time`, `end_time`, `num`, `units`,`money_units`, `province_id`, `province_name`, `city_id`, `city_name`, `view_count`,`inquiry_count`,`provider_id`, `provider_name`, `is_import`, `com_name`, `linkman`,`mobile`, `add_by`) VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # print('sql', sql)
            data = cur.execute(sql_in, (
                '1', create_date, '0', str(os_img_2_str_1), str(price_list[-1]), str(res_title), str(wey),
                str(one_level_id), str(two_level_id), str(d_id_3), 0, keywords_json, '',
                '', os_img_2_str, '1', create_date, '1', '1', 0,
                create_date, '', str(hebing_), '0', create_date, create_date, 1, str(res_danwei),
                '元', '', '', '', '', '0', '0',
                '1ec40ecd3cf64908941b5f7679f19d2b', '', '1', str(res_dizhi), str(man), str(res_phone), ''
            ))  # 单条插入
            print('.......................................')
            print('data', data)

            conn.commit()  # 提交
        except Exception as e:
            raise e

        # print(data)  # 打印返回结果

        time.sleep(0.1)

        print('爬取第{}条'.format(num_num))
        num_num += 1


url_url = 'http://www.912688.com/chanpin/624B90E862A47406-orderBymultiple-aoddesc-viewlist-page{}.html'
d_id_3 = '740'
keywords_name = '手部护理'
ress = res_11(url_url)
res_22(ress, d_id_3, keywords_name)

cur.close()  # 关闭游标
conn.close()  # 关闭连接

# def delia_img():
#     try:
#         img_dict = {}
#         delia_img_1 = []  # 详情图片的文件夹名字
#         str_ran_2 = str(random.randint(0, 999999))
#         delia_img_1.append(str_ran_2)
#         os.makedirs('d:\\newnew33\\{}'.format(str_ran_2))
#         res_delia_img = tree.xpath('//*[@id="prodDetailDiv"]/p/img/@src')
#         delia_img_2 = []  # 详情图片名字
#         for delia_img in res_delia_img:
#             delia_img = delia_img.strip()
#             code_img = requests.get(url=delia_img).content
#             name = str(random.randint(1, 100))
#             # print('name', name)
#             delia_img_2.append(name + '.jpg')
#             with open('d:\\newnew33\\{}\\{}.jpg'.format(str_ran_2, name), 'wb') as f:
#                 f.write(code_img)
#             print('详情ok')
#
#         print('delia_img_2', delia_img_2)
#         delia_img_2_str = ','.join(delia_img_2)
#         print('详情', delia_img_2_str)
#         img_dict['delia_img_1'] = delia_img_1
#         img_dict['delia_img_2'] = delia_img_2
#
#     except:
#         print('详情图保存错误')









