import scrapy


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['www.majorcineplex.com']
    start_urls = ['https://www.majorcineplex.com/en/main/']

    def parse(self, response):
        for movie in response.xpath("//div[@class = 'eachMovie']"):
            yield{
                'title': movie.xpath("normalize-space(.//h3[@class='nameMovieEn']/text())").get()
            }
