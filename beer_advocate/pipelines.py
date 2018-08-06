# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import io

class BeerAdvocatePipeline(object):
    def process_item(self, item, spider):
        return item



class BeerAdvocateRatingsSummaryPipeline(object):
	def __init__(self):
		self.filename = 'crawl_results.txt'

	def open_spider(self, spider):
		self.file = io.open(self.filename, 'w', encoding = 'utf-8')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		line = '||'.join(item.values()) + '\n'
		self.file.write(line)
		return item
