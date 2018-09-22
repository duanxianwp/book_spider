# -*- coding: utf-8 -*-
import json
import re

from book.db import dbutil
import scrapy
from bs4 import BeautifulSoup

from book.items import BookItem


class IturingSpider(scrapy.Spider):
    name = 'ituring'
    allowed_domains = ['www.ituring.com.cn']
    start_urls = ['http://www.ituring.com.cn/']
    detail_page = 0
    book_detail_url = 'http://www.ituring.com.cn/book?tab=book&sort=new&category=1&page={}'

    def start_requests(self):
        yield scrapy.Request(self.book_detail_url.format(self.detail_page), callback=self.parse_booke_detail)

    def parse_booke_detail(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        hrefs = soup.select('h4.name > a')
        if len(hrefs) < 1:
            return
        for a in hrefs:
            href = self.start_urls[0][:-1] + a.get('href')
            yield scrapy.Request(url=href, callback=self.parse_book_info)
            # 判断是否要继续往下一页爬

        href = self.start_urls[0][:-1] + hrefs[-1].get('href')
        # 查询是否已经爬过，查数据库
        is_exist = dbutil.is_exist(href)
        if not is_exist:
            self.detail_page = self.detail_page + 1
            yield scrapy.Request(self.book_detail_url.format(self.detail_page), callback=self.parse_booke_detail)

    def parse_book_info(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        item = BookItem()
        item['book_name'] = self.get_text(soup.select_one('div.book-title'))
        item['author'] = self.get_text_with_no(soup.select_one('div.book-author > span:nth-of-type(1)'), '(', 0)
        item['translator'] = self.get_text_with_no(soup.select_one('div.book-author > span:nth-of-type(2)'), '(', 0)
        item['editor'] = self.get_list_one_text(re.findall(re.compile('请联系\\s<a.*>(.*?)</a>'), response.text))
        item['price'] = self.get_text(soup.select_one('span.price'))
        item['isbn'] = self.get_list_one_text(re.findall(re.compile('书\\s+号</strong>(.*?)</li>'), response.text))
        item['publish_status'] = self.get_list_one_text(
            re.findall(re.compile('出版状态</strong>(.*?)</li>'), response.text))
        item['publish_date'] = self.get_list_one_text(re.findall(re.compile('出版日期</strong>(.*?)</li>'), response.text))
        item['origin_book_name'] = self.get_list_one_text(
            re.findall(re.compile('原书名</strong><a.*>(.*?)</a>'), response.text))
        item['origin_book_price'] = self.get_text(soup.select_one('s'))
        item['pages'] = self.get_list_one_text(re.findall(re.compile('页\\s+数</strong>(.*?)</li>'), response.text))
        item['format'] = self.get_list_one_text(re.findall(re.compile('开\\s+本</strong>(.*?)</li>'), response.text))
        item['introduction'] = self.get_text(soup.select_one('div.book-intro'))
        item['origin_book_isbn'] = self.get_list_one_text(
            re.findall(re.compile('原书号</strong><a.*>(.*?)</a'), response.text))
        item['avatar'] = soup.select_one('div.book-img  > a > img').get('src')
        item['tags'] = json.dumps(re.findall(re.compile('post-tag">(.*?)</a>'), response.text))
        item['book_url'] = response.request.url
        item['website'] = '图灵社区'
        yield item

    @staticmethod
    def get_text(string):
        if string:
            return string.text.strip()
        else:
            return None

    @staticmethod
    def get_text_with_no(string, sp, index):
        if string:
            return "".join(string.text.split()).split(sp)[index].strip()
        else:
            return None

    @staticmethod
    def get_list_one_text(texts):
        if len(texts) > 0:
            return texts[0].strip()
        else:
            return None
