# -*- coding: utf-8 -*-
import scrapy
from spider.items import SpiderItem
from scrapy.selector import Selector
import traceback

class IfengSpider(scrapy.Spider):
    name = "ifeng"
    allowed_domains = ["ifeng.com"]
    start_urls = (
        'http://finance.ifeng.com/a/20150701/13811668_0.shtml',
    )

    def parse(self, response):
        item = SpiderItem()
        item['url'] = response.url
        item['site'] = '凤凰网'
        item['column'] = '财经'
        re = Selector(response)
        try:
            #<h1 itemprop="headline" id="artical_topic">女大学生瞒着家人整容 10天内动两次刀</h1>
            title = re.xpath('//h1[@id="artical_topic"]/text()').extract()
            pub_time = re.xpath('//span[@itemprop="datePublished"]/text()').extract()
            source = re.xpath('//a[@itemprop="isBasedOnUrl"]/text()').extract()

            div = re.xpath('//div[@id="main_content"]/text()').extract()

            item['title'] = title
            item['pub_time'] = pub_time
            item['source'] = source

        except Exception, e:
            print e
            traceback.print_exc()
            item['title'] = self.get_text(response, 'head > title::text')
        return item


