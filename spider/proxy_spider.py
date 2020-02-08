# -*- coding: UTF-8 -*-

import requests
from lxml import etree
import base64
import json
from hyper.contrib import HTTP20Adapter


def main():

    url = 'https://ip.ihuan.me/address/5LiK5rW3.html'
    headers = {
        ':authority': 'ip.ihuan.me',
        ':method': 'GET',
        ':path': '/address/5LiK5rW3.html',
        ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,ko;q=0.6,zh-TW;q=0.5',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://ip.ihuan.me/address/5LiK5rW3.html?__cf_chl_captcha_tk__=182b0c2f558181921446017f896b3208356a2780-1581143065-0-AW_vdssUuo6RBxJkUbsVp_QffhpnYJi8sZiqEu-bE90gd_pKkiEqv_evZLghtVEEJ6AIDuUgUwprgjGnKfVb9Q38XlaoVFrNriZUAjHtYURgLlwBZQuYfUks05oRwVcOVaIPRlbI0R3FaTjMOzADk6udpdupf0lRIPjNcTDYcj3dDk961g04dOQjkR2Pg7jQd2672Nw1ZrUxIkjlza0pcBdYMtRfHBdJxsG8OR4PNgGG9ESL4xKo9aW4N8eijT5FZrWwL6iKbasn-BkFXbzw6JXVZ5Um0upHGqIKCHXXQLLoldOZiW2mrv9prtLR-eHHFlSp4MYWjeBsHUaenHo7_aEraP8kfHVPD3Jx5VloZ4ytH9GlxGKPQCNnfI1wR6AQOw',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }

    sessions = requests.session()
    sessions.mount('https://ip.ihuan.me/', HTTP20Adapter())

    r = sessions.get(url, headers=headers)

    html = etree.HTML(r.text)
    trs = html.xpath('.//table//tbody//tr')

    arr = []
    for tr in trs:
        print(1)
        tds = tr.xpath('.//td')
        if len(tds) == 10:

            ip = tds[0].xpath('.//a/text()')[0]
            port = tds[1].text
            speed = float(tds[7].text.replace(u'秒'))

            if speed < 1:
                print('http://%s:%s' % (ip, port))
                arr.append('http://%s:%s' % (ip, port))

    f = open("proxy.json", "a")
    f.write(json.dumps({'proxy': arr}))
    f.close()


if __name__ == "__main__":
    main()
