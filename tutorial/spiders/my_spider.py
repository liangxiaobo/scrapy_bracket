#-*- coding: UTF-8 -*- 

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tutorial.items import TutorialItem
from urllib2 import *
# import os

class MySpider(CrawlSpider):
    name = 'bracket'
    allowed_domains = ['themepixels.com']
    start_urls = ['http://themepixels.com/demo/webpage/bracket/index.html']

    rules = (
        # Rule(LinkExtractor(allow=('\.html', ), deny=())),

        #
        Rule(LinkExtractor(allow=('\.html', )), callback='parse_item'),

    )

    # def parse(self, response):
    #     self.log('Hi, this is an item page! %s' % response.url)
    #     print('load .....................2')

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        print('load .....................')

        # item = TutorialItem()
        # item['title'] = response.xpath('//title').extract()
        # return item


    # base_dir = os.getcwd() + "/resrouce"

    # rules = (
    #     # Rule(LinkExtractor(allow=('\.html', ), deny=())),

        
    #     Rule(LinkExtractor(allow=('\.html', )), callback='parse'),

    # )


  


        