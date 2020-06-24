# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# for test convenience
#

# from .query_en import CamDictSpider

import logging
import re

import pymongo
from PyQt5.QtWidgets import QAction
from aqt import mw


# exprs_dict = {}

# settings = CamDictSpider.custom_settings
# logging.info(settings)


def do_test():
    """
    For testing convenience
    """
    logging.info('Hello World! This is testing.')
    # read_db()


# def list_exprs():
#     note_ids = [
#         # TODO select model
#         note_id for note_id in mw.col.find_notes('"note:Plain Text"')
#     ]
#     # logging.info(notes)
#     for note_id in note_ids:
#         # Replace '&nbsp;' with whitespace TODO select field
#         text = re.sub(r'&nbsp;', ' ', mw.col.getNote(note_id)['New Words'])
#         # IF not standard format
#         if not re.fullmatch(r'^(<div>)?[a-zA-Z,; ]*(</div>)?$', text):
#             logging.info('Format error in %s' % text)
#             # TODO suspend card
#             continue
#         # Remove div tag and leading/trailing whitespaces
#         text = re.sub(r'<[/]?div>', '', text).strip()
#         # Expressions
#         exprs = re.split(r'\s?[,;]\s?', text)
#         exprs_dict[note_id] = exprs
#     logging.info(exprs_dict)


# def read_db():
#     # Connect to MongoDB
#     client = pymongo.MongoClient(settings.get('MONGO_URI'))
#     db = client[settings.get('MONGO_DATABASE')]
#     coll = db[settings.get('MONGO_COLLECTION')]
#     logging.info(coll)


test_action = QAction("TEST DICT CRAWLING...", mw)
test_action.triggered.connect(do_test)
mw.form.menuTools.addAction(test_action)
