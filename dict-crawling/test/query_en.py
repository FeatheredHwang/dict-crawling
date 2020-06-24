# import re
import hashlib
import logging
import os
from typing import List

import pymongo

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.pipelines.images import FilesPipeline
from scrapy.utils.python import to_bytes
from w3lib.html import remove_tags


print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))


# Create an instance of class TakeFirst
take_first = TakeFirst()


class MongoPipeline:

    def __init__(self, mongo_uri, mongo_db, mongo_coll):
        self.mongo_uri = mongo_uri
        self.client = None
        self.mongo_db = mongo_db
        self.db = None
        self.mongo_coll = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):
        # pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_coll=crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        # initializing spider
        # opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # deleting all documents in the collection
        self.db[self.mongo_coll].delete_many({})

    def close_spider(self, spider):
        # clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        # how to handle each post
        self.db[self.mongo_coll].insert(dict(item))
        return item


class UKPronPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        # original_path = super(UKPronPipeline, self).file_path(request, response=None, info=None)
        # Get sha1 of file
        # media_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        # Get extension of file
        media_ext = os.path.splitext(request.url)[1]
        # Download ogg files only
        if media_ext != '.ogg':
            logging.info('Ogg file of "%s" not found.')
        # delete 'full/' from the path
        # return 'full/%s%s' % (media_guid, media_ext)
        return 'downloads/%s' % (os.path.basename(request.url))


class EnExprItem(scrapy.Item):
    # query string as _id
    _id = scrapy.Field(
        # pymongo.errors.WriteError: can't use an array for _id
        output_processor=take_first
    )
    # expression as _id
    expr = scrapy.Field()
    # url of query result
    url = scrapy.Field()
    # category
    cat = scrapy.Field()
    # definition
    define = scrapy.Field()
    # pronunciation
    pron = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


class EnExprLoader(ItemLoader):
    """
    Nothing changed yet.
    """


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
            # 'scrapy.pipelines.files.FilesPipeline': 300
            'dict-crawling.testing.query_en.UKPronPipeline': 10,
            'dict-crawling.testing.query_en.MongoPipeline': 100,
        },
        'FILES_STORE': os.path.dirname(__file__),
        'MONGO_URI': 'mongodb://localhost:27017',
        'MONGO_DATABASE': 'new-expressions',
        'MONGO_COLLECTION': 'scrapy_cambridge_dict'
    }

    def __init__(self, exprs: List[str] = [], *args, **kwargs):
        """
        :param exprs: string or a list of string
        :param args:
        :param kwargs:
        """
        super(CamDictSpider, self).__init__(*args, **kwargs)
        # TODO this line is used for test, delete it later
        exprs = ['recoil', 'blow OFF', ' spELL', 'spell', 'selected', 'selecting']
        for expr in exprs:
            self.exprs.append(expr.lower().split())

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

        print(response.url)

        # IF redirect needed, follow the redirect link.
        # For example, 'selected' is the past simple and past participle of 'select',
        # so it will be redirected to 'select'
        ref = response.css('a.Ref::attr(href)').get()
        if ref:
            return response.follow(
                ref,
                callback=self.parse,
                meta={'q': response.meta.get('q')}
            )

        il = EnExprLoader(item=EnExprItem(), response=response)
        # il.default_input_processor = take_first

        # m = re.match(r'(?P<base>.*[/])(?P<expr>[a-z-]+)([?]q=(?P<query>[a-zA-Z0-9%]*))?', response.request.url)
        # q = m.group('query')
        # if not q:
        #     q = m.group('expr')
        # else:
        #     # Replace '%2B' with whitespace in expression
        #     q = re.sub(r'%2B', ' ', q)
        # il.add_value('q', q)
        # il.add_value('url', m.group('base') + m.group('expr'))

        il.add_value('_id', response.meta.get('q'))
        il.add_value('url', response.url)
        il.add_css('expr', 'span.dhw::text', take_first)
        il.add_css('cat', '.dpos::text', take_first)
        # As Anki2.1 doesn't support HTML5 audio, I have to download the audio file.
        # get uk pronunciation url
        src = response.css('.uk .daud source[type="audio/ogg"]::attr(src)').get()
        url = response.urljoin(src)
        il.add_value('pron', os.path.basename(url))
        il.add_value('file_urls', url)
        il.add_css('define', '.def', take_first, remove_tags)
        return il.load_item()


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(CamDictSpider)
    process.start()
