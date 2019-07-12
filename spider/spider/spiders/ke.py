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

    district_name = 'zhabei'

    domain = 'https://sh.ke.com/ershoufang/%s/pg%d/'
    district = 'https://sh.ke.com/ershoufang/%s/'
    main = 'https://sh.ke.com'

    def start_requests(self):
        current_date = datetime.datetime.now()
        yield scrapy.Request(
            method='get',
            url=self.district % ('zhabei'),
            callback=self.parse_district,
            meta={
                'date': current_date.strftime("%Y-%m-%d")
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

    def parse_district(self, response):
        if response.text is not None:
            content = self.clean(response.text)

            html = etree.HTML(content)
            divs = html.xpath('.//div[@data-role="ershoufang"]//div')
            hrefs = divs[1].xpath('.//a/@href')

            for href in hrefs:
                yield scrapy.Request(
                    method='get',
                    url=self.main + href,
                    callback=self.parse_len,
                    meta={
                        'date': response.meta['date'],
                        'href': href
                    }
                )

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
                        url=self.main + response.meta['href'] + 'pg'+ str(i) + '/',
                        callback=self.parse,
                        meta={
                            'date': response.meta['date']
                        }
                    )

    def parse(self, response):
        if response.text is not None:
            yield SpidersKeList(content=response.text, district=self.district_name, date=response.meta['date'])