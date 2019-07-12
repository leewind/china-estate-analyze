# -*- coding: utf-8 -*-
import scrapy
from ..items import SpidersKeList
import datetime

class KeSpider(scrapy.Spider):
    name = 'ke'
    allowed_domains = ['ke.com']
    start_urls = ['http://ke.com/']

    domain = 'https://sh.ke.com/ershoufang/%s/pg%d/'

    def start_requests(self):
        # self.connect()

        current_date = datetime.datetime.now()

        #TODO 如何获取这部分数据，需要处理一下
        district = [{
            'name': 'beicai',
            'count': 41
        }, {
            'name': 'biyun',
            'count': 8
        }, {
            'name': 'caolu',
            'count': 16
        }, {
            'name': 'chuansha',
            'count': 35
        }, {
            'name': 'datuanzhen',
            'count': 3
        }, {
            'name': 'gaodong',
            'count': 5
        }, {
            'name': 'gaohang',
            'count': 11
        }, {
            'name': 'geqing',
            'count': 4
        }, {
            'name': 'hangtou',
            'count': 10
        }, {
            'name': 'huamu',
            'count': 13
        }, {
            'name': 'huinan',
            'count': 30
        }, {
            'name': 'jinqiao',
            'count': 60
        }, {
            'name': 'jinyang',
            'count': 29
        },{
            'name': 'kangqiao',
            'count': 20
        },{
            'name': 'laogangzhen',
            'count': 20
        },{
            'name': 'lianyang',
            'count': 5
        },{
            'name': 'lingangxincheng',
            'count': 5
        },{
            'name': 'lujiazui',
            'count': 22
        },{
            'name': 'nanmatou',
            'count': 8
        },{
            'name': 'nichengzhen',
            'count': 10
        },{
            'name': 'sanlin',
            'count': 42
        },{
            'name': 'shibo',
            'count': 29
        },{
            'name': 'shuyuanzhen',
            'count': 3
        },{
            'name': 'tangqiao',
            'count': 15
        },{
            'name': 'tangzhen',
            'count': 17
        },{
            'name': 'waigaoqiao',
            'count': 15
        },{
            'name': 'wanxiangzhen',
            'count': 2
        },{
            'name': 'weifang',
            'count': 14
        },{
            'name': 'xinchang',
            'count': 9
        },{
            'name': 'xuanqiao',
            'count': 6
        },{
            'name': 'yangdong',
            'count': 10
        },{
            'name': 'yangjing',
            'count': 14
        },{
            'name': 'yuanshen',
            'count': 15
        },{
            'name': 'yuqiao1',
            'count': 8
        },{
            'name': 'zhangjiang',
            'count': 25
        },{
            'name': 'zhoupu',
            'count': 26
        },{
            'name': 'zhuqiao',
            'count': 5
        }]

        for item in district:
            for i in range(1, item['count'] + 1):
                yield scrapy.Request(
                    method='get',
                    url=self.domain % (item['name'], i),
                    callback=self.parse,
                    meta={
                        'date': current_date.strftime("%Y-%m-%d")
                    }
                )

    def parse(self, response):
        if response.text is not None:
            yield SpidersKeList(content=response.text, date=response.meta['date'])