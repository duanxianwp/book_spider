import os

from book.db import redisutil, dbutil, mailutil

cmd = './book_spider.sh'


def spider_job():
    os.system(cmd)


def clean_job():
    redisutil.del_set()


def push_every_day_books():
    #books = redisutil.lrange()
    # book 从mysql里查，redis 老超时
    books = dbutil.get_today_books()
    users = dbutil.get_all_able_user()
    if not users or not books:
        return
    # 对books进行推送
    # 推送邮件
    message = get_message(books)
    for user in users:
        mailutil.push_email(user.email, message)
    # 推送短信


def get_message(books):
    message = '有你关注的类型书籍上线了哦，列表如下:'
    for book in books:
        book = eval(str(book, encoding='utf-8'))
        book_name = '**{}**,'.format(book['book_name'])
        message = message + book_name
    return message
