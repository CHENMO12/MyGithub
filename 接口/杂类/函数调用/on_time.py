#!/usr/bin/python3.7
# @Time : 2020/10/27 18:11
import time
from apscheduler.schedulers.blocking import BlockingScheduler


def job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


if __name__ == '__main__':
    # BlockingScheduler：在进程中运行单个任务，调度器是唯一运行的东西
    scheduler = BlockingScheduler()
    # 采用阻塞的方式
    a = 28
    while True:
        # 采用date的方式，在特定时间只执行一次
        date = '2020-10-{} 09:30:00'.format(a)
        scheduler.add_job(job, 'date', run_date=date)
        scheduler.start()
        a += 1
