import os
from book.db import redisutil, dbutil

cmd = './book_spider.sh'


def spider_job():
    os.system(cmd)


def clean_job():
    redisutil.del_set()


def push_every_day_books():
    books = redisutil.smembers()
    users = dbutil.get_all_able_user()
    if not users:
        return
    # 对books进行推送
     # 推送邮件
     # 推送短信
    
