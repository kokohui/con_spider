# import scrapy
from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
import requests
from lxml import etree
import json
from bs4 import BeautifulSoup
import re

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


            # 标题
            res_title = ''
            try:
                res_title = tree.xpath('//h1/text()')[0]
                print('res_title', res_title)
            except:
                print('res_title', res_title)

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

            # 联系人
            con_man = ''
            try:
                con_man = tree.xpath('//a[@class="link name"]/text()')[0].strip()
                print('con_man', con_man)
            except:
                print('con_man', con_man)

            # 联系电话
            con_tel = ''
            try:
                con_tel = tree.xpath('//dd[@class="mobile-number"]/text()')[0].strip()
                print('con_tel', con_tel)
            except:
                print('con_tel', con_tel)

            # 联系地址
            con_adress = ''
            try:
                con_adress = tree.xpath('//div[@class="item address fd-clr"]/span/text()')[0]
                print('con_adress', con_adress)
            except:
                print('con_adress', con_adress)

            # 公司详情url
            con_url = ''
            try:
                con_url = tree.xpath('//*[@id="topnav"]/div/ul/li[@data-page-name="creditdetail"]/a/@href')[0].strip()
                print('con_url', con_url)
            except:
                print('con_url', con_url)
            sleep(3)
            
            self.parse_con(self, con_url)

    @staticmethod
    def parse_con(self, con_url):
        """解析公司部分内容"""
        res_con = s.get(url=con_url, headers=self.headers, cookies=self.cookies_dict).text
        # res_con.encoding = 'utf-8'
        # res_con = res_con.content
        print(res_con)
        # tree = etree.HTML(res_con)
        # soup = BeautifulSoup(res_con, 'lxml')
        # 
        # # 公司详情简介
        # summary = ''
        # try:
        #     # summary = tree.xpath('//div[@class="info-left"]/p[@class="simple-info"]/span/text()')
        #     # summary_1 = tree.xpath('//div[@class="info-left"]/p[@class="simple-info"]/span/text()')
        #     summary = soup.select('#J_COMMON_CompanyInfoSimpleInfo > span')
        #     summary_1 = soup.select('#J_COMMON_CompanyInfoSimpleInfo > span').text
        #     print('summary', summary)
        #     print('summary_1', summary_1)
        # except:
        #     print('summary', summary)
        # 
        # # 公司主营产品
        # scopes = ''
        # try:
        #     scopes = soup.select('')
        #     scopes = tree.xpath('//div[@class="info-right"]//tr[3]/td[2]/p/span[1]/text()')
        #     print('scopes', scopes)
        # except:
        #     print('scopes', scopes)
        sleep(3)
        

if __name__ == '__main__':
    login = login()
    login.sinin()
    login.parse_url()
    login.parse_detail()
    login.kill()




