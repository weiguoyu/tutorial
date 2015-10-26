# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import DianpingItem

class MySpider(scrapy.Spider):
    name = 'dianping'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/search/keyword/1/0_早餐面馆网']
    #start_urls = ['http://www.dianping.com/search/keyword/1/0_早餐面馆网/r12#nav-tab|0|1']

    def parse(self, response):
        for href in response.xpath('//div[@id="region-nav"]//a'):
            url = response.urljoin(href.xpath('@href').extract()[0])
            area = href.xpath('./span/text()').extract()[0]
            import time
            time.sleep(1)
            print "##################"
            print url
            print area
            yield scrapy.Request(url, callback=self.parse_area)

    def parse_area(self, response):
        print "********************"
        for href in response.xpath('//div[@id="region-nav-sub"]//a')[1:]:
            url = response.urljoin(href.xpath('@href').extract()[0])
            area = href.xpath('./span/text()').extract()[0]
            import time
            time.sleep(1)
            print url
            print area
            print "before Request"
            yield scrapy.Request(url, callback=self.parse_page)

        # 不限
        for href in response.xpath('//div[@class="shop-list J_shop-list shop-all-list"]//a[@data-hippo-type="shop"]'):
            url = response.urljoin(href.xpath('@href').extract()[0])
            shop = href.xpath('@title').extract()[0]
            print url
            print shop
            yield scrapy.Request(url, callback=self.parse_shop)

    def parse_page(self, response):
        print "-----------------------"
        print response.url
        import time
        time.sleep(1)
        for href in response.xpath('//div[@class="shop-list J_shop-list shop-all-list"]//a[@data-hippo-type="shop"]'):
            url = response.urljoin(href.xpath('@href').extract()[0])
            shop = href.xpath('@title').extract()[0]
            print url
            print shop
            yield scrapy.Request(url, callback=self.parse_shop)
        next_url = response.xpath('//div[@class="page"]//a[@class="next"]')
        if next_url:
            next_url = response.urljoin(next_url.xpath('@href').extract()[0])
            yield scrapy.Request(next_url, callback=self.parse_page)

    def parse_shop(self, response):
        item = DianpingItem()
        print "$$$$$$$$$$$$$$"
        print response.url
        import time
        time.sleep(1)
        item['shop_name'] = response.xpath('//h1[@class="shop-name"]//text()').extract()[0].strip()
        item['shop_address'] = response.xpath('//div[@class="expand-info address"]//span[@itemprop="street-address"]/@title').extract()[0]
        lng_atr = response.xpath('//div[@id="aside"]/script/text()').re(r"lng:(\d*.\d*),lat:(\d*.\d*)")
        item['shop_longitude'], item['shop_latitude'] = lng_atr
        item['shop_city'] = response.xpath('//a[@class="city J-city"]//text()').extract()[0].strip()
        item['shop_region'] = response.xpath('//span[@itemprop="locality region"]//text()').extract()[0].strip()
        return item




