# encoding: utf-8
# @Author : GaoCG
# @File : DateLoop.py

from apscheduler.schedulers.blocking import BlockingScheduler
import time
import argparse
from Spyder.jobs import spyderDaily
from Spyder.logutil import errorLogs


def loop():
    sched = BlockingScheduler()
    job = spyderDaily.SpyderDaily()
    log_record = errorLogs.ErrorLog()

    def Spyder_job():
        try:
            job.pri_job()
        except KeyboardInterrupt:
            print("用户中断")
            log_record.saveLog("用户中断")
        except IOError:
            print("IOError")

    sched.add_job(Spyder_job(), 'cron', day_of_week='mon-sun', hour=0, minute=10, second=0)

    try:
        sched.start()
    except KeyboardInterrupt:
        print("用户中断")
        log_record.saveLog("用户中断")
    except IOError:
        print("IOError")
