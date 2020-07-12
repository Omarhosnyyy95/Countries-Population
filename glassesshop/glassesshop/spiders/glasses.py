import scrapy


class GlassesSpider(scrapy.Spider):
    name = 'glasses'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    
    def get_product_price(self, selector):
        original_price = selector.xpath(".//div[@class='col-6 col-lg-6']/div[@class='p-price']//span/text()").get()
        discounted_price = selector.xpath(".//div[@class='col-6 col-lg-6']/div[@class='p-price']//span[@class='color-red']/text()").get()
        if original_price is not None:
            return original_price
        else:
            return discounted_price



    def parse(self, response):

        # Products without the ad
        products = response.xpath("(//div[@id='product-lists']/div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row'])[not(self::div/a[@href='/buy-one-get-one-free'])]")
        for product in products:
            product_url = product.xpath(".//div[@class = 'product-img-outer']/a/@href").get()
            product_image = product.xpath(".//div[@class = 'product-img-outer']/a/img[@class = 'lazy d-block w-100 product-img-default']/@src").get()
            product_name = product.xpath(".//div[@class = 'p-title']/a/text()").get()

            yield{
                'product_url': product_url,
                'product_image': product_image,
                'product_name': product_name,
                'product_price': self.get_product_price(product)
            }

        next_page = response.xpath("//li[@class = 'page-item']/a[@rel='next']/@href").get()
        if next_page:
            yield scrapy.Request(url = next_page, callback=self.parse)
