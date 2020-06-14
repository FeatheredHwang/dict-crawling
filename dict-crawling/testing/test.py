# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# for testing convenience
#


import logging
import re

from PyQt5.QtWidgets import QAction
from aqt import mw

field = 'New Words'


def do_test():
    """
    For testing convenience
    """
    logging.info('Hello World')
    # model = mw.col.models.byName('Plain Text')
    # note_ids = mw.col.find_notes("note:Basic")
    # logging.info(note_ids)
    notes = [
        mw.col.getNote(note_id)
        for note_id in mw.col.find_notes('"note:Plain Text"')
    ]
    # logging.info(notes)
    for note in notes:
        # Replace '&nbsp;' with whitespace
        text = re.sub(r'&nbsp;', ' ', note['New Words'])
        # IF not standard format
        if not re.fullmatch(r'^(<div>)?[a-zA-Z,; ]*(</div>)?$', text):
            logging.info('Format error in %s' % text)
            # TODO suspend card
            continue
        # Remove div tag and leading/trailing whitespaces
        text = re.sub(r'<[/]?div>', '', text).strip()
        words = re.split(r'\s?[,;]\s?', text)
        logging.info(words)


test_action = QAction("TEST DICT CRAWLING...", mw)
test_action.triggered.connect(do_test)
mw.form.menuTools.addAction(test_action)
