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

        # content = r['content'].replace(/<script[^>]*?>(?:.|\n)*?<\/script>/i, '')
        content = re.sub(r'<script[^>]*?>(?:.|\n)*?<\/script>', '', r['content'])
        content = re.sub(r'<!--.+-->', '', content)
        html = etree.HTML(content)

        li_list = html.xpath('//ul[@class="sellListContent"]//li')
        for li in li_list:
            print(etree.tostring(li, pretty_print=True))
            break


if __name__ == "__main__":
    main()