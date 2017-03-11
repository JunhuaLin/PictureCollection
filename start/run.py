# encoding: utf-8

import requests

from start.download_model import Download
from start.html_parser_model import HtmlParser


def get_photo_url(pn=1, rn=60):
    urls = []
    url = r"http://image.baidu.com/data/imgs"

    def params():
        payload = {
            'col': '美女',
            'tag': '小清新',
            'sort': 0,
            'pn': pn,
            'rn': rn,
            'p': 'channel',
            'from': 1,
        }
        return payload

    r = requests.get(url, params())
    for image in r.json()['imgs']:
        try:
            urls.append(image["downloadUrl"])
        except:
            print "解析出错"

    return urls


if __name__ == "__main__":
    Download.init()
    download = Download.get_instance()

    url = "http://www.tooopen.com/img/87.aspx"

    html_parser = HtmlParser(100)
    html_parser.start(url)

    url_list = html_parser.get_img_set()
    print len(url_list)
    print "开始下载图片"

    download.use_proxy(True)
    download.download(url_list)
    print "下载图片结束"
