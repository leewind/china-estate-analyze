# -*- coding: utf-8 -*-
import pymongo
import pymysql
from mongodb_util import get_mongo_db_client
from lxml import etree


def main():
    client = get_mongo_db_client()
    db = client['ke']

    for r in db['kelist'].find().limit(1):
        html = etree.HTML(r['content'], etree.HTMLParser())

        li_list = html.xpath('//ul[@class="sellListContent"]//li')
        print(len(li_list))
        for li in li_list:

            print(etree.tostring(li, pretty_print=True))
            break


if __name__ == "__main__":
    main()