from datetime import datetime, timedelta
import sys
import os
import time

from apscheduler.schedulers.background import BackgroundScheduler


def alarm(time1):
    print('Alarm! This alarm was scheduled at %s.' % time1)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore('sqlalchemy', url='sqlite:///example.sqlite')

    scheduler.add_job(alarm, 'interval', seconds=10, args=[datetime.now()])

    scheduler.start()

    while 1:
        time.sleep(1)
        print time.time()
        scheduler.get_jobs()
        # scheduler.print_jobs()
