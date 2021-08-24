# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DevelopercrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    link = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    languages = scrapy.Field()
    contributors = scrapy.Field()
    watch = scrapy.Field()
    stars = scrapy.Field()
    forks = scrapy.Field()


