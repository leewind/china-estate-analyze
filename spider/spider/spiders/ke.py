# -*- coding: utf-8 -*-
import scrapy
from ..items import SpidersKeList


class KeSpider(scrapy.Spider):
    name = 'ke'
    allowed_domains = ['ke.com']
    start_urls = ['http://ke.com/']

    domain = 'https://sh.ke.com/ershoufang/zhabei/pg%dl2/'

    def start_requests(self):
        # self.connect()

        current_date = datetime.datetime.now()

        for i in range(1, 45):
            yield scrapy.Request(
                method='get',
                url=self.domain % (i),
                callback=self.parse,
                meta={
                    'date': current_date.strftime("%Y-%m-%d")
                }
            )

    def parse(self, response):
        if response.text is not None:
            yield SpidersKeList(content=response.text, date=response.meta['date'])
