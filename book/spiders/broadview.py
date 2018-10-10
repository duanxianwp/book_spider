# -*- coding: utf-8 -*-
import json
import re
import scrapy
from bs4 import BeautifulSoup
from book.db import dbutil
from book.items import BookItem


class BroadviewSpider(scrapy.Spider):
    name = 'broadview'
    allowed_domains = ['www.broadview.com.cn']
    start_urls = ['http://www.broadview.com.cn/']
    detail_page = 0
    book_detail_url = 'http://www.broadview.com.cn/book?tab=book&sort=new&page={}'

    def start_requests(self):
        yield scrapy.Request(self.book_detail_url.format(self.detail_page), callback=self.parse_booke_detail)

    def parse_booke_detail(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        hrefs = soup.select('div.book-img > a')
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
        item['book_name'] = self.get_text(soup.select_one('h2.book-name'))
        item['author'] = soup.select_one('p.book-author').text.strip().split('(')[0].strip().replace('\n','').replace(' ','').strip()
        item['translator'] = self.get_list_one_text(
            re.findall(re.compile('<a.*>(.*?)\\s+</a>\\s+\(译者\)'), response.text))
        item['editor'] = self.get_list_one_text(re.findall(re.compile('维护人：\\S+<a.*>(.*?)</a>'), response.text))
        price_text = re.findall(re.compile('price\\S>(.*?)</span>'), response.text)
        item['price'] = None if (len(price_text) < 2 or price_text[1].find('￥') < 0) else price_text[1]
        item['isbn'] = self.get_list_one_text(re.findall(re.compile('书\\s+号\\S+>(.*?)\\s+</li>'), response.text))
        item['publish_status'] = self.get_list_one_text(
            re.findall(re.compile('出版状态\\S+>(.*?)\\s+</li>'), response.text))
        item['publish_date'] = self.get_list_one_text(re.findall(re.compile('出版日期\\S+>(.*?)\\s+</li>'), response.text))
        item['origin_book_name'] = self.get_list_one_text(
            re.findall(re.compile('原书名\\S+n>\\s+(.*?)\\s+</li>'), response.text))
        item['origin_book_price'] = None
        item['pages'] = self.get_list_one_text(re.findall(re.compile('页\\s+数\\S+>(.*?)\\s+</li>'), response.text))
        item['format'] = self.get_list_one_text(re.findall(re.compile('开\\s+本\\S+>(.*?)\\s+</li>'), response.text))
        item['introduction'] = self.get_text(soup.select_one('div#abstract'))
        item['origin_book_isbn'] = self.get_list_one_text(
            re.findall(re.compile('原书号\\S+>(.*?)\\s+</li>'), response.text))
        item['avatar'] = soup.select_one('div.book-detail-img  > a > img').get('src')
        item['tags'] = self.get_tags_text(soup.select('div.block-tag > div.block-body > ul > li > a'))
        item['book_url'] = response.request.url
        item['website'] = '博文视点'
        #特殊处理
        if str(item['isbn']).strip() == '':
            item['isbn'] = None
        yield item

    @staticmethod
    def get_text(string):
        if string:
            return "".join(string.text.replace(" ", "").replace("\n\r", '').split())
        else:
            return None

    @staticmethod
    def get_list_one_text(texts):
        if len(texts) > 0:
            return texts[0].strip()
        else:
            return None

    @staticmethod
    def get_tags_text(req):
        if not req or len(req) < 1:
            return None
        return json.dumps(list(map(lambda x: x.text, req)))