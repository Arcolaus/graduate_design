# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name=scrapy.Field()
    movie_url=scrapy.Field()
    
    pass
