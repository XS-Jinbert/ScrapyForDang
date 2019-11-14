# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.crawler import _get_spider_loader

# TODO：需要根据网站的不同新建一个文件夹
class ScrapyspPipeline(object):
    # 注意win系统文件命名规则：不能包含/,\,:,*,?,",<,>,|
    #revise_dict = {':':'：',}
    save_path = r''
    def __init__(self,settings):
        for name in _get_spider_loader(settings).list():
            self.spidername = name
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    # the method above is to get the spider name
    def process_item(self, item, spider):
        # Get the directory path
        spidername = spider.name
        save_path = os.path.join(self.save_path, spidername)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        # index_name:title,text,url
        FileName_ = item['title']
        if ':' in FileName_ or '?' in FileName_:
            FileName = FileName_.replace(':','：')
            FileName = FileName.replace('?','？')
        else:
            FileName = FileName_
        path = os.path.join(save_path,FileName) + '.txt'

        with open(path,'w+',encoding='utf-8') as f:
            f.write(item['url'])
            f.write('\n')
            f.write(item['Time_Stamp'])
            f.write('\n')
            f.write(item['text'])
        return item
