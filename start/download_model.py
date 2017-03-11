# encoding = utf-8
import os
import urlparse

import requests


class Download(object):
    root_dir = "D:\\images"
    this_download = None
    chunk_size = 1024

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

    def download(self, url_str):

        if url_str is None:
            return
        r = requests.get(url_str)
        url_str_parse = urlparse.urlparse(url_str)
        file_name = url_str_parse.path.split('/')[-1]
        file_path = "\\".join([self.root_dir, file_name])

        with open(file_path, 'wb') as fd:
            for chunk in r.iter_content(self.chunk_size):
                fd.write(chunk)
