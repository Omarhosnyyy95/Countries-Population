import scrapy
from scrapy_splash import SplashRequest

class QuartierSpider(scrapy.Spider):
    name = 'quartier'
    allowed_domains = ['www.majorcineplex.com']

    def start_requests(self):
        yield SplashRequest(url="https://www.majorcineplex.com/booking2/search_showtime/cinema=106", 
                            callback=self.parse, 
                            endpoint="execute", 
                            args={
                                'lua_source': self.script,
                                #'timeout': 90
                                },
                            headers={
                                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                                'Referer': 'www.majorcineplex.com'
                                }
                        )


    def parse(self, response):
        for theatre in response.xpath("//div[@class='book_st_row']"):
            yield{
                'theatre_number': theatre.xpath(".//div[@class='book_st_theatre_no']/text()").get(),
                'movies': theatre.xpath(".//div[@class='book_st_mvname']/text()").getall(),
                'genre': theatre.xpath(".//span[@class='mvdesc mvdescbf']/text()").getall(),
                'duration': theatre.xpath(".//span[@class='mvdesc']/text()").getall(),
                'available_times': theatre.xpath(".//a[contains(@class, 'nextst')]/text()").getall()
            }        
