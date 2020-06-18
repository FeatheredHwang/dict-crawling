import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader


class MoeDictSpider(scrapy.Spider):
    name = "moe_dict_spider"
    start_urls = ['https://www.moedict.tw/%E8%90%8C']

    def parse(self, response):
        pass


process = CrawlerProcess()
process.crawl(MoeDictSpider)
process.start()
