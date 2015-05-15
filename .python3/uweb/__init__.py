# coding: utf-8
# This module depends on the following library.
#   * requests
#   * lxml
#   * pyquery
#

import requests
import pyquery

import functools

def _memoize(obj):
    """
        Memoize decorator:
        Caches a function's return value each time it is called.
        If called later with the same arguments, the cached value is returned
        (not reevaluated).
    """
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer


class WebPage(requests.Response):
    u"""
        requests.Response と pyquery.PyQuery をくっつけただけのクラス
    """
    @classmethod
    def get(cls, url, **kwds):
        self = cls()
        self.response = requests.get(url, **kwds)
        self.__dict__.update(self.response.__dict__)
        return self

    @property
    @_memoize
    def root(self):
        return pyquery.PyQuery(self.text)

    def find(self, *args, **kwds):
        return self.root.find(*args, **kwds)

    def links(self):
        return self.find('a')

    def link_urls(self):
        urls = []
        for link in self.links():
            url = link.attrib.get('href', None)
            if url:
                urls.append(url)
        return urls

    def images(self):
        return self.find('img')

    def image_urls(self):
        urls = []
        for img in self.images():
            url = img.attrib.get('src', None)
            if url:
                urls.append(url)
        return urls

    @property
    @_memoize
    def title(self):
        titles = self.find('title')
        if titles:
            return titles[0].text
        return ''



class WebSpider(object):
    name = 'WebSpider'
    allowed_domains = []
    start_urls = []
    sitemap_urls = []

    def parse(self, response):
        pass





spider = WebSpider('Google Images Spider')
spider.schedule()
spider.download()

spider.download_images(['jpg', 'png', 'gif'])
spider.start()
spider.dump()
spider.kill()
