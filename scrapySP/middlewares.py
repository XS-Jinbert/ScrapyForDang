# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from helper import MyWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class ScrapyspSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyspDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # TODO:it only uesd in TNYT, should be revised
        # Called for each request that goes through the downloader
        # middleware.
        # 引入click_page进行检查，这是因为爬虫存在二次链接
        if 'query' in request.url:
            if spider.name == 'TNYT':
                return self._TNYT_Request(request)
            if spider.name == 'WST':
                return self._WST_Request(request)
        return None
    def _WST_Request(self,request):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # TODO:how to change the header?
        #dcap = DesiredCapabilities.CHROME.copy()
        #dcap['chrome.switches'] = ['--user-agent=\
        #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36']
        #dcap['acceptSslCerts'] = True
        #dcap['acceptInsecureCerts'] = True
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        driver = webdriver.Chrome()
        # return navigator.userAgent
        # '//a[@data-ng-bind-html="doc.headline"]'
        driver.get(request.url)
        driver.implicitly_wait(5)
        true_page = driver.page_source
        driver.close()
        return HtmlResponse(request.url, body=true_page, encoding='utf-8', request=request)
    def _TNYT_Request(self,request):
        if 'query' not in request.url:
            return None
            # Selenuim do not support PhantomJS anymore, ues headless chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # TODO: headless chrome cannot click: may the chromedriver is too old
        driver = webdriver.Chrome(chrome_options=chrome_options)

        driver.get(request.url)
        # may the web cannot be fully displayed.So we should wait for a while.
        # but the fucntion ultil is more better
        # driver.implicitly_wait(10)
        time.sleep(5)
        pattern = '//*[@id="site-content"]/div/div[2]/div[2]/div/button'
        # if use forced waitting function time.sleep. it's hard to set the wait time
        while True:
            # TODO:the function is not ok though
            # TODO: how to stop click automatically?(may write a code that check the new item)
            loc = MyWait(driver, 5, poll_frequency=1).until(lambda dr: dr.find_element_by_xpath(pattern))
            if loc:
                time.sleep(5)
                # driver.execute_script('arguments[0].click();', loc)
                try:
                    loc.click()
                except:
                    continue
            else:
                break

        time.sleep(3)
        true_page = driver.page_source
        driver.close()
        return HtmlResponse(request.url, body=true_page, encoding='utf-8', request=request)
        
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        #return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
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
