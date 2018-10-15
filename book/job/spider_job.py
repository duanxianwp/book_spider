import schedule
import time
import sys
sys.path.append('./')
from book.job import task

# 执行清理redis队列的job
schedule.every().day.at("23:50").do(task.clean_job)
# 执行爬虫job
schedule.every().day.at("23:00").do(task.spider_job)
# 执行推送job
schedule.every().day.at("23:30").do(task.push_every_day_books)

while True:
    schedule.run_pending()
    time.sleep(1)
