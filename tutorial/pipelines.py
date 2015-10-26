# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from twisted.enterprise import adbapi
from hashlib import md5
import MySQLdb.cursors
import logging

log = logging.getLogger("dianping")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
file_handler = logging.FileHandler("dianping.log")
file_handler.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
log.addHandler(file_handler)
log.addHandler(stream_handler)


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class MySQLStorePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls, crawler):
        dbargs = dict(
            host=crawler.settings.get('MYSQL_HOST'),
            db=crawler.settings.get('MYSQL_DBNAME'),
            user=crawler.settings.get('MYSQL_USER'),
            passwd=crawler.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._insert, item, spider)
        d.addErrback(self.__handle_error, item, spider)
        return item

    def _insert(self, conn, item, spider):
        md5id = self._get_md5id(item)
        conn.execute("select 1 from dianping where md5id = '%s'" % md5id)
        ret = conn.fetchone()
        if ret:
            log.warn("Item already stored in db: %s" % item)
        else:
            conn.execute("insert into dianping(md5id, shop_name, shop_address, "
                         "shop_region, shop_city, shop_latitude, shop_longitude) "
                         "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                         % (md5id, item["shop_name"], item["shop_address"], item["shop_region"],
                            item["shop_city"], item["shop_latitude"], item["shop_longitude"]))
            log.info("Item stored in db: %s" % item)

    def __handle_error(self, e, item, spider):
        log.error(e)

    def _get_md5id(self, item):
        return md5(" ".join([item["shop_name"], item["shop_latitude"],
                             item["shop_longitude"]]).encode("utf8")).hexdigest()


