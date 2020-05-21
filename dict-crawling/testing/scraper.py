import scrapy


class MoeDictSpider(scrapy.Spider):
    name = "moedict_spider"
    start_urls = ['https://www.moedict.tw/%E8%90%8C']
