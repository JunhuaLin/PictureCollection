# encoding = utf-8
import re

from start.contract_model import UrlManagerBase


class UrlManager(UrlManagerBase):
    def __init__(self, capacity=100):
        self.url_set = set()
        self.url_pattern = re.compile(r'^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')
        self.capacity = capacity

    def add(self, url):
        if isinstance(url, str) and self.url_pattern.match(url):
            return
        self.url_set.add(url)

    def get(self):
        return self.url_set

    def is_empty(self):
        return len(self.url_set) == 0

    def is_full(self):
        return len(self.url_set) >= 100
