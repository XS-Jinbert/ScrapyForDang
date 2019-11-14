from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import calendar
import pandas as pd
from docx import Document
starttime = '20190901'
stoptime = '20191031'
class MyWait(WebDriverWait):
    def until(self, method, message=''):
        """Calls the method provided with the driver as an argument until the \
        return value is not False."""
        screen = None
        stacktrace = None

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                screen = getattr(exc, 'screen', None)
                stacktrace = getattr(exc, 'stacktrace', None)
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        return False

def genor_header(cookie):
	# User-Agent列表，这个可以自己在网上搜到，用于伪装浏览器的User Agent
	USER_AGENTS = [
		"Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
		"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
		"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
		"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
		"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
		"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
		"Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
		"Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
		"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
		"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
		"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
		"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
		"Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
		"Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
		"Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
		"Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "
	]
	# IP地址列表，用于设置IP代理
	IP_AGENTS = [
		"http://58.240.53.196:8080",
		"http://219.135.99.185:8088",
		"http://117.127.0.198:8080",
		"http://58.240.53.194:8080"
	]

	# 设置IP代理
	proxies = {"http": random.choice(IP_AGENTS)}

	# =============================================================================
	# 上面的设置是为了应对网站的反爬虫，与具体的网页爬取无关
	# =========================;

	# 设置requests请求的 headers
	# the key name must be correct
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',  # 设置get请求的User-Agent，用于伪装浏览器UA
		#'Cookie': cookie,
		#'Connection': 'keep-alive',
		#'Accept': '*/*',
		#'Accept-Encoding': 'gzip, deflate, br',
		#'Accept-Language': 'zh-CN,zh;q=0.9',
		#'origin': 'https://www.nytimes.com',
		#'Referer': 'https://www.nytimes.com/search?dropmab=false&endDate=20191012&query=china%20threat%20&sort=best&startDate=20190925',
		#'content-length':'426',
		#'content-type':'application/json',
	}
	return headers

# TODO:应该添加一个原生模版 20190930
def time_transform(s):
	# Fuck LAT cause of diferrent format for date
	def _trans1(s):
		# example:Oct. 29, 2019
		try:
			s_remain = s[4:]
			m_in_EN = s[:3]
			m = list(calendar.month_abbr).index(m_in_EN)
			s_temp = str(m)+s_remain
			timearray = time.strptime(s_temp,'%m %d, %Y')
			date = time.strftime('%Y%m%d',timearray)
			return date
		except:
			return None
	def _trans2(s):
		#example:514, 2019
		try:
			timearray = time.strptime(s, '%m%d, %Y')
			date = time.strftime('%Y%m%d',timearray)
			return date
		except:
			return None
	def _trans3(s):
		#example:Oct 29, 2019
		try:
			s_remain = s[3:]
			m_in_EN = s[:3]
			m = list(calendar.month_abbr).index(m_in_EN)
			s_temp = str(m) + s_remain
			timearray = time.strptime(s_temp, '%m %d, %Y')
			date = time.strftime('%Y%m%d', timearray)
			return date
		except:
			return None
	def _trans4(s):
		try:
			# example: April 5, 2019
			s_remain_ = s.split(' ')[1:]
			s_remain=' '
			s_remain = s_remain.join(s_remain_)
			m_in_EN = s[:3]
			m = list(calendar.month_abbr).index(m_in_EN)
			s_temp = str(m) + s_remain
			timearray = time.strptime(s_temp, '%m%d, %Y')
			date = time.strftime('%Y%m%d', timearray)
			return date
		except:
			return None
	method = [_trans3,_trans1,_trans2,_trans4]
	for m in method:
		date = (lambda x:m(x))(s)
		if date:
			return date
	#TODO:If all the method cannot work.I quit,hope someday someone will fix it
	birth = '19980312'
	return birth

def genor_search_vocabulary():
	# path=r''
	# the doc file will use for filter the atricle
	return ['china']