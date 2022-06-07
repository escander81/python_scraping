from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from lerua.spiders.lermer import LermerSpider
from lerua import settings

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    query = input("Что нужно в леруа?\n")
    process.crawl(LermerSpider, query=query)
    # query = 'лыжи'
    # process.crawl(LermerSpider, query=query)

    process.start()