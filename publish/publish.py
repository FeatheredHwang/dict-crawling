# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# For release convenience
#


import os
import sys
from zipfile import ZipFile

if __name__ == '__main__':
    # project path
    pj_path = os.path.dirname(sys.path[0])
    print('Project path:    ', pj_path)
    # project name
    pj_name = os.path.basename(pj_path)
    print('Project name:    ', pj_name)
    # publish path
    pub_path = os.path.join(sys.path[0], pj_name + '.ankiaddon')
    print('Publish path:    ', pub_path)
    # code path, make sure that core code directory name is as the same as the project folder name
    code_path = os.path.join(pj_path, pj_name)
    print('Code path:       ', code_path)
    if not os.path.exists(code_path):
        print('Directory %s not found' % code_path)
    else:
        # ready to write zip file
        with ZipFile(pub_path, 'w') as zf:
            for foldername, subfolders, filenames in os.walk(code_path):
                for filename in filenames:
                    if True:
                        # TODO Add ignore rule
                        filepath = os.path.join(foldername, filename)
                        zf.write(filepath, os.path.relpath(filepath, code_path))
        print('Publishing succeed.')
