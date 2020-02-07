import requests
from lxml import etree
import base64
import json


def main():

    url = 'http://free-proxy.cz/zh/proxylist/country/CN/http/ping/all'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Host': 'free-proxy.cz',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://free-proxy.cz/zh/proxylist/country/CN/all/ping/all',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    r = requests.get(url, headers=headers)

    html = etree.HTML(r.text)
    trs = html.xpath('.//table[@id="proxy_list"]//tbody//tr')

    arr = []
    for tr in trs:
        tds = tr.xpath('.//td')
        if len(tds) == 11:

            script = tds[0].xpath('.//script/text()')[0]
            code = script.replace(
                'document.write(Base64.decode("', '').replace('"))', '')

            ip = base64.b64decode(code).decode("utf-8")
            port = tds[1].xpath('.//span/text()')[0]
            protocol = tds[2].xpath('.//small/text()')[0]

            arr.append({
                'ip': ip,
                'port': port,
                'protocol': protocol
            })

    f = open("proxy.json", "a")
    f.write(json.dumps({'proxy': arr}))
    f.close()


if __name__ == "__main__":
    main()
