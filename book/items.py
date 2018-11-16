# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class BookItem(scrapy.Item):
    book_name = Field()
    author = Field()
    translator = Field()
    editor = Field()
    price = Field()
    isbn = Field()
    publish_status = Field()
    publish_date = Field()
    origin_book_name = Field()
    origin_book_price = Field()
    pages = Field()
    format = Field()
    introduction = Field()
    origin_book_isbn = Field()
    avatar = Field()
    tags = Field()
    book_url = Field()
    website = Field()


class BusItem(scrapy.Item):
    title = Field()
    no = Field()
    publish_date = Field()
    time = Field()
    maker = Field()
    category = Field()
    actors = Field()
    photo = Field()
    magent = Field()
    url = Field()
