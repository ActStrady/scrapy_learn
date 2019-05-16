#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/16 11:45
# @Author : ActStrady@tom.com
# @FileName : image_spider.py
# @GitHub : https://github.com/ActStrady/scrapy_learn

"""
一些爬取数据的类，这些类继承自基类Spider
"""

from scrapy import Spider
from scrapy import Request


class PhotoTakenImageSpider(Spider):
    """
    爬取摄图网的照片http://699pic.com/photo/
    """
    # spider的名字，执行爬虫要使用该名
    name = 'photo_taken_images'

    # 初始请求，要请求的页面
    def start_requests(self):
        url = 'http://699pic.com/photo/'
        # Request默认会交由parse函数去执行。要指定就使用callback来指定
        yield Request(url)

    # 默认的解析函数，Request()会交由其处理
    def parse(self, response):
        # 解析到所有图片分组url
        group_urls = response.xpath(".//div[class='pl-list'/a[first()]/@href]").extract()
        for group_url in group_urls:
            # 请求组页面,交给下一解析函数
            yield Request(group_url, callback=self.image_li_parse)

    # 解析列表小图片
    def image_li_parse(self, response):
        # 小图片列表
        image_li_urls = response.xpath(".//li/a/@href").extract()
        for image_li_url in image_li_urls:
            yield Request(image_li_url, callback=self.image_parse)

    def image_parse(self, response):
        image_url = response.xpath(".//div[@class='huabu']/a[1]/img/@src").extract()
        