# china-estate-analyze

## Install

项目攻关你工作在`python3`的环境里，需要首先安装`python3`及相应版本的`pip`包管理工具，其次安装如下依赖

1. `scrapy`的命令行工具，关于`scrapy`的安装和使用参考[官方文档](https://scrapy.org/)
2. `lxml`提供对`html`的解析能力
3. `pymongo`提供`python`处理`mongodb`的能力，本系统处理数据会全部存储在`mongodb`的数据库中
4. 本程序以来`mongodb`，在启动之前，需要提前配置`mongodb`数据库

## Spider

1. 安装完所有依赖宝，需要修改数据库信息，数据库信息配置在`root/spider/spider/piplines.py`中

   修改这里的`mongodb://%s:%s@192.168.31.87:27017/`修改`ip`信息和用户名密码

   ```python
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
   ```

2. 进入`spider`目录执行命令

   ```shell
   scrapy crawl ke -a city_name=上海
   ```

   

