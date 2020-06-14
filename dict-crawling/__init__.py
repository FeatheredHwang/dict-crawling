# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


"""
Anki add-on developing template.

Much thanks to ...

See github page to report issues or to contribute:
https://github.com/feathered-hwang/anki-myaddon
"""


# set up logging to file - see previous section for more details
import logging
import os
import sys


# current module's directory
cur_dir = os.path.dirname(__file__)
# logging set up
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=os.path.join(cur_dir, 'logger.log'),
                    filemode='w')
# print the module's directory
logging.info(cur_dir)


# import test module if exist
try:
    from .testing import test
except ImportError:
    logging.info("test module doesn't exist.")
