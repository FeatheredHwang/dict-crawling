# import re

import pymongo

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader

from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


class MongoPipeline:
    collection_name = 'en_scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        # initializing spider
        # opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        # how to handle each post
        self.db[self.collection_name].insert(dict(item))
        return item


class EnExprItem(scrapy.Item):
    # query
    q = scrapy.Field()
    # url
    url = scrapy.Field()
    # expression
    expr = scrapy.Field()
    # category
    cat = scrapy.Field()
    # pronunciation
    pron = scrapy.Field()
    # definition
    define = scrapy.Field()
    # file_urls = scrapy.Field()
    # files = scrapy.Field()


class EnExprLoader(ItemLoader):
    default_input_processor = TakeFirst()


class CamDictSpider(scrapy.Spider):
    name = 'cambridge_dict_spider'
    allowed_domains = ['dictionary.cambridge.org']
    # expressions
    exprs = []

    custom_settings = {
        # To get the user-agent required for cambridge.org,
        # visit `https://www.cambridge.org/gb/cambridgeenglish/support`
        # TODO (Archive) What if the required User-Agent changed? How to correct it automatically?
        "USER_AGENT": 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'ITEM_PIPELINES': {
            'scrapy.pipelines.files.FilesPipeline': 1,
            'dict-crawling.testing.query_en.MongoPipeline': 100,
        },
        # 'FILES_STORE': str(PurePath(__file__).parent.joinpath('CamDictPipeline')),
        'MONGO_URI': 'mongodb://localhost:27017',
        'MONGO_DATABASE': 'sivji-sandbox',
    }

    def __init__(self, exprs=None, *args, **kwargs):
        super(CamDictSpider, self).__init__(*args, **kwargs)
        if exprs is None:
            exprs = []
        self.exprs = exprs
        # TODO this line is used for test, delete it later
        self.exprs = ['recoil', 'blow OFF', ' spELL', 'selected']
        print(self.exprs)

    def start_requests(self):
        for q in self.exprs:
            print(q)
            yield scrapy.Request(
                'https://dictionary.cambridge.org/dictionary/english/%s' % q,
                callback=self.parse,
                meta={'q': q}
            )

    def parse(self, response):
        # get uk pronunciation url
        # src = response.css('.uk .daud source[type="audio/mpeg"]::attr(src)').get()
        # url = response.urljoin(src)
        # return EnWordItem(file_urls=[url])
        # return response.css('.uk .daud').get()
        print(response.url)



        il = EnExprLoader(item=EnExprItem(), response=response)
        # m = re.match(r'(?P<base>.*[/])(?P<expr>[a-z-]+)([?]q=(?P<query>[a-zA-Z0-9%]*))?', response.request.url)
        # q = m.group('query')
        # if not q:
        #     q = m.group('expr')
        # else:
        #     # Replace '%2B' with whitespace in expression
        #     q = re.sub(r'%2B', ' ', q)
        # il.add_value('q', q)
        # il.add_value('url', m.group('base') + m.group('expr'))
        il.add_value('q', response.meta.get('q'))
        il.add_value('url', response.url)
        il.add_css('expr', 'span.dhw::text')
        il.add_css('cat', '.dpos')
        il.add_css('pron', '.uk')
        il.add_css('define', '#cald4-1-1+ .dsense_b .ddef_d')
        print(il.load_item())
        return il.load_item()


process = CrawlerProcess()
process.crawl(CamDictSpider)
process.start()
