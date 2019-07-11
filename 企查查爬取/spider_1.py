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
    """爬虫类"""

    def __init__(self):

        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 创建一个浏览器对象
        self.bro = webdriver.Chrome(executable_path=r'D:\chromedriver', chrome_options=option)
        # self.bro = webdriver.Chrome(executable_path=r'C:\谷歌selenium驱动\chromedriver', chrome_options=option)
        self.url = 'https://www.qichacha.com/user_login?back=%2F'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        self.cookies = ''
        self.page_text = ''
        self.list_url_dedail = []
        self.cookies_dict = dict()
        self.dict_data = {}  # 返回数据

    def sinin(self):
        """登录"""

        self.bro.get(url=self.url)
        sleep(3)

        # iframe = self.bro.find_element_by_xpath('//iframe')  # 找到“嵌套”的iframe
        # self.bro.switch_to.frame(iframe)  # 切换到iframe
        # sleep(2)
        self.bro.find_elements_by_id('normalLogin')[0].click()
        sleep(2)

        # self.bro.find_element_by_id('nameNormal').send_keys('17686846682')
        # sleep(2)
        # self.bro.find_element_by_id('TPL_password_1').send_keys('kong267871')
        # sleep(2)
        # self.bro.find_element_by_id('J_SubmitStatic').click()
        # sleep(2)
        # try:
        #     self.bro.find_element_by_xpath('//*[@id="s-module-overlay"]/div[2]/div/div[2]/em[4]').click()
        #     sleep(2)
        # except:
        #     print('没有')
        #
        # # 获取session
        # self.cookies = self.bro.get_cookies()
        # with open("cookies.txt", "w") as fp:
        #     json.dump(self.cookies, fp)
        #
        # self.page_text = self.bro.page_source

    def kill(self):
        """关闭selenium"""
        self.bro.quit()






if __name__ == '__main__':
    login = login()
    login.sinin()
    # login.kill()




