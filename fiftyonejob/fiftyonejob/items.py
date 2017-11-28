# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FiftyonejobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class FiftyOneJobItem(scrapy.Item):
    url = scrapy.Field()
    enterprise_name = scrapy.Field()
    pname = scrapy.Field()
    smoney = scrapy.Field()
    emoney = scrapy.Field()
    plocation = scrapy.Field()
    parea = scrapy.Field()
    experience = scrapy.Field()
    position_education = scrapy.Field()
    tags = scrapy.Field()
    date_pub = scrapy.Field()
    advantage = scrapy.Field()
    jobdesc = scrapy.Field()
    ptype = scrapy.Field()
    crawl_time = scrapy.Field()
    pnumber = scrapy.Field()
    company_profile = scrapy.Field()