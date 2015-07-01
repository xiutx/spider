# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class SpiderPipeline(object):
    def process_item(self, item, spider):
        out = []
        for column in self.columns:
            out.append(item[column] if column in item else '')
        for i in xrange(len(out)):
            self.file.write('\001'.join(out[i])+'\n')

        return item

    def open_spider(self, spider):
        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')
        self.file = open('%s_%s.txt' % (spider.name, date), 'wt')
        self.columns = ('site', 'column', 'url', 'title', 'pub_time', 'source', 'content')

    def close_spider(self, spider):
        self.file.close()