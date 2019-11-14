import scrapy 

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
	    #print(response.url)
        page = response.url.split("")[-2]
		#print(page)
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
		# 下列代码用于调试shell 
		#if ".org" in response.url:
        #    from scrapy.shell import inspect_response
        #    inspect_response(response, self)

		
		