import scrapy
from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net/en']

    script = '''

    function main(splash, args)
        
        splash.private_mode_enabled = false
        url = args.url
        assert(splash:go(url))
        assert(splash:wait(1))
        coins = assert(splash:select_all(".filterPanelItem___2z5Gb"))
        usd = coins[3]
        usd:mouse_click()
        assert(splash:wait(1))
        splash:set_viewport_full()
        return splash:html()  
    end

    '''
    def start_requests(self):
        yield SplashRequest(url="https://www.livecoin.net/en", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })



    def parse(self, response):
        for currency in response.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield{
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get(),
                'last price': currency.xpath(".//div[3]/span/text()").get(),
                'change(24h)': currency.xpath(".//div[4]//span/text()").get(),
                'high(24h)': currency.xpath(".//div[5]/span/text()").get(),
                'low(24h)': currency.xpath(".//div[6]//span/text()").get(),
            }
