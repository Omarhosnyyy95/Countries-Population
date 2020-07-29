
import scrapy
from scrapy.selector import Selector
import json
 
 
class ListingsSpider(scrapy.Spider):
    name = 'listings'
 
    allowed_domains = ['www.centris.ca']
 
    handle_httpstatus_list = [555]
 
    position = {
        "startPosition": 0
    }
 
    def start_requests(self):
        yield scrapy.Request(
            url='https://www.centris.ca/UserContext/Lock',
            method="POST",
            body=json.dumps({
                "uc": 0
            }),
            headers={
                'content-type': 'application/json'
            },
            callback=self.lock,
        )
    
    def lock(self, response):
        uck = response.text
        yield scrapy.Request(
            url='https://www.centris.ca/UserContext/UnLock',
            method='POST',
            body=json.dumps({
                'uc': 0,
                'uck': uck
            }),
            headers={
                'content-type': 'application/json', 
                'x-centric-uck': uck,
                'x-centris-uc': 0
            },
            callback=self.send_query,
            meta={
                'uck': uck
            }
        )
 
    def send_query(self, response):
        uck = response.meta['uck']
        query = {
 
            "query": {
                "UseGeographyShapes": 0,
                "Filters": [
                    {
                        "MatchType": "CityDistrictAll",
                        "Text": "Montréal (All boroughs)",
                        "Id": 5
                    }
                ],
                "FieldsValues": [
                    {
                        "fieldId": "CityDistrictAll",
                        "value": 5,
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "SellingType",
                        "value": "Rent",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "Category",
                        "value": "Residential",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "LandArea",
                        "value": "SquareFeet",
                        "fieldConditionId": "IsLandArea",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "RentPrice",
                        "value": 0,
                        "fieldConditionId": "ForRent",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "RentPrice",
                        "value": 1500,
                        "fieldConditionId": "ForRent",
                        "valueConditionId": ""
                    }
                ]
            },
            "isHomePage": True
 
        }
        yield scrapy.Request(
            url="https://www.centris.ca/property/UpdateQuery",
            method="POST",
            body=json.dumps(query),
            headers={
                "Content-Type": "application/json",
                "x-centris-uck": uck,
                "x-centris-uc": 0
            },
            callback=self.update_query
        )
 
    def update_query(self, response):
        yield scrapy.Request(
            url="https://www.centris.ca/Property/GetInscriptions",
            method="POST",
            body=json.dumps(self.position),
            headers={
                "Content-Type": "application/json",
            },
            callback=self.parse
        )
 
    def parse(self, response):
        resp_dict = json.loads(response.body)
        html = resp_dict.get('d').get('Result').get('html')
        sel = Selector(text=html)
        listings = sel.xpath("//div[@data-id='templateThumbnailItem']")
        for listing in listings:
            category = listing.xpath(".//div[@class='location-container']/span[@class='category']/div//text()").get(),
            price = listing.xpath(".//div[@class='price']//span/@content").get(),
            address = listing.xpath(".//span[@class='address']/div[1]//text()").get()
            yield{
                'category': category,
                'price': price,
                'address': address
            }