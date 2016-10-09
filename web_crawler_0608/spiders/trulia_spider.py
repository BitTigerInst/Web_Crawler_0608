import scrapy
import re
from scrapy.selector import Selector

from web_crawler_0608.items import TruliaWebCrawlerItem




class TruliaSpider(scrapy.Spider):
    name = "trulia"
    allowed_domains = ["trulia.com"]

    start_urls = ["https://www.trulia.com/NJ/Atlantic_City/",
                  "https://www.trulia.com/NJ/Barnegat/",
                  "https://www.trulia.com/NJ/Bayville/",
                  "https://www.trulia.com/NJ/Bloomfield/",
                  "https://www.trulia.com/NJ/Brick/",
                  "https://www.trulia.com/NJ/Bridgeton/",
                  "https://www.trulia.com/NJ/Brigantine/",
                  "https://www.trulia.com/NJ/Browns_Mills/",
                  "https://www.trulia.com/NJ/Burlington/",
                  "https://www.trulia.com/NJ/Camden/",
                  "https://www.trulia.com/NJ/Cape_May_Court_House/",
                  "https://www.trulia.com/NJ/Cherry_Hill/",
                  "https://www.trulia.com/NJ/Clifton/",
                  "https://www.trulia.com/NJ/East_Orange/",
                  "https://www.trulia.com/NJ/Edison/",
                  "https://www.trulia.com/NJ/Egg_Harbor_Township/",
                  "https://www.trulia.com/NJ/Forked_River/",
                  "https://www.trulia.com/NJ/Elizabeth/",
                  "https://www.trulia.com/NJ/Fort_Lee/",
                  "https://www.trulia.com/NJ/Freehold/",
                  "https://www.trulia.com/NJ/Galloway/",
                  "https://www.trulia.com/NJ/Hamilton/",
                  "https://www.trulia.com/NJ/Howell/",
                  "https://www.trulia.com/NJ/Jackson/",
                  "https://www.trulia.com/NJ/Irvington/",
                  "https://www.trulia.com/NJ/Jersey_City/",
                  "https://www.trulia.com/NJ/Lakewood/",
                  "https://www.trulia.com/NJ/Linden/",
                  "https://www.trulia.com/NJ/Little_Egg_Harbor_Township/",
                  "https://www.trulia.com/NJ/Marlton/",
                  "https://www.trulia.com/NJ/Mays_Landing/",
                  "https://www.trulia.com/NJ/Millville/",
                  "https://www.trulia.com/NJ/Mount_Laurel/",
                  "https://www.trulia.com/NJ/Newark/",
                  "https://www.trulia.com/NJ/Ocean_City/",
                  "https://www.trulia.com/NJ/Paterson/",
                  "https://www.trulia.com/NJ/Pennsauken/",
                  "https://www.trulia.com/NJ/Plainfield/",
                  "https://www.trulia.com/NJ/Pleasantville/",
                  "https://www.trulia.com/NJ/Sicklerville/",
                  "https://www.trulia.com/NJ/Somerset/",
                  "https://www.trulia.com/NJ/Teaneck/",
                  "https://www.trulia.com/NJ/Toms_River/",
                  "https://www.trulia.com/NJ/Trenton/",
                  "https://www.trulia.com/NJ/Union/",
                  "https://www.trulia.com/NJ/Vineland/",
                  "https://www.trulia.com/NJ/Wayne/",
                  "https://www.trulia.com/NJ/West_Orange/",
                  "https://www.trulia.com/NJ/Williamstown/",
                  "https://www.trulia.com/NJ/Willingboro/"]

    def parse(self, response):
        page = Selector(response)

        divs = page.xpath('//div[@class= "card backgroundBasic"]')

        for div in divs:
            item = TruliaWebCrawlerItem()

            # To get the property link
            href = div.xpath('.//a/@href').extract_first()
            item['href'] = href
            str = item['href'].split("-", 1)
            item['mortgage_id'] = str[0].split("/")[len(str[0].split("/")) - 1]
            #item['mortgage_id'] = re.match(r'/property/(.*)', str[0]).group(1)

            # this method sometimes does not work when the address is complicated, so I update it To get the city, state, zip code
            address_detail = str[1].split("-")
            item['neighborhood'] = div.xpath('.//div[@class="typeTruncate"]/text()').extract_first()
            item['mortgage_value'] = div.xpath(
                './/span[@class="cardPrice h4 man pan typeEmphasize noWrap typeTruncate "]/text()'). \
                extract_first()

            item['state'] = address_detail[len(address_detail) - 2]  # the second last is state
            item['zip_code'] = address_detail[len(address_detail) - 1]  # the last is zipcode
            item['city'] = item['neighborhood'].split(",")[len(item['neighborhood'].split(",")) - 2]
            item['address'] = div.xpath('.//a/@alt').extract_first()

            # # To get the numbers of bedrooms and bathrooms
            item['bedroom'] = div.xpath('.//li[@class="pln"]/text()').extract_first()
            item['bathroom'] = div.xpath('.//li[@class=""]/text()').extract_first()
            # item['sqft'] =  div.xpath('.//li[@class=""]/text()').extract()

            yield item

        page_ctrl = response.xpath('//div[@class="backgroundBasic"]')
        isNextPageThere = page_ctrl.xpath('.//a[@aria-label="Next"]').xpath('@href').extract_first()

        if isNextPageThere:
            next_page_url = "http:" + isNextPageThere.encode('utf-8')
            print "next page url: {0}".format(next_page_url)
            print next_page_url
            request = scrapy.Request(next_page_url, callback=self.parse, meta={  # render the next page
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 1}
                },
            })
            yield request
        else:
            print "this is the end!"




# class CollectCityHrefSpider(scrapy.Spider):
#     name = "trulia_city"
#
#     allowed_domains = ["trulia.com"]
#     start_urls = [
#         "https://www.trulia.com/sitemap/New-Jersey-real-estate/"
#     ]
#
#     def parse(self, response):
#         page = Selector(response)
#
#         divs = page.xpath('//div[@class= "line"]')
#         diva = divs.xpath('.//div')
#         for div in diva:
#             item = CityItem()
#
#             item['href'] = div.xpath('.//a/@href').extract_first()
#             item['city'] = div.xpath('.//a/text()').extract_first()
#
#             yield item
