# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from spider.items import SpiderItem
from scrapy.http.request import Request
import time
import re

import base64


class PbcSpider(CrawlSpider):
    time = time.time()
    last_time = time - 36000
    name = "pbc"
    allowed_domains = ["pbc.gov.cn"]
    start_urls = (
        'http://www.pbc.gov.cn/',
    )

    def trans(self, a, b, c):
        tmp = a + b
        zhishu = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        hash = 0

        for i in xrange(len(tmp)):
            hash += ord(tmp[i])

        hash *= zhishu[c]
        hash += 111111
        return "WZWS_CONFIRM_PREFIX_LABEL" + str(c) + str(hash)

    def parse(self, response):
        body = response.body
        randomstr = re.findall(r'(RANDOMSTR[0-9]{3,5})', body)
        randomint = re.findall(r'(WZWS_CONFIRM_PREFIX_LABEL.{1})', body)
        x = "STRRANDOM"+randomstr[0][9:]

        c = int(randomint[0][-1])
        a = randomstr[0]
        confirm = self.trans(a, x, c)

        wzwstemplate = base64.b64encode(str(c))
        wzwschallenge = base64.b64encode(confirm)
        wzwsconfirm = response.headers['Set-Cookie'][12:-8]

        self.cookie = {"wzwsconfirm":wzwsconfirm,"wzwstemplate":wzwstemplate,"wzwschallenge":wzwschallenge}
        yield Request('http://www.pbc.gov.cn/', method="POST", cookies=self.cookie, callback=self.parse_page)

    def parse_page(self, response):
        res = Selector(response)
        a = res.xpath('//a[@class="hei12"]/@href').extract()

        for i in xrange(len(a)):
            if len(a[i]) > 70:
                yield Request('http://www.pbc.gov.cn'+a[i], method="POST", cookies=self.cookie, callback=self.parse_item)

    def parse_item(self, response):
        item = SpiderItem()
        res = Selector(response)
        pub_time = res.xpath('//td[@align="right" and @class="hui12"]/text()').extract()
        timearray = time.strptime(pub_time[0], "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(timearray))
        if timestamp > self.last_time:
            con = res.xpath('//p')
            content = con.xpath('.//text()').extract()
            source = res.xpath('//td[@align="middle" and  @class="hui12"]/text()').extract()[0][5:]
            title = res.xpath('//h2/text()').extract()
            column = res.xpath('//a[@class="navigation_style"]/text()').extract()[-1]
            item['url'] = response.url
            item['site'] = '中国人民银行'.decode('utf-8')
            item['column'] = column
            item['title'] = title
            item['pub_time'] = pub_time
            item['source'] = source
            item['content'] = content
            return item




