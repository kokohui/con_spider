# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy import Request
from ..items import One688Item
from selenium import webdriver
from selenium.webdriver import ChromeOptions


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'

    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 创建一个浏览器对象
    bro = webdriver.Chrome(executable_path=r'D:\chromedriver', chrome_options=option)

    model_urls = []

    def start_requests(self):
        url = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%D6%ED&button_click=top&earseDirect=false&n=y&netType=1%2C11&beginPage=2&offset=9'

        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        获取url列表
        :param response:
        :return:
        """
        # print(response.text)
        for num in range(1, 61):
            res_url_list = response.xpath('//*[@id="offer{}"]/div[@class="imgofferresult-mainBlock"]/div[1]/a/@href'.format(num)).extract()
            # 'https://login.1688.com/member/signin.htm?from=sm&Done=http://detail.1688.com/offer/567003895208.html'
            res_url_list_one = 'https://login.1688.com/member/signin.htm?from=sm&Done=' + res_url_list[0]

            self.model_urls.append(res_url_list_one)
            for res_url in res_url_list:
                print(res_url)
                print('.........................')
                # yield Request(res_url, callback=self.parse_detail)

    def parse_detail(self, response):
        print('parse_buy_list>>>')
        print(response)
        # res_title = response.xpath('//*[@id="mod-detail-title"]/h1/text()').extract()
        # print(res_title)





