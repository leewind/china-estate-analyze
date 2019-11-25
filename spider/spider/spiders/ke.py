# -*- coding: utf-8 -*-
import scrapy
from ..items import SpidersKeList
import datetime
import re
from lxml import etree
import json

class KeSpider(scrapy.Spider):
    name = 'ke'
    allowed_domains = ['ke.com']
    start_urls = ['http://ke.com/']

    def start_requests(self):

        f = open('city_list.json', 'rb')
        text = f.read()
        o = json.loads(text)

        current_date = datetime.datetime.now()
        for city in o['cities']:
            for district in city['districts']:
                for hotpot in district['hotpot']:

                    yield scrapy.Request(
                        method='get',
                        url= city['city_host'] + hotpot['url'],
                        callback=self.parse_len,
                        meta={
                            'city_name': city['city_name'],
                            'district_name': district['district_name'],
                            'hotpot_name': hotpot['hotpot'],
                            'date': current_date.strftime("%Y-%m-%d"),
                            'href': city['city_host'] + hotpot['url']
                        }
                    )

    def clean(slef, content):
        content = re.sub(r'<script[^>]*?>(?:.|\n)*?<\/script>', '', content)
        content = re.sub(r'<meta.+>', '', content)
        content = re.sub(r'<link.+>', '', content)
        content = re.sub(r'<!--.+-->', '', content)
        content = re.sub(r'\n', '', content)
        content = re.sub(r'<br/>', '', content)
        content = re.sub(r'<span class="houseIcon"></span>', '', content)
        return content

    def parse_len(self, response):
        if response.text is not None:
            content = self.clean(response.text)
            html = etree.HTML(content)
            page_data = html.xpath('.//div[contains(@class, "house-lst-page-box")]/@page-data')
            for data in page_data:
                o = json.loads(data)
                for i in range(1, o['totalPage'] + 1):
                    yield scrapy.Request(
                        method='get',
                        url=response.meta['href'] + 'pg'+ str(i) + '/',
                        callback=self.parse,
                        meta={
                            'city_name': response.meta['city_name'],
                            'district_name': response.meta['district_name'],
                            'hotpot_name': response.meta['hotpot_name'],
                            'href': response.meta['href'],
                            'date': response.meta['date']
                        }
                    )

    def parse(self, response):
        if response.text is not None:
            yield SpidersKeList(
                content=response.text,
                district=response.meta['district_name'],
                hotpot = response.meta['hotpot_name'],
                city = response.meta['city_name'],
                date=response.meta['date']
            )