# encoding = utf-8
import os
import urlparse

import requests


class Download(object):
    root_dir = "D:\\images"
    this_download = None
    chunk_size = 1024
    proxies = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}
    is_use_proxies = False
    timeout = 10

    def __init__(self):
        if not os.path.exists(Download.root_dir):
            os.mkdir(Download.root_dir)

    @staticmethod
    def init(root=""):
        if root:
            Download.root_dir = root

        if not Download.this_download:
            Download.this_download = Download()

    @staticmethod
    def get_instance():
        if not Download.this_download:
            raise Exception("you most call init method!")
        return Download.this_download

    def download(self, url):

        if url is None:
            return

        proxies = self.proxies
        if not self.is_use_proxies:
            proxies = None

        if isinstance(url, str):
            r = requests.get(url, proxies=proxies, timeout=self.timeout)
            self._download_single(r, url)
            return

        if isinstance(url, set) or isinstance(url, list):
            for u in url:
                r = requests.get(u, proxies=proxies, timeout=self.timeout)
                self._download_single(r, u)

    def _download_single(self, r, url):
        url_str_parse = urlparse.urlparse(url)
        file_name = url_str_parse.path.split('/')[-1]
        file_path = "\\".join([self.root_dir, file_name])
        with open(file_path, 'wb') as fd:
            for chunk in r.iter_content(self.chunk_size):
                fd.write(chunk)
        print url

    def set_proxies(self, proxies):
        if isinstance(proxies, dict):
            self.proxies = proxies

    def use_proxy(self, use=False):
        if use:
            self.is_use_proxies = True
        else:
            self.is_use_proxies = False
