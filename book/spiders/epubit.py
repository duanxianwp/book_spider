# -*- coding: utf-8 -*-
import json

import scrapy

from book.items import BookItem
from book.db import dbutil


class EpubitSpider(scrapy.Spider):
    name = 'epubit'
    allowed_domains = ['www.epubit.com']
    start_urls = ['https:/www.epubit.com/']
    detail_page = 1
    book_detail_url = 'https://www.epubit.com/book/search'
    book_info_url = 'https://www.epubit.com/book/getDetail'
    book_store_url = 'https://www.epubit.com/book/detail?id={}'
    detail_form_param = {
        'rows': '12',
        'searchColumn': '',
        'eleEdPrice': '',
        'categoryId': '',
        'order': 'desc',
        'sort': 'publishDate',
        'listed': '1',
        'isPaper': '1',
        'salesStatus': '',
        'condition': 'booklist'
    }

    def start_requests(self):
        self.detail_form_param['page'] = str(self.detail_page)
        yield scrapy.FormRequest(
            url=self.book_detail_url,
            formdata=self.detail_form_param,
            callback=self.parse_book_detail
        )

    def parse_book_detail(self, response):
        res = json.loads(response.text)
        if not res:
            return
        rows = res.get('data').get('rows')
        if not rows or len(rows) < 1:
            return
        for row in rows:
            book_id = row.get('id')
            yield scrapy.FormRequest(
                url=self.book_info_url,
                formdata={'id': book_id},
                callback=self.parse_book_info
            )
        # 查询是否已经爬过，查数据库
        href = self.book_store_url.format(rows[-1].get('id'))
        is_exist = dbutil.is_exist(href)
        if not is_exist:
            self.detail_page = self.detail_page + 1
            self.detail_form_param['page'] = str(self.detail_page)
            yield scrapy.FormRequest(
                url=self.book_detail_url,
                formdata=self.detail_form_param,
                callback=self.parse_book_detail
            )

    def parse_book_info(self, response):
        res = json.loads(response.text).get('data')
        item = BookItem()
        item['book_name'] = res.get('name')
        item['author'] = res.get('author')
        item['translator'] = res.get('translator')
        item['editor'] = res.get('executiveEditor')
        item['price'] = res.get('discountBookPrice')
        item['isbn'] = res.get('isbn')
        item['publish_status'] = res.get('exStatus')
        item['publish_date'] = res.get('publishDate')
        item['origin_book_name'] = res.get('originalBookName')
        item['origin_book_price'] = res.get('unitPrice')
        item['pages'] = res.get('pages')
        item['format'] = res.get('exBookSize')
        item['introduction'] = res.get('resume')
        item['origin_book_isbn'] = None
        item['avatar'] = 'https://www.epubit.com/oldres/writeBookImg/' + res.get('id')
        item['tags'] = self.get_tags_text(res.get('categoryFullName'))
        item['book_url'] = response.request.url
        item['website'] = '异步社区'
        yield item

    @staticmethod
    def get_tags_text(string):
        if string:
            return str(string.strip().split('>'))
        else:
            return None
