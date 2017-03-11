# encoding: utf-8

import requests

from start.download_model import Download


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
    n = 1
    for index in range(n, n + 6):
        for url in get_photo_url(index * 60):
            download.download(url)
            print url
