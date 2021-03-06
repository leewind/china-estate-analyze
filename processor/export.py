# -*- coding: utf-8 -*-
import pymongo
import pymysql
from lxml import etree
import re
import pandas as pd
import numpy as np
import json
import datetime
import warnings
warnings.filterwarnings("ignore")

import pymongo
import urllib

def get_city_list():
    f = open('../spider/city_list.json', 'rb')
    text = f.read()
    o = json.loads(text)
    f.close()
    return o

def get_mongo_db_client():
    username_str = 'breadt'
    password_str = 'Breadt@2019'

    username = urllib.parse.quote_plus(username_str)
    password = urllib.parse.quote_plus(password_str)

    client = pymongo.MongoClient(
        'mongodb://%s:%s@192.168.31.87:27017/' % (username, password))
    return client

def safe_get_info(html, parser, value=None):
    info_arr = html.xpath(parser)
    info = info_arr[0] if len(info_arr) > 0 else value
    return info

def parse_one(item, info):
    html = etree.HTML(item)

    house_info = html.xpath(
        '//div[@class="houseInfo"]/text()')[0].replace(' ', '')
    house_info_arr = house_info.split('|')

    if len(house_info_arr) == 5:
        year = house_info_arr[1].replace('年建', '')
    elif len(house_info_arr) == 4:
        year = house_info_arr[1].replace('年建', '')
    else:
        year = 0

    if len(house_info_arr) == 5:
        size = house_info_arr[3].replace('平米', '')
    elif len(house_info_arr) == 3:
        size = house_info_arr[1].replace('平米', '')
    else:
        size = house_info_arr[-1].replace('平米', '')

    if len(house_info_arr) == 5:
        structure = house_info_arr[2]
    elif len(house_info_arr) == 4:
        structure = house_info_arr[2]
    else:
        structure = house_info_arr[0].split(')')[1]

    if len(house_info_arr) == 5:
        op = house_info_arr[4]
    elif len(house_info_arr) == 3:
        op = house_info_arr[2]
    else:
        op = 0

    if len(house_info_arr) == 5:
        level = house_info_arr[0]
    elif len(house_info_arr) == 3:
        level = house_info_arr[0].split(')')[0]
    else:
        level = house_info_arr[0]


    tax_info = html.xpath('//span[@class="taxfree"]/text()')
    return {
        'city': info['city'],
        'district': info['district'],
        'hotpot': info['hotpot'],
        'href': safe_get_info(html, '//a[contains(@class,"maidian-detail")]/@href'),
        'title': safe_get_info(html, '//a[contains(@class,"maidian-detail")]/@title'),
        'info': house_info,
        'level': level,
        'year': year,
        'structure': structure,
        'size': size,
        'op': op,
        'price': safe_get_info(html, '//div[@class="totalPrice"]/span/text()', 0),
        'tax': safe_get_info(html, '//span[@class="taxfree"]/text()'),
        'date': info['date'],
        'address': safe_get_info(html, '//div[@class="positionInfo"]//a/text()'),
    }

def get_data_from_db(date, city):
    client = get_mongo_db_client()
    db = client['ke']

    data = []

    cursor = db['kelist'].find({'date': date, 'city': city})
    for r in cursor:

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
            one = parse_one(item)
            print(one)

            data.append(one)

    return data


if __name__ == "__main__":
    o = get_city_list()
    today = datetime.date.today()

    for info in o['cities']:
        print(info['city_name'])
        data = get_data_from_db('2019-11-26', info['city_name'])
        df = pd.DataFrame(data)

        if len(df) > 0:
            t = df.copy()
            t['price'] = t['price'].astype(np.float32)
            t['size'] = t['size'].astype(np.float32)
            t['avg_price'] = t['price'] / t['size']

            t.to_csv('../data/%s_%s.csv' % (info['city_name'], today.strftime('%Y%m%d')), index=False)
