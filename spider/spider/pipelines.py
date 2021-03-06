# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import SpidersKeList
from lxml import etree
import urllib
import pymongo
import re

class SpiderPipeline(object):

    username_str = 'breadt'
    password_str = 'Breadt@2019'

    def connect(self):

        username = urllib.parse.quote_plus(self.username_str)
        password = urllib.parse.quote_plus(self.password_str)

        self.client = pymongo.MongoClient('mongodb://%s:%s@192.168.31.87:27017/' % (username, password))
        self.db = self.client["ke"]

    def open_spider(self, spider):
        print('SpidersPipeline.open_spider')
        self.connect()

    def process_item(self, item, spider):

        data = []
        if isinstance(item, SpidersKeList):
            data = self.parse_content(item)

            # feedback = self.db["kelist"].insert_one({
            #     'content': item['content'],
            #     'district': item['district'],
            #     'city': item['city'],
            #     'hotpot': item['hotpot'],
            #     'date': item['date']
            # })

        return data

    def safe_get_info(self, html, parser, value=None):
        info_arr = html.xpath(parser)
        info = info_arr[0] if len(info_arr) > 0 else value
        return info

    def parse_one(self, item, info):
        html = etree.HTML(item)

        house_info = html.xpath('//div[@class="houseInfo"]/text()')[0].replace(' ', '')
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

        href = self.safe_get_info(html, '//a[contains(@class,"maidian-detail")]/@href')

        id = 0
        items = re.findall('\d+\.html', href)
        if href is not None and len(items) > 0:
            id = items[0].replace('.html', '')

        return {
            'uid': info['date'] + '_' + str(id),
            'id': id,
            'city': info['city'],
            'district': info['district'],
            'hotpot': info['hotpot'],
            'href': href,
            'title': self.safe_get_info(html, '//a[contains(@class,"maidian-detail")]/@title'),
            'info': house_info,
            'level': level,
            'year': year,
            'structure': structure,
            'size': size,
            'op': op,
            'price': self.safe_get_info(html, '//div[@class="totalPrice"]/span/text()', 0),
            'tax': self.safe_get_info(html, '//span[@class="taxfree"]/text()'),
            'date': info['date'],
            'address': self.safe_get_info(html, '//div[@class="positionInfo"]//a/text()'),
        }

    def parse_content(self, info):
        content = re.sub(r'<script[^>]*?>(?:.|\n)*?<\/script>', '', info['content'])
        content = re.sub(r'<meta.+>', '', content)
        content = re.sub(r'<link.+>', '', content)
        content = re.sub(r'<!--.+-->', '', content)
        content = re.sub(r'\n', '', content)
        content = re.sub(r'<br/>', '', content)
        content = re.sub(r'<span class="houseIcon"></span>', '', content)

        pattern = re.compile(r'<li class="clear">.*?</li>')   # 查找数字
        result = pattern.findall(content)

        data = []
        for item in result:
            one = self.parse_one(item, info)
            feedback = self.db["kelist"].insert_one(one)
            data.append(one)

        return data


    def close_spider(self, spider):
        self.client.close()
