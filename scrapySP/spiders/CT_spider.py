

# TODO:learn what the yield actuall is?
# TODO:there is a limit reading
# TODO:occur the monthly free article limit
import scrapy
import re
import os
from scrapySP.items import NewsItem
from helper import genor_search_vocabulary, starttime, stoptime, time_transform
# TODO（11、12）:CT产生了大量的date loss要检查
# CT do not need VPN and but the robotset must be False
# count = 0
class QuotesSpider(scrapy.Spider):
    name = "CT"
    keywords = genor_search_vocabulary()
    links = []
    index = 1
    # cookie = r'tuuid=cf9a2465-a67f-4fa7-a69f-31ab1ede69bc; c=1572575327; tuuid_lu=1572575330; lb1s=!0,3,341940242; ab1d=!0,743.96,341940242'
    def start_requests(self):
        yield scrapy.Request(url=self.url_genor(), callback=self.parse)

    def parse(self, response):
        # ---------------------------------
        # First we do content get first
        # the crop[:-2] is a trick cause CT the last two link is useless
        links_follow = response.xpath('//ul[@class="flex-grid story--clln"]//\
                        li[@class="col col-desktop-3 col-tablet-3 col-mobile-6"]')
        #global count
        for href in links_follow:
            base_url = r'https://www.chicagotribune.com/'
            data_dict = self._extract(href)
            item = NewsItem()
            item['title'] = data_dict['title']
            if data_dict['time']:
                time_stamp = time_transform(data_dict['time'])
                if time_stamp < starttime or time_stamp > stoptime:
                    continue
                item['Time_Stamp'] = time_stamp
            else:
                continue
                #count += 1
                #print("The date-lossing' url is {}, and the total count is {}".format(response.url,count))
                #item['Time_Stamp'] = 'Date Loss'
            yield scrapy.Request(url=base_url + data_dict['link'], callback=self.check,meta={'data':item})
        # ---------------------------------------
        # if links_follow is not emptyrecursion continue
        if links_follow:
            next_url = self.url_genor()
            yield scrapy.Request(url=next_url, callback=self.parse)

    def check(self, response):
        # return a list with text content and url relative
        # choose the content
        temp_list = response.xpath("//div[@class=' crd--cnt ']//text()").extract()
        # why use filter, cause through this xpath formula we will get a lots of blank element, we need remove them all
        text_list = list(filter(lambda a: a != ' ', temp_list))
        temp = '\n'
        # Must use new variable to save the str after .join
        text = temp.join(text_list)  # get the whole page content
        for keyword in self.keywords:
            if keyword in text:
                # https://www.chicagotribune.com//business/ct-biz-kohls-penney-retail-results-20190521-story.html
                # The middle market is collapsing' at Kohl's, J.C. Penney
                item = response.meta['data']
                item['url'] = response.url
                item['text'] = text
                yield item
                break
    def url_genor(self):

        search_list = []
        search_temp = input('Please input what you want to search(one by one word)\n')
        while search_temp != '':
            search_list.append(search_temp)
            search_temp = input('')
        s = '+'
        search_result = s.join(search_list)
        url = 'https://www.chicagotribune.com/search/{}/1-y/ALL/score/{}/'.format(search_result, self.index)
        self.index += 1
        return url

    def _extract(self,href):
        # return a dict whose keys include link title and time
        data_dict = {}
        text = href.extract()
        link_pattern = re.compile('<a class="no-u" href="(.*?)"',re.S)
        data_dict['link'] = re.findall(link_pattern, text)[0]
        title_pattern = re.compile('<a class="no-u" href=".*?">(.*?)</a>',re.S)
        data_dict['title'] = re.findall(title_pattern, text)[0]
        try:
            time_pattern = re.compile('<span class="timestamp "> (.*?) </span>',re.S)
            data_dict['time'] = re.findall(time_pattern, text)[0].capitalize()
        except:
            data_dict['time'] = None
        return data_dict
'''
    # Attention: there is index value we should add it 
	https://www.chicagotribune.com/search/china%20threat/1-y/ALL/score/index/
    def url_genor(self):
        search_temp = input('please input your search word one by one, and enter will be the end')
        #while search_temp != '':
		#	search_list.append(search_temp)
		#	search_temp =  input('')
		#s = '%20'
		#search_result = s.join(search_list)
		date = input('input the date range you want,like"1-y means in one year, 100-d measn in 100 days"')
		url = 'https://www.chicagotribune.com/search/{}/{}/ALL/score/{}/'.format(search_result,date,self.index)
		return url 
'''