
# TODO:点击搜索扔不稳定
import scrapy
import re
import os
import requests
from scrapySP.items import NewsItem
from helper import genor_search_vocabulary, starttime, stoptime, time_transform
import random


class QuotesSpider(scrapy.Spider):
	name = "TNYT"
	keywords = genor_search_vocabulary()
	links = []


	def start_requests(self):
		date_search = '12%20Months'
		search_list = []
		search_temp = input('Please input what you want to search')
		while search_temp != '':
			search_list.append(search_temp)
			search_temp = input('')
		s = '%20'
		search_result = s.join(search_list)
		url = 'https://www.nytimes.com/search?dropmab=false&endDate={}&query={}&sort=best&startDate={}'\
			.format(stoptime, search_result, starttime)

		yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):

		# the parse content
		#1.Getting the selector 
		LinksSelector = response.css('main').css('li')
		#2. Checking the content is the main conteng not ad.
		main_web = 'https://www.nytimes.com'
		true_id = 'search-bodega-result'
		links_follow = []
		# TODO:利用Post无法实现show more功能
		#headers, url = self._show_more()
		#a = scrapy.FormRequest(url=url,formdata={},callback=self.show_more)
		for s in LinksSelector:
			id = s.css('li::attr(data-testid)').get()
			if id == true_id:
				# Get the href and check whether the key word in the article 
				sub_web = s.css('a::attr(href)').get()
				time_pattern = re.compile('time.*?>(.*?)</time>', re.S)
				time_stamp = time_transform(re.findall(time_pattern, s.extract())[0]+', 2019')
				if time_stamp < starttime or time_stamp > stoptime:
					continue
				item = NewsItem()
				item['Time_Stamp'] = time_stamp
				yield scrapy.Request(url=main_web+sub_web, callback=self.check,meta={'data':item})
		# This is to check whether the show_more clik function works or not
				# links_follow.append(main_web+sub_web)
		#if len(links_follow) < 11:
		#	raise IOError("the click simulate doesn't work")
		#else:
		#	print('The num of links is {}'.format(len(links_follow)))
		#for link in links_follow:
		#	# Attention: 记录一个文件，有标题， 有对应网站
		#	yield scrapy.Request(url=link, callback=self.check)
		#with open(filename, 'wb') as f:
		#	f.write(response.body)

	def check(self,response):
		# return a list with text content and url relative 
		# choose the content
		index = 1
		text_list = []
		while True:
			res = response.xpath("(//p[re:match(@class,'css-exrw3m evys1bk0')])[{}]/text()".format(str(index)))
			if res:
				temp_s = res.extract()
				s_ = str()
				s = s_.join(temp_s)
				text_list.append(s)
				index+= 1
			else:
				break
		temp=str('\n')
		# Must use new variable to save the str after .join
		text = temp.join(text_list) # get the whole page content
		for keyword in self.keywords:
			if keyword in text:
				title = response.xpath('//h1//text()').extract()[0]
				#yield self._record([text,title,response.url])
				item = response.meta['data']
				item['url'] = response.url
				item['text'] = text
				item['title'] = title
				yield item
				break
	#def url_genor(self):
		#startDate = input('please input your startDate like "20190925"')
		#endDate = input('please input your endDate like "20191012"')
		#search_list = []
		## 回车结束
		#while search_temp != '':
		#	search_list.append(search_temp)
		#	search_temp =  input('please input your search word one by one, and enter will be the end')
		#s = '%20'
		#search_result = s.join(search_list)
		#link = 'https://www.nytimes.com/search?dropmab=false&endDate={}&query={}&sort=best&startDate={}'.format(endDate,search_result,startDate)
		#print('the search link is %s'%link)
