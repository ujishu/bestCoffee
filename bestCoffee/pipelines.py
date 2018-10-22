# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2

class BestcoffeePipeline(object):
    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'db_admin'
        password = 'argon1111,,'
        database = 'bestcoffe'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def process_item(self, item, spider):
        self.cur.execute("insert into amazon() values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (item['time'],
                                                                item['title'],
                                                                item['product_url'],
                                                                item['image_url'],
                                                                item['price'],
                                                                item['currency'],
                                                                item['site'],
                                                                item['location'],
                                                                item['product_rating']))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
