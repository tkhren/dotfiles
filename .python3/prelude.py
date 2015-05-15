# coding: utf-8

"""
    Library for a python interpreter.
    This script works on Python 3.x

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

def __path_filter(names, pattern):
    if pattern == '*':
        return names
    elif isinstance(pattern, type(re.compile(r''))):
        return [p for p in names if pattern.search(p)]
    else:
        return fnmatch.filter(names, pattern)

def __path_listdir(pathObj, pattern='*'):
    """Return a list of entry names under the current directory."""
    names = __path_filter(os.listdir(str(pathObj)), pattern)
    return [pathObj.joinpath(name) for name in names]

def __path_files(pathObj, pattern='*'):
    """Return a list of file names under the current directory."""
    return [p for p in pathObj.listdir(pattern) if p.is_file()]

def __path_dirs(pathObj, pattern='*'):
    """Return a list of directory names under the current directory."""
    return [p for p in pathObj.listdir(pattern) if p.is_dir()]

def __path_links(pathObj, pattern='*'):
    """Return a list of link file names under the current directory."""
    return [p for p in pathObj.listdir(pattern) if p.is_symlink()]

def __path_walk(pathObj, pattern='*'):
    """Generate the entry names in a directory tree by walking the tree
    reursively. """
    for root, dirs, files in os.walk(pathObj):
        dirs = __path_filter(dirs, pattern)
        for f in dirs:
            yield pathObj.joinpath(root, f)
        files = __path_filter(files, pattern)
        for f in files:
            yield pathObj.joinpath(root, f)

def __path_walkfiles(pathObj, pattern='*'):
    """Generate the file names in a directory tree by walking the tree
    reursively. """
    for root, dirs, files in os.walk(pathObj):
        files = __path_filter(files, pattern)
        for f in files:
            yield pathObj.joinpath(root, f)

def __path_walkdirs(pathObj, pattern='*'):
    """Generate the directory names in a directory tree by walking the tree
    reursively. """
    for root, dirs, files in os.walk(pathObj):
        dirs = __path_filter(dirs, pattern)
        for f in dirs:
            yield pathObj.joinpath(root, f)


print('These commands were executed:')
exec_('import sys, os')
exec_('import random')
exec_('import fnmatch')
exec_('import re; rc = re.compile')
exec_()
exec_('from pprint import pprint as pp')
exec_('from subprocess import getoutput as sh')
exec_()
exec_('import pathlib')
exec_('from pathlib import Path')
exec_('Path.listdir = __path_listdir')
exec_('Path.files = __path_files')
exec_('Path.dirs  = __path_dirs')
exec_('Path.links = __path_links')
exec_('Path.walk  = __path_walk')
exec_('Path.walkfiles = __path_walkfiles')
exec_('Path.walkdirs  = __path_walkdirs')
exec_('cwd = Path.cwd()')
exec_()
exec_('import ustr')
exec_('import useq')
#exec_('import uweb')
exec_('import umath')
exec_('from umath.base10 import Base10')
exec_()
