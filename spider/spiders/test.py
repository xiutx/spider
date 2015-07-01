# -*- coding: utf-8 -*-
import scrapy
from spider.items import SpiderItem
from scrapy.selector import Selector
import traceback

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["sohu.com"]
    start_urls = (
        'http://roll.sohu.com/20150602/n414316914.shtml',
    )


    def parse(self, response):
        item = SpiderItem()
        url = response.url
        item['url'] = url

        item['site'] = "搜狐网".decode('utf-8')
        item['column'] = '财经'.decode('utf-8')
        re = Selector(response)
        try:
            if url[7] == 'r':
                title = re.xpath('//div[@class="title"]/h1/text()').extract()
                pub_time = re.xpath('//span[@class="time"]/text()').extract()
                source = re.xpath('//div[@id="media_name"]/text()').extract()
                div = re.xpath('//div[@id="contentText"]')
            else:
                title = re.xpath('//h1[@itemprop="headline"]/text()').extract()
                div = re.xpath('//div[@itemprop="articleBody"]')
                pub_time = re.xpath('//div[@id="pubtime_baidu"]/text()').extract()
                source = re.xpath('//span[@itemprop="publisher"]/span/text()').extract()

            text = div.xpath('.//text()').extract()
            content = ''

            for i in xrange(len(text)):
                s = text[i]
                s = s.replace(" ", '')
                s = s.replace("\r", '')
                s = s.replace("\n", '')
                s = s.replace("\t", '')
                s = s.replace('\u3000', '')
                content += s
                print content

            item['title'] = title
            item['pub_time'] = pub_time
            item['source'] = source
            item['content'] = content
        except Exception, e:
            print e
            traceback.print_exc()

        return item

