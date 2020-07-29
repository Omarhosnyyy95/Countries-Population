import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.majorcineplex.com']
    start_urls = ['http://www.majorcineplex.com/']

    def parse(self, response):
        pass
