# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HbogoMovieItem(scrapy.Item):
    title = scrapy.Field()
    origin_year = scrapy.Field()
    origin_country = scrapy.Field()
    genre = scrapy.Field()
    length_minutes = scrapy.Field()
    pegi = scrapy.Field()
    imdb_rating = scrapy.Field()  # from 10
    description = scrapy.Field()
    directors = scrapy.Field()
    cast = scrapy.Field()


class HbogoSeriesItem(scrapy.Item):
    title = scrapy.Field()
