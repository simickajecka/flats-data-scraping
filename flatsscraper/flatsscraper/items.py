# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlatsscraperItem(scrapy.Item):

    title =  scrapy.Field()
    prices = scrapy.Field()
    area = scrapy.Field()
    dataflat = scrapy.Field()
    description = scrapy.Field()
    coordinates = scrapy.Field()
    carousel = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    page_url = scrapy.Field()


