import scrapy
import re
import os
from scrapySP.items import NewsItem
from helper import genor_header
import re
from helper import time_transform, genor_search_vocabulary, starttime, stoptime
# todo：User-Agent is not enough , to find what else is need
# todo: xpath cannot extract the lower layers'information
# todo:here are some data about video and I quit it
# Must use webdriver to get the content. the reason from 'https://ask.csdn.net/questions/259264'
# use-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36

class QuotesSpider(scrapy.Spider):
    name = "WST"
    keywords = genor_search_vocabulary()
    index = 0
    def start_requests(self):
        self.cookie = r'APID=UP3c602ca2-b63f-11e7-8fd2-0253d1243bda; UMAP=MTAwNzoxNTIyOTc5NjU4OzEwMDY6MTUyMjk4MTEwOTsxMDAzOjE1Mzc2NzY5Mjk7NDAwMToxNTA3Njk2MDM1; IDSYNC="s~1c4t:38~1igv:6k~1igv:6l~1k5k:a4~1igv:di8~1ifo:dns~1igv:e2d~1igv:eax~1d47:ehg~1igv:exi~1igv:f43~1igv:fda~1igv:nan~1a0x:13b3~1igv:13mm~1igv:16pp~1igv:175s~1kqw:175u~1hbf:175x~1ifo:1769~1jto:176e~1ifo:176s~1k4e:1770~1k5k:18a7~1igv:18bj~1kc2:18gs~1ifo:18ul~1igv:18um~1igv:18vc~1igv:18vm~1igv:18wc~1igv:1760~1jr0:17kh~1jr0:175w~1j4a:172t~1jr0:1762~1jr0:1766~1jr0:1772~1jto:173k~1k5k"; ADMARK=Sat,  2 Nov 2019 11:54:40 GMT'
        yield scrapy.Request(url=self.url_genor(), callback=self.parse,headers=genor_header(self.cookie))

    def parse(self, response):
        content_pattern = '//a[@data-ng-bind-html="doc.headline"]' #//div[@class="pb-feed-headline ng-scope"]
        content_links = response.xpath(content_pattern)
        for index,content in enumerate(content_links):
            date = time_transform(self._date_extract(response,index))
            if date < starttime or  date > stoptime:
                continue
            link = content.xpath('@href').extract()[0]
            title_list = content.xpath('text()').extract()
            title = str()
            title = title.join(title_list)
            item = NewsItem()
            item['title'] = title
            item['Time_Stamp'] = date
            yield scrapy.Request(url=link,callback=self._check,meta={'data':item},headers=genor_header(self.cookie))
        # Link to next page
        if content_links:
            url = self.url_genor()
            yield scrapy.Request(url=url, callback=self.parse,headers=genor_header(self.cookie))

    # To get the date info
    def _date_extract(self,response,index):
        try:
            date = response.xpath('//span[@class="pb-timestamp ng-binding"]')[index].xpath('text()').extract()[0]
        except:
            # TODO: Find nothing
            date = '19980312'
            print('The error url is {}'.format(response.url))
        return date

    def _check(self, response):
        # return a list with text content and url relative
        # choose the content
        index = 1
        text_list = []

        # Cause some word get hyperlink,So we should join them.
        while True:
            res = response.xpath('(//p[@class="font--body font-copy color-gray-darkest ma-0 pad-bottom-md undefined"])[{}]/text()'\
                                       .format(index))
            if res:
                temp_s = res.extract()
                s_ = str()
                s = s_.join(temp_s)
                text_list.append(s)
                index += 1
            else:
                break
        temp = str('\n')
        # Must use new variable to save the str after .join
        text = temp.join(text_list)  # get the whole page content
        for keyword in self.keywords:
            if keyword in text:
                # yield self._record([text,title,response.url])
                item = response.meta['data']
                item['url'] = response.url
                item['text'] = text
                yield item
                break

    def url_genor(self):
        date_search = '12%20Months'
        search_list = []
        search_temp = input('Please input what you want to search(one by one word)\n')
        while search_temp != '':
            search_list.append(search_temp)
            search_temp = input('')
        s = '%20'
        search_result = s.join(search_list)
        url = 'https://www.washingtonpost.com/newssearch/?datefilter={}&query={}&sort=Relevance&startat={}#top'\
                .format(date_search, search_result, self.index)
        self.index += 20
        return url