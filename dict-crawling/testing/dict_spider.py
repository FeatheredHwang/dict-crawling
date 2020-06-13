from pathlib import Path, PurePath

import scrapy
from scrapy.crawler import CrawlerProcess


class MoeDictSpider(scrapy.Spider):
    name = "moe_dict_spider"
    start_urls = ['https://www.moedict.tw/%E8%90%8C']

    def parse(self, response):
        pass


class AudioItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()


class CamDictSpider(scrapy.Spider):

    name = 'cambridge_dict_spider'
    allowed_domains = ['dictionary.cambridge.org']
    start_urls = ['https://dictionary.cambridge.org/dictionary/english/recoil']

    custom_settings = {
        # To get the user-agent required for cambridge.org,
        # visit `https://www.cambridge.org/gb/cambridgeenglish/support`
        # TODO (Archive) What if the required User-Agent changed? How to correct it automatically?
        "USER_AGENT": 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'ITEM_PIPELINES': {'scrapy.pipelines.files.FilesPipeline': 1},
        'FILES_STORE': str(PurePath(__file__).parent.joinpath('CamDictPipeline')),

    }

    def parse(self, response):
        # get uk pronunciation url
        src = response.css('.uk .daud source[type="audio/mpeg"]::attr(src)').get()
        url = response.urljoin(src)
        return AudioItem(file_urls=[url])


process = CrawlerProcess()
process.crawl(CamDictSpider)
process.start()
