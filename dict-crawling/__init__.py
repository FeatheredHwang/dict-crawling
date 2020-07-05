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
import traceback

# add-on's directory
cur_dir = os.path.dirname(__file__)
# logging set up
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=os.path.join(cur_dir, 'general.log'),)
# print the module's information
logging.info('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))

# add current directory to sys path so that we can import modules in it
sys.path.insert(1, cur_dir)

# import test module if exist
try:
    from .test import test
except ImportError as e:
    logging.error("""Something went error when importing test.py: \n{msg}\n{trc}"""
                  .format(msg=str(e), trc=traceback.format_exc()))
