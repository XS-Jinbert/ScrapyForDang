#-*- coding:utf-8 -*-

from scrapy.cmdline import execute
import os
import sys

if __name__ == '__main__':
    #添加当前项目的绝对地址
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    #执行 scrapy 内置的函数方法execute，  使用 crawl 爬取并调试，最后一个参数jobbole 是我的爬虫文件名
    #for name in  ['WST','TNYT','CT','LAT']:
    execute(['scrapy', 'crawl', 'CT'])
