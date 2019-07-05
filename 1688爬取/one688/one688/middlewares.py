# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from time import sleep
from scrapy.http import HtmlResponse


class One688DownloaderMiddleware(object):

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        model_urls = spider.model_urls
        bro = spider.bro
        if request.url in model_urls:

            bro.get(url=request.url)
            sleep(3)

            iframe = bro.find_element_by_xpath('//iframe')  # 找到“嵌套”的iframe
            bro.switch_to.frame(iframe)  # 切换到iframe
            sleep(2)

            bro.find_element_by_id('J_Quick2Static').click()
            sleep(2)

            bro.find_element_by_id('TPL_username_1').send_keys('辉哥又来啦')
            sleep(2)
            bro.find_element_by_id('TPL_password_1').send_keys('kong267871')
            sleep(2)
            bro.find_element_by_id('J_SubmitStatic').click()
            sleep(2)

            page_text = bro.page_source

            return HtmlResponse(url=bro.current_url, body=page_text, encoding='utf-8', request=request)

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
