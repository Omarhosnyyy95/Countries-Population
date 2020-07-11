import scrapy


class GdpDeptSpider(scrapy.Spider):
    name = 'gdp_dept'
    allowed_domains = ['worldpopulationreview.com/']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        rows = response.xpath('//table/tbody/tr')
        for row in rows:
            name = row.xpath('.//td[1]/a/text()').get()
            gdp_ratio = row.xpath('.//td[2]/text()').get()
            population = row.xpath('.//td[3]/text()').get()

            yield{
                'Country Name': name,
                'GDP Ratio': gdp_ratio,
                'Population': population
            }

