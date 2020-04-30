# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TestSpider(CrawlSpider):
    name = 'test'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    rules = (
        Rule(LinkExtractor(allow=r'films\?showType=3&offset='), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        pass
        # item = {}
        # #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # #item['name'] = response.xpath('//div[@id="name"]').get()
        # #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
