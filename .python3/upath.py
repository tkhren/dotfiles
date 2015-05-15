# coding: utf-8

import hashlib

def countlines(path):
    """Count lines."""
    path = str(path)   # for pathlib
    count = -1
    for count, line in enumerate(open(path)): pass
    return count + 1

def hash(path, algorithm='md5', hex=True, blocksize=1024):
    """Calcurate hash of the file."""
    path = str(path)   # for pathlib

    if hasattr(hashlib, algorithm):
        hash_ = eval('hashlib.%s' % algorithm)()
    else:
        raise AttributeError("'module' object has no attribute '%s'" % algorithm)

    with open(path, mode='rb') as f:
        while True:
            chunk = f.read(blocksize)
            if chunk: hash_.update(chunk)
            else: break
    return hash_.hexdigest() if hex else hash_.digest()


# vim: ft=python ff=unix fenc=utf-8
