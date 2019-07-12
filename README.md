# china-estate-analyze

## install

需要安装`scrapy`的命令行工具

## spider

1. 在ke.py文件里修改`district_name = 'zhabei'`的值，我这里用的都是上海的，需要爬其他区域的需要修改对应域名
2. 做了修正现在代码爬取的过程可以直接爬一个区，会先爬取子区域和子区域的页数，然后再去爬取
