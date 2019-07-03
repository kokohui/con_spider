# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import One688Item
from selenium import webdriver
from selenium.webdriver import ChromeOptions


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'

    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 创建一个浏览器对象
    bro = webdriver.Chrome(executable_path=r'C:\Users\Administrator\Desktop\爬虫+数据\爬虫day06\chromedriver.exe',
                           options=option)
    name = 'wangyi'

    def start_requests(self):
        url = 'https://login.1688.com/member/signin.htm?spm=b26110380.2178313.0.d3.51192253lcd8IR&Done=https%3A%2F%2Fs.1688.com%2Fcompany%2Fcompany_search.htm%3Fkeywords%3D%25B6%25FA%25BB%25FA%26button_click%3Dtop%26earseDirect%3Dfalse%26n%3Dy%26netType%3D1%252C11'


    # start_urls = ['https://s.1688.com/newbuyoffer/buyoffer_search.htm?keywords=%B6%FA%BB%FA&n=y&carrybuyoffer=true']
    #
    # def parse(self, response):
    #     """
    #     获取商品 产品, 供应, 求购 url
    #     :param response:
    #     :return:
    #     """
    #
    #     # 产品
    #     res_pro_url = response.xpath('//div[@class="searchtab-mod"]//li[1]/a/@href')[0].extract()
    #     print('res_pro_url', res_pro_url)
    #
    #     # 供应
    #     res_supply_url = response.xpath('//div[@class="searchtab-mod"]//li[2]/a/@href')[0].extract()
    #     print('res_supply_url', res_supply_url)
    #
    #     # 求购
    #     res_buy_url = response.xpath('//div[@class="searchtab-mod"]//li[3]/a/@href')[0].extract()
    #     print('res_buy_url', res_buy_url)
    #
    #     params = '?pageSize=60&from=marketSearch&beginPage=2'
    #     url = res_buy_url + params
    #
    #     yield Request(url=url, callback=self.parse_buy_list)
    #
    # def parse_buy_list(self, response):
    #     print('parse_buy_list>>>')
    #     res_detail_list = response.xpath('//div[@id="sm-offer-list"]/div[@class="im-offer-box"]//h3/a/@href').extract()
    #     for res_detail_url in res_detail_list:
    #         print(res_detail_url)



