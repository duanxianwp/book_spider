import schedule
import time
from book.job import task

# 执行清理redis队列的job
schedule.every().day.at("23:50").do(task.clean_job)
# 执行爬虫job
schedule.every().day.at("00:00").do(task.spider_job)
# 执行爬虫job
schedule.every().day.at("08:00").do(task.push_every_day_books)

while True:
    schedule.run_pending()
    time.sleep(1)
