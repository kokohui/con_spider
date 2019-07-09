from selenium import webdriver
from time import sleep
from selenium.webdriver import ChromeOptions
import requests
from lxml import etree
import json
from bs4 import BeautifulSoup
import re
import random
import os

s = requests.session()


class login():

    def __init__(self):

        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 创建一个浏览器对象
        self.bro = webdriver.Chrome(executable_path=r'D:\chromedriver', chrome_options=option)
        # self.bro = webdriver.Chrome(executable_path=r'C:\谷歌selenium驱动\chromedriver', chrome_options=option)
        self.url = 'https://login.1688.com/member/signin.htm?spm=b26110380.sw1688.1.3.780e4510sQlgTW&Done=https%3A%2F%2Fs.1688.com%2Fselloffer%2Foffer_search.htm%3Fkeywords%3D%25B6%25FA%25BB%25FA%26button_click%3Dtop%26earseDirect%3Dfalse%26n%3Dy%26netType%3D1%252C11'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        self.cookies = ''
        self.page_text = ''
        self.list_url_dedail = []
        self.cookies_dict = dict()
        # self.con_url = ''

    def sinin(self):
        """登录"""

        self.bro.get(url=self.url)
        sleep(3)

        iframe = self.bro.find_element_by_xpath('//iframe')  # 找到“嵌套”的iframe
        self.bro.switch_to.frame(iframe)  # 切换到iframe
        sleep(2)

        self.bro.find_element_by_id('J_Quick2Static').click()
        sleep(2)

        self.bro.find_element_by_id('TPL_username_1').send_keys('辉哥又来啦')
        sleep(2)
        self.bro.find_element_by_id('TPL_password_1').send_keys('kong267871')
        sleep(2)
        self.bro.find_element_by_id('J_SubmitStatic').click()
        sleep(2)
        try:
            self.bro.find_element_by_xpath('//*[@id="s-module-overlay"]/div[2]/div/div[2]/em[4]').click()
            sleep(2)
        except:
            print('没有')

        # 获取session
        self.cookies = self.bro.get_cookies()
        with open("cookies.txt", "w") as fp:
            json.dump(self.cookies, fp)

        self.page_text = self.bro.page_source

    def kill(self):
        """关闭selenium"""
        self.bro.quit()

    def parse_url(self):
        """获取详情页url列表"""

        url = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%B6%FA%BB%FA&button_click=top&earseDirect=false&n=y&netType=1%2C11'
        cookies_dict = self.cookies_dict
        with open("cookies.txt", "r") as fp:
            cookies = json.load(fp)
            for cookie in cookies:
                cookies_dict[cookie['name']] = cookie['value']
        print(cookies_dict)
        
        r = s.get(url=url, headers=self.headers, cookies=cookies_dict)
        r.encoding = 'utf-8'
        r = r.content

        tree = etree.HTML(r)
        for num in range(1, 21):
            res_url_list = tree.xpath('//*[@id="offer{}"]/div[@class="imgofferresult-mainBlock"]/div[1]/a/@href'.format(num))
            # 'https://login.1688.com/member/signin.htm?from=sm&Done=http://detail.1688.com/offer/567003895208.html'

            for res_url in res_url_list:
                print(res_url)
                print('.........................')
                self.list_url_dedail.append(res_url)
                sleep(3)
                
    def parse_detail(self):
        """解析商品详情页内容"""

        cookies_dict = self.cookies_dict
        for res_url in self.list_url_dedail:
            response = s.get(url=res_url, headers=self.headers, cookies=cookies_dict)
            response.encoding = 'utf-8'
            response = response.content
            # print(response)
            tree = etree.HTML(response)

            # 保存商品图片
            os_img_2_list = []
            try:
                os_img_1 = []
                str_ran = str(random.randint(0, 999999))
                os_img_1.append(str_ran)
                os.makedirs('/home/imgServer/spiders/{}'.format(str_ran))
                #     将图片链接保存到硬盘
                res_img = tree.xpath('//*[@id="dt-tab"]/div/ul/li/div/a/img/@src')
                for img_url in res_img:
                    img_url = img_url.replace('.60x60', '')

                    if img_url.endswith('.jpg'):
                        print('img_url', img_url)

                        code_img = requests.get(url=img_url).content
                        img_name = str(random.randint(1, 999999))
                        with open('/home/imgServer/spiders/{}/{}.jpg'.format(str_ran, img_name), 'wb') as f:
                            f.write(code_img)
                        os_img_2 = 'http://img.youkeduo.com.cn/spiders/' + '{}/{}.jpg'.format(str_ran, img_name)
                        os_img_2_list.append(os_img_2)
                os_img_2_str_1 = os_img_2_list[0]
                os_img_2_str = ','.join(os_img_2_list)

                print('图片ok', os_img_2_list)
            except:
                print('图片错误.')

            # 标题
            res_title = ''
            try:
                res_title = tree.xpath('//h1/text()')[0]
                print('res_title', res_title)
            except:
                print('res_title', res_title)

            # detail详情
            res_detail_html = response
            try:
                soup = BeautifulSoup(res_detail_html, 'lxml')
                html = str(soup.find('div', class_="detail-inside area-detail-feature"))

                strinfo = re.compile('<img.*?>')
                html_2 = strinfo.sub('', html)

                strinfo = re.compile('<br.*?>')
                html_3 = strinfo.sub('', html_2)

                # 把下载图片添加到html
                div_list = ['<div id="img_detail">', '</div>']
                for os_img_2_url in os_img_2_list:
                    os_img_2_url = '<img alt="{}" src="{}">'.format(res_title, os_img_2_url)
                    div_list.insert(1, os_img_2_url)
                div_str = '<br>\n'.join(div_list)

                html_all = html_3 + '\n' + div_str
            except Exception as e:
                raise e


            # 价格
            res_price = ''
            try:
                res_price = tree.xpath('//tr[@class="price"]//text()')
                res_price = ''.join(res_price).strip()
                res_price = res_price.replace('\n', '').replace('\t', '').replace(' ', '')
                if res_price.startswith('价格¥'):
                    res_price = re.findall(r'\d+\.\d+', res_price, re.S)[0]
                print('下面是价格:')
                print('res_price>>>>', res_price)
            except:
                print('res_price', res_price)

            # 单位
            unit = ''
            try:
                unit = tree.xpath('//span[@class="unit"]/text()')[0]
                print('unit', unit)
            except:
                print('unit', unit)

            # 公司名
            con_name = ''
            try:
                con_name = tree.xpath('//a[@class="company-name"]/text()')[0].strip()
                print('con_name', con_name)
            except:
                print('con_name', con_name)

            # 联系地址
            con_adress = ''
            try:
                con_adress = tree.xpath('//div[@class="item address fd-clr"]/span/text()')[0]
                print('con_adress', con_adress)
            except:
                print('con_adress', con_adress)

            # 公司详情url, 和联系方式详情url
            con_url = ''
            link_url = ''
            try:
                con_url = tree.xpath('//*[@id="topnav"]/div/ul/li[@data-page-name="creditdetail"]/a/@href')[0].strip()
                link_url = tree.xpath('//*[@id="topnav"]/div/ul/li[@data-page-name="contactinfo"]/a/@href')[0].strip()
                print('con_url', con_url)
            except:
                print('con_url', con_url)

            sleep(3)
            self.parse_con(self, con_url)
            sleep(3)
            self.parse_link(self, link_url)

    @staticmethod
    def parse_link(self, link_url):
        """解析部分联系方式"""
        print('parse_link>>>>>>>')
        res_con = s.get(url=link_url, headers=self.headers, cookies=self.cookies_dict).text
        tree = etree.HTML(res_con)

        # 联系人
        con_man = ''
        try:
            con_man = tree.xpath('//a[@class="membername"]/text()')[0].strip()
            # con_man_2 = tree.xpath('//a[@class="name"]/text()')[0].strip()
            print('con_man', con_man)
            # print('con_man_2', con_man_2)
        except:
            print('con_man', con_man)

        # 联系电话
        con_tel = ''
        try:
            # con_tel = tree.xpath('//dd[@class="mobile-number"]/text()')[0].strip()
            con_tel = tree.xpath('//dl[@class="m-mobilephone"]/dd/text()')[0].strip()
            print('con_tel', con_tel)
        except:
            print('con_tel', con_tel)

    @staticmethod
    def parse_con(self, con_url):
        """解析公司部分内容"""
        print('parse_con>>>>>>>>>')
        res_con = s.get(url=con_url, headers=self.headers, cookies=self.cookies_dict).text
        tree = etree.HTML(res_con)

        # 公司详情简介
        summary = ''
        try:
            summary = tree.xpath('//p[@id="J_COMMON_CompanyInfoDetailInfo"]/span/text()')[0].strip()
            print('summary', summary)
        except:
            print('summary', summary)

        # 公司主营产品
        scopes = ''
        try:
            scopes = tree.xpath('//span[@class="tb-value-data"]/text()')[2]
            print('scopes', scopes)
        except:
            print('scopes', scopes)
        sleep(3)
        

if __name__ == '__main__':
    login = login()
    login.sinin()
    login.parse_url()
    login.parse_detail()
    login.kill()




