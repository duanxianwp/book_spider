import schedule
import time
import os

cmd = '../../book_spider.sh'

def spider_job():
    os.system(cmd)


def clean_job():
    pass


# 执行清理redis队列的job
schedule.every().day.at("23:50").do(clean_job)
# 执行爬虫job
schedule.every().day.at("00:00").do(spider_job)

while True:
    schedule.run_pending()
    time.sleep(1)
