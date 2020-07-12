import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.tinydeal.com']
    start_urls = ['https://www.tinydeal.com/specials.html']

    def parse(self, response):
        products = response.xpath("//div[@class='p_box_wrapper']/li")
        for product in products:
            product_name = product.xpath(".//a[@class='p_box_title']/text()").get()
            product_url = response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get())
            discounted_price = product.xpath(".//div[@class='p_box_price']/span[@class='productSpecialPrice fl']/text()").get()
            original_price = product.xpath(".//div[@class='p_box_price']/span[@class='normalprice fl']/text()").get()
            yield{
                'product_name': product_name,
                'product_url': product_url,
                'discounted_price': discounted_price,
                'original_price': original_price,
                'User-Agent': response.request.headers['User-Agent'] # Spoofing request headers
            }
        
        # next page button is an absolute url so we can use scrapy.Request
        next_page = response.xpath("//a[@class='nextPage']/@href").get()

        if next_page:
            yield scrapy.Request(url = next_page, callback= self.parse)

