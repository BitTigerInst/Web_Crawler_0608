import scrapy
import re
from scrapy.selector import Selector

from web_crawler_0608.items import TruliaWebCrawlerItem


class TruliaSpider(scrapy.Spider):
    name = "trulia"
    allowed_domains = ["trulia.com"]

    start_urls = [

        "http://www.trulia.com/CA/San_Francisco/"
    ]

    def parse(self, response):
        page = Selector(response)

        divs = page.xpath('//div[@class= "card backgroundBasic"]')

        for div in divs:
            item = TruliaWebCrawlerItem()

            # To get the property link
            item['href'] = div.xpath('.//a/@href').extract_first()
            str = item['href'].split("-", 1)
            item['mortgage_id'] = re.match(r'/property/(.*)', str[0]).group(1)
            item['address'] = str[1]       
    
            # this method sometimes does not work when the address is complicated, so I update it 
            #To get the city, state, zip code
            address_detail = str[1].split("-")
            item['city'] = "{0} {1}".format(address_detail[3], address_detail[4])
            item['state'] = address_detail[5]
            item['zip_code'] = address_detail[6]
            #item['city'] = "{0} {1}".format(address_detail[3], address_detail[4])
            item['state'] = address_detail[len(address_detail)-2]   # the second last is state
            item['zip_code'] = address_detail[len(address_detail)-1] # the last is zipcode

            #To get the mortgage value and mortgage neighborhood
            item['mortgage_value'] = div.xpath('.//span[@class="h4 man pan typeEmphasize "]/text()'). \
                extract_first()
            item['neighborhood'] = div.xpath('.//div[@class="typeTruncate"]/text()'). \
            item['mortgage_value'] = div.xpath('.//span[@class="cardPrice h4 man pan typeEmphasize noWrap typeTruncate "]/text()'). \
                extract_first()
            item['neighborhood'] = div.xpath('.//div[@class="typeTruncate"]/text()').extract_first()
            item['city'] = item['neighborhood'].split(",")[len(item['neighborhood'].split(","))-2]    # city is second to the last
            item['address'] = div.xpath('.//a/@alt').extract_first()


            # To get the numbers of bedrooms and bathrooms
            item['bedroom'] =  div.xpath('.//li[@class="pln"]/text()').extract_first()
            item['bathroom'] =  div.xpath('.//li[@class=""]/text()').extract_first()
            #item['sqft'] =  div.xpath('.//li[@class=""]/text()').extract()
            
            yield item

