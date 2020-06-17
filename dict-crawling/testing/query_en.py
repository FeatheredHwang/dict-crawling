import re

import pymongo

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader


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


class CamDictSpider(scrapy.Spider):
    name = 'cambridge_dict_spider'
    allowed_domains = ['dictionary.cambridge.org']
    # start_urls = ['https://dictionary.cambridge.org/dictionary/english/recoil']

    custom_settings = {
        # To get the user-agent required for cambridge.org,
        # visit `https://www.cambridge.org/gb/cambridgeenglish/support`
        # TODO (Archive) What if the required User-Agent changed? How to correct it automatically?
        "USER_AGENT": 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'ITEM_PIPELINES': {
            'scrapy.pipelines.files.FilesPipeline': 1,
            # 'MongoPipeline': 100,
        },
        # 'FILES_STORE': str(PurePath(__file__).parent.joinpath('CamDictPipeline')),

    }

    def __init__(self, expr=None, *args, **kwargs):
        super(CamDictSpider, self).__init__(*args, **kwargs)
        expr = ['recoil', 'blow OFF', ' spELL']
        self.start_urls = ['https://dictionary.cambridge.org/dictionary/english/%s' % q for q in expr]

    # def start_requests(self):
    #     yield scrapy.Request('https://dictionary.cambridge.org/dictionary/english/%s' % self.word)

    def parse(self, response):
        # get uk pronunciation url
        # src = response.css('.uk .daud source[type="audio/mpeg"]::attr(src)').get()
        # url = response.urljoin(src)
        # return EnWordItem(file_urls=[url])
        # return response.css('.uk .daud').get()

        # print(response.request.url)

        il = ItemLoader(item=EnExprItem(), response=response)
        m = re.match(r'(?P<base>.*[/])(?P<expr>[a-z-]+)([?]q=(?P<query>[a-zA-Z0-9%]*))?', response.request.url)
        q = m.group('query')
        if not q:
            q = m.group('expr')
        else:
            # Replace '%2B' with whitespace in expression
            q = re.sub(r'%2B', ' ', q)
        il.add_value('q', q)
        il.add_value('url', m.group('base') + m.group('expr'))
        il.add_css('expr', '.dhw')
        il.add_css('cat', '.dpos')
        il.add_css('pron', '.uk')
        il.add_css('define', '#cald4-1-1+ .dsense_b .ddef_d')
        # print(il.load_item())
        return il.load_item()

    # @staticmethod
    # def inquiry(word):
    #     yield scrapy.Request('https://dictionary.cambridge.org/dictionary/english/%s' % word)


process = CrawlerProcess()
process.crawl(CamDictSpider)
process.start()
