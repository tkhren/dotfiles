# coding: utf-8

"""
    Library for a python interpreter.
    This script works on Python 2.7

    Write a following sentence in your ~/.pythonrc.
        from prelude import *
"""

import prelude

def exec_(code=''):
    try:
        exec(code, globals())
        print('>>> %s' % code)
    except Exception as e:
        print('*** %s: %s\n' % (code, e))


print('These commands were executed:')
exec_('import sys, os')
exec_('import random')
exec_('import fnmatch')
exec_('import re; rc = re.compile')
exec_()
exec_('from pprint import pprint as pp')
exec_('from subprocess import getoutput as sh')
exec_()
