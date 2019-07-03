# -*- coding: utf-8 -*-
import pymongo
import pymysql
from mongodb_util import get_mongo_db_client
from lxml import etree
import re


def main():
    client = get_mongo_db_client()
    db = client['ke']

    for r in db['kelist'].find().limit(1):

        content = re.sub(r'<script[^>]*?>(?:.|\n)*?<\/script>', '', r['content'])
        content = re.sub(r'<meta.+>', '', content)
        content = re.sub(r'<link.+>', '', content)
        content = re.sub(r'<!--.+-->', '', content)
        content = re.sub(r'\n', '', content)
        content = re.sub(r'<br/>', '', content)
        content = re.sub(r'<span class="houseIcon"></span>', '', content)

        pattern = re.compile(r'<li class="clear">.*?</li>')   # 查找数字
        result = pattern.findall(content)

        for item in result:
            # print(item)
            html = etree.HTML(item)

            print(html.xpath('//a[contains(@class,"maidian-detail")]/@href')[0])

            print(html.xpath('//a[contains(@class,"maidian-detail")]/@title')[0])

            # house info
            print(html.xpath('//div[@class="houseInfo"]/text()')[0].replace(' ', ''))

            # price
            print(html.xpath('//div[@class="totalPrice"]/span/text()')[0])

            # taxfree
            print(html.xpath('//span[@class="taxfree"]/text()')[0])

            print(r['date'])
            break


if __name__ == "__main__":
    main()