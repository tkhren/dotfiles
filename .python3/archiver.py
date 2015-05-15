# coding: utf-8

import os
import zipfile
import tarfile
import mimetypes

try:
    import rarfile  # 'rarfile' module is required
except ImportError as e:
    rarfile = None

_mime = mimetypes.MimeTypes()

class _ArcType:
    ZIP = _mime.guess_type('a.zip')
    JAR = _mime.guess_type('a.jar')
    XPI = _mime.guess_type('a.xpi')
    BZIP2 = _mime.guess_type('a.bz2')
    XZ  = _mime.guess_type('a.xz')
    TAR = _mime.guess_type('a.tar')
    TARGZ = _mime.guess_type('a.tar.gz')
    TARBZ2 = _mime.guess_type('a.tar.bz2')
    TARXZ = _mime.guess_type('a.tar.xz')
    RAR = _mime.guess_type('a.rar')
    Z = _mime.guess_type('a.Z')
    P7Z = _mime.guess_type('a.7z')
    CAB = _mime.guess_type('a.cab')
    LHA = _mime.guess_type('a.lha')


class InvalidArchiveError(Exception):
    pass


class Archive(object):
    """Utility class to pack and unpack various archive.
    Usage:
    >>> a = Archive('a.tar.gz')
    >>> a.add('/path/to/file')
    >>> a.unpack('abc')
    """
    ZIP = 'ZIP'
    ZIP_DEFLATED = 'ZIP_DEFLATE'
    ZIP_BZIP2 = 'ZIP_BZIP2'
    ZIP_LZMA2 = 'ZIP_LZMA2'
    TAR = 'TAR'
    TAR_GZIP = 'TAR_GZIP'
    TAR_BZIP2 = 'TAR_BZIP2'
    TAR_LZMA2 = 'TAR_LZMA2'
    RAR = 'RAR'

    def __init__(self, path, astype=None):
        self.path = path

        if astype is None:
            mime = _mime.guess_type(path)
            if mime == _ArcType.ZIP: astype = self.ZIP_DEFLATED
            elif mime == _ArcType.JAR: astype = self.ZIP_DEFLATED
            elif mime == _ArcType.XPI: astype = self.ZIP_DEFLATED
            elif mime == _ArcType.BZIP2: astype = self.ZIP_BZIP2
            elif mime == _ArcType.XZ: astype = self.ZIP_LZMA2
            elif mime == _ArcType.TAR: astype = self.TAR
            elif mime == _ArcType.TARGZ: astype = self.TAR_GZIP
            elif mime == _ArcType.TARBZ2: astype = self.TAR_BZIP2
            elif mime == _ArcType.TARXZ: astype = self.TAR_LZMA2
            elif mime == _ArcType.RAR: astype = self.RAR
            else:
                raise InvalidArchiveError()

        if astype == self.ZIP:
            kwds = {'compression': zipfile.ZIP_STORED}
            self._arcopen = (lambda m: zipfile.ZipFile(self.path, m, **kwds))

        elif astype == self.ZIP_DEFLATED:
            kwds = {'compression': zipfile.ZIP_DEFLATED}
            self._arcopen = (lambda m: zipfile.ZipFile(self.path, m, **kwds))

        elif astype == self.ZIP_BZIP2:
            kwds = {'compression': zipfile.ZIP_BZIP2}
            self._arcopen = (lambda m: zipfile.ZipFile(self.path, m, **kwds))

        elif astype == self.ZIP_LZMA2:
            kwds = {'compression': zipfile.ZIP_LZMA}
            self._arcopen = (lambda m: zipfile.ZipFile(self.path, m, **kwds))

        elif astype == self.TAR:
            kwds = {}
            self._arcopen = (lambda m: tarfile.open(self.path, m, **kwds))

        elif astype == self.TAR_GZIP:
            kwds = {}
            self._arcopen = (lambda m: tarfile.open(self.path, ('w:gz'if m=='w'else m), **kwds))

        elif astype == self.TAR_BZIP2:
            kwds = {}
            self._arcopen = (lambda m: tarfile.open(self.path, ('w:bz2'if m=='w'else m), **kwds))

        elif astype == self.TAR_LZMA2:
            kwds = {}
            self._arcopen = (lambda m: tarfile.open(self.path, ('w:xz'if m=='w'else m), **kwds))

        self.arctype = astype

    def __repr__(self):
        return 'Archive("%s",%s)' % (self.path, self.arctype)

    def namelist(self):
        with self._arcopen('r') as arcfile:
            try:
                return arcfile.namelist()
            except AttributeError as e:
                return arcfile.getnames()

    def infolist(self):
        with self._arcopen('r') as arcfile:
            try:
                return arcfile.infolist()
            except AttributeError as e:
                return arcfile.getmembers()

    def getinfo(self, name):
        with self._arcopen('r') as arcfile:
            try:
                return arcfile.getinfo(name)
            except AttributeError as e:
                return arcfile.getmember(name)

    def size(self):
        return os.path.getsize(self.path)

    def __adddirectory(self, arcfile, path):
        for root,dirs,files in os.walk(path):
            for d in dirs:
                self._adddirectory(arcfile, os.path.join(root, d))
            for f in files:
                arcfile.write(os.path.join(root, f))

    def __addfile(self, arcfile, path):
        try:
            arcfile.write(path)
            if os.path.isdir(path):
                self.__adddirectory(arcfile, path)
        except AttributeError as e:
            arcfile.add(path, recursive=True)

    def add(self, paths):
        """
            paths := '/path1'
                  := ['/path1', '/path2', '/path3']
                  := ('/path1', '/path2', '/path3')
        """
        if isinstance(paths, (list, tuple)):
            if len(paths) == 0:
                return
            with self._arcopen('a') as arcfile:
                for path in paths:
                    self.__addfile(arcfile, path)
        else:
            with self._arcopen('a') as arcfile:
                self.__addfile(arcfile, paths)

    def unpack(self, path='.', pwd=None):
        with self._arcopen('r') as arcfile:
            if self.arctype.startswith('ZIP'):
                arcfile.extractall(path, pwd=pwd)
            else:
                arcfile.extractall(path)

if __name__=="__main__":
    a = Archive('/home/tkhr/Downloads/a.zip')
    print(a.namelist())
