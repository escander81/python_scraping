import scrapy
from scrapy.http import HtmlResponse
from lerua.items import LeruaItem
from scrapy.loader import ItemLoader


class LermerSpider(scrapy.Spider):
    name = 'lermer'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']


    def parse(self, response: HtmlResponse):
        print()
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaItem(), response=response)
        print()
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("price", "//span[@slot='price']//text()")
        loader.add_xpath('photos', "//source[contains(@srcset, 'w_1200')]/@srcset")
        loader.add_value("url", response.url)
        yield loader.load_item()