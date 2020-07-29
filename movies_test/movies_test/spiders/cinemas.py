import scrapy


class CinemasSpider(scrapy.Spider):
    name = 'cinemas'
    allowed_domains = ['www.majorcineplex.com']
    start_urls = ['https://www.majorcineplex.com/cinema/']

    def parse(self, response):
        for cinema in response.xpath("//div[@class='eachlistcinemaEn']"):
            yield{
                'cinema_name': cinema.xpath("normalize-space(.//h3/text())").get()
            }
        
