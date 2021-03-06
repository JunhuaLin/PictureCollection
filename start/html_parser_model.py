# encoding = utf-8
import re
import urlparse

import requests
from bs4 import BeautifulSoup


class HtmlParser(object):
    def __init__(self, max_page):
        self._max_page = max_page
        self.url_set = set()
        self.img_url_set = set()
        self.url_pattern = re.compile(r'^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')
        self.img_pattern = re.compile(r'.+((.jpg)|(.png)|(.jpng))$')
        self.img_url_pattern = re.compile(r'^(//).+')
        self.count = 0
        self.img_count = 0
        self.request_timeout = 2
        self.is_use_proxies = False
        self.proxies = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}

    def parse(self, url):
        if not self.match_url(url):
            return
        proxies = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}
        headers = {
            'user-agent': r'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}

        r = None
        try:
            if self.is_use_proxies:
                r = requests.get(url, headers=headers, proxies=proxies, timeout=self.request_timeout)
            else:
                r = requests.get(url, headers=headers, timeout=self.request_timeout)
        except:
            return

        soup = BeautifulSoup(r.text, 'html.parser')

        self.parse_image_url(url, soup)
        self.parse_a_url(url, soup)

    def parse_a_url(self, url, soup):
        a_url_set = self.url_set
        if len(self.url_set) >= self._max_page:
            return

        temp_a_url_set = set()
        for a in soup.find_all('a'):
            if len(self.url_set) >= self._max_page:
                break

            url_join = urlparse.urljoin(url, a.get("href"))
            if not self.match_url(url_join):
                continue
            if url_join in a_url_set:
                continue
            a_url_set.add(url_join)
            temp_a_url_set.add(url_join)

            self.count += 1
            print "url -", self.count, " ---> ", url_join

        for url in temp_a_url_set:
            self.parse(url)

    def parse_image_url(self, url, soup):
        if len(self.img_url_set) >= self._max_page:
            return False

        for img in soup.find_all('img'):
            if not self.add_image_url(url, img, ('data-src', 'src')):
                return

        for img in soup.find_all('input'):
            if not self.add_image_url(url, img, ('data-src', 'src')):
                return

    def add_image_url(self, url, img, property):
        for p in property:
            try:
                url_path = img.get(p)
                url_join = ""
                if self.img_url_pattern.match(url_path):
                    url_join = "".join(["http:", url_path])
                else:
                    url_join = urlparse.urljoin(url, url_path)

                if url_join and self.img_pattern.match(url_join.split("\\")[-1]):
                    if len(self.img_url_set) >= self._max_page:
                        return False
                    self.img_url_set.add(url_join)
                    self.img_count += 1
                    print "img url -", self.img_count, " ---> ", url_join
            except:
                continue

        return True

    def match_url(self, str_url):
        return self.url_pattern.search(str_url)

    def get_img_set(self):
        return self.img_url_set

    def set_proxies(self, proxies):
        if isinstance(proxies, dict):
            self.proxies = proxies

    def use_proxy(self, use=False):
        if use:
            self.is_use_proxies = True
        else:
            self.is_use_proxies = False

    def timeout(self, time=2):
        self.request_timeout = time

# if __name__ == "__main__":
#     url = "http://www.tooopen.com/img/88_876.aspx"
#     # url = "https://www.t66y.com/thread0806.php?fid=16"
#     html_parser = HtmlParser(100)
#     html_parser.start(url)
#     print len(html_parser.get_img_set())
