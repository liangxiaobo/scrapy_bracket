import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from tutorial.items import TutorialItem
from urllib2 import *
from scrapy.exceptions import DropItem
import os

class DmozSpider(CrawlSpider):
    name = "dmoz"
    allowed_domains = ["themepixels.com"]
    start_urls = [
        "http://themepixels.com/demo/webpage/bracket/index.html"
    ]

    base_dir = os.getcwd() + "/resrouce"

    rules = (
        # Rule(LinkExtractor(allow=('\.html', ), deny=())),

        
        Rule(LinkExtractor(allow=('\.html', )), callback='parse_item'),

    )


    def create_file_not_html(self, file_url, item_file_path):
        self.log(file_url)
        if os.path.exists(file_url) == True:
            return

        with open(file_url, 'wb') as f:
            try:
                req = Request(os.path.split(self.start_urls[0])[0]+'/'+item_file_path)
                link_reponse = urlopen(req, timeout=30)
                link_page = link_reponse.read()
                #unicodePage = link_page.decode("utf-8")
                f.write(link_page)
                f.close

                self.log('%s ============' % len(link_page))

            except Exception, e:
                self.log('error  +++++++++++++++')
                # raise e


    def parse_item(self, response):
        link_items = []
        script_items = []
        a_items = []

        self.log('-------- %s' % response.url)


        # create html file 
        page_url = response.url[response.url.find('/bracket/')+len('/bracket/'): len(response.url)]
        page_url_split = os.path.split(page_url)

        if page_url_split[0]:
            self.log('not is null ..........')
            if os.path.exists(page_url_split[0]) == False:
                os.system('mkdir %s' % page_url_split[0])
                self.log("create dir {0}+++++++++++++\n".format(page_url_split[0]))



        with open('%s/%s' % (self.base_dir , page_url), 'wb') as hf:
            try:
                hf.write(response.body_as_unicode())
                hf.close()
            except Exception, e:
                raise e

        for sel in response.xpath('//link'):
            item = TutorialItem()
            item['link'] = sel.xpath('@href').extract()
            #yield item

            file_path = os.path.split('%s/%s' % (self.base_dir, item['link'][0]))
            
            if os.path.exists(file_path[0]) == False:
                os.system('mkdir %s' % file_path[0])
                self.log("create dir {0}+++++++++++++\n".format(file_path[0]))

            

            self.create_file_not_html('%s/%s' % (file_path[0], file_path[1]), item['link'][0])

            # link_items.append(item)

        for scr_item in response.xpath('//script'):
            item = TutorialItem()
            item['link'] = scr_item.xpath('@src').extract()

            if item['link']:
                file_path = os.path.split('%s/%s' % (self.base_dir, item['link'][0]))
                if os.path.exists(file_path[0]) == False:
                    os.system('mkdir %s' % file_path[0])
                    self.log("create dir {0}+++++++++++++\n".format(file_path[0]))

                self.create_file_not_html('%s/%s' % (file_path[0], file_path[1]), item['link'][0])

            # script_items.append(item)

        for img_item in response.xpath('//img'):
            item = TutorialItem()
            item['link'] = img_item.xpath('@src').extract()

            file_path = os.path.split('%s/%s' % (self.base_dir, item['link'][0]))
            if os.path.exists(file_path[0]) == False:
                os.system('mkdir %s' % file_path[0])
                self.log("create dir {0}+++++++++++++\n".format(file_path[0]))

            self.create_file_not_html('%s/%s' % (file_path[0], file_path[1]), item['link'][0])

            # a_items.append(item)

        # print(link_items)
        # print(script_items)
        # print(a_items)