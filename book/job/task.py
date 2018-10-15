import os
from book.db import redisutil, dbutil, mailutil

cmd = './book_spider.sh'


def spider_job():
    os.system(cmd)


def clean_job():
    redisutil.del_set()


def push_every_day_books():
    books = redisutil.smembers()
    users = dbutil.get_all_able_user()
    if not users or not books:
        return
    # 对books进行推送
    # 推送邮件
    send_mail = '18888106880@163.com'
    message = get_message(books)
    map(lambda x: mailutil.push_email(send_mail, x['email'], message), users)
    # 推送短信


def get_message(books):
    message = '有你关注的类型书籍上线了哦，列表如下:'
    for book in books:
        book_name = '书名:{},'.format(book['book_name'])
        message = message + book_name
    return message