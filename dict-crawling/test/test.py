# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# for test convenience
#

from .query_en import CamDictSpider

import logging
import pymongo
import re

from PyQt5.QtWidgets import QAction
from aqt import mw
from scrapy.crawler import CrawlerProcess


logging.info('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))

exprs_dict = {}
settings = CamDictSpider.custom_settings


def do_test():
    """
    For testing convenience
    """
    logging.info('Hello World! This is testing.')
    list_exprs()
    query_db()


def list_exprs():
    note_ids = [
        # TODO select model
        note_id for note_id in mw.col.find_notes('"note:Plain Text"')
    ]
    # logging.info(notes)
    for note_id in note_ids:
        # Replace '&nbsp;' with whitespace TODO select field
        text = re.sub(r'&nbsp;', ' ', mw.col.getNote(note_id)['New Words'])
        # IF not standard format
        if not re.fullmatch(r'^(<div>)?[a-zA-Z,; ]*(</div>)?$', text):
            logging.info('Format error in %s' % text)
            # TODO suspend card
            continue
        # Remove div tag and leading/trailing whitespaces
        text = re.sub(r'<[/]?div>', '', text).strip()
        # Split to get expressions and add (note_id, expressions) into dict
        exprs = re.split(r'\s?[,;]\s?', text)
        exprs_dict[note_id] = exprs

    logging.info('Expression dictionary:\n{}'.format(exprs_dict))
    # concatenate each note's expressions
    all_exprs = sum(exprs_dict.values(), [])
    logging.info('All the expressions:\n{}'.format(all_exprs))
    # scrapy these expressions
    process = CrawlerProcess()
    process.crawl(CamDictSpider, exprs=all_exprs)
    process.start()
    # test logging
    logging.info('Dict-crawling finished.')


def query_db():
    # create connection
    client = pymongo.MongoClient(settings.get('MONGO_URI'))
    db = client[settings.get('MONGO_DATABASE')]
    coll = db[settings.get('MONGO_COLLECTION')]

    # do query
    # for (note_id, exprs) in exprs_dict:
    #     note = mw.col.getNote(note_id)
    #     for expr in exprs:

    # close connection
    client.close()
    logging.info('MongoDB query finished.')


test_action = QAction("TEST DICT CRAWLING...", mw)
test_action.triggered.connect(do_test)
mw.form.menuTools.addAction(test_action)
