# encoding: utf-8
class DownloadBase(object):
    def download(self):
        pass


class UrlManagerBase(object):
    def put(self, url):
        pass

    def get(self):
        pass

    def is_empty(self):
        pass


class HTMLParserBase(object):
    def parser(self, html):
        pass
