
# TODO: the time_stamp here is big problem
import scrapy
import re
import os
from scrapySP.items import NewsItem
from helper import time_transform, genor_search_vocabulary, starttime, stoptime
# TODO: Cause we can get the time from the title and we shold make a filter to make sure date(like 2019-10-25 in our range)
# LAT do not need VPN and but the robotset must be False
class QuotesSpider(scrapy.Spider):
    name = "LAT"
    keywords = genor_search_vocabulary()
    index = 1
    def start_requests(self):
        yield scrapy.Request(url=self.url_genor(), callback=self.parse)

    def parse(self, response):
        content_pattern = '//div[@class="PromoMedium-content"]'
        content_follow = response.xpath(content_pattern)
        # TODO: cannot use xpath twice? And I used index method to get title and date
        for i in range(len(content_follow)):
            date_pattern = '//div[@class="PromoMedium-content"]/div[@class="PromoMedium-timestamp"]/@data-date'
            date = time_transform(response.xpath(date_pattern)[i].extract()) # Oct. 15, 2019
            if date > stoptime or date < starttime:
                continue
            temp_pattern = '//div[@class="PromoMedium-content"]//div[@class="PromoMedium-title"]//a[@class="Link"]'
            temp = response.xpath(temp_pattern)[i]
            link = temp.xpath('@href').extract()[0]
            title = temp.xpath('text()').extract()[0]
            item = NewsItem()
            item['title'] = title
            item['Time_Stamp'] = date
            yield scrapy.Request(url=link, callback=self.check, meta={'data': item})
        # ---------------------------------------
        # if links_follow is not emptyrecursion continue
        if content_follow:
            next_url = self.url_genor()
            yield scrapy.Request(url=next_url, callback=self.parse)

    # with open(filename, 'wb') as f:
    #	f.write(response.body)

    def check(self, response):
        # return a list with text content and url relative
        # choose the content
        text_list = response.xpath("//div[@class='RichTextArticleBody']//p//text()").extract()
        temp = str('\n')
        # Must use new variable to save the str after .join
        text = temp.join(text_list)  # get the whole page content
        for keyword in self.keywords:
            if keyword in text:
                item = response.meta['data']
                item['url'] = response.url
                item['text'] = text
                yield item
                break

    # with open(file_path,'w') as f:
    #	f.write(fileurl)
    #	f.write('\n')
    #	f.write(filetext)
    def url_genor(self):
        search_list = []
        search_temp = input('Please input what you want to search(one by one word)\n')
        while search_temp != '':
            search_list.append(search_temp)
            search_temp = input('')
        s = '%20'
        search_result = s.join(search_list)
        url = 'https://www.latimes.com/search?q={}&p={}'.format(search_result,self.index)
        self.index += 1
        return url
'''
# LAT_spider date will use judge method and it's web cannot filter the time stamp 
search_temp =  input('please input your search word one by one, and enter will be the end')
#while search_temp != '':
		#	search_list.append(search_temp)
		#	search_temp =  input('')
		#s = '%20'
		#search_result = s.join(search_list)
		#startDate = input('please input your startDate like "20190925"')
		#endDate = input('please input your endDate like "20191012"')
		url = 'https://www.latimes.com/search?q={}&p={}'.format(search_result,self.index)
		return url 
'''