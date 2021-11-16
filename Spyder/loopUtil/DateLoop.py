# encoding: utf-8
# @Author : GaoCG
# @File : DateLoop.py

from apscheduler.schedulers.blocking import BlockingScheduler
import time
import argparse
from Spyder.jobs import spyderDaily
from Spyder.logutil import errorLogs

def loop(spyder_config):
    sched = BlockingScheduler()
    job = spyderDaily.SpyderDaily(spyder_config)
    log_record = errorLogs.ErrorLog()

    @sched.scheduled_job('interval', seconds=2)
    def Spyder_job():
        try:
            job.Spyder()
        except KeyboardInterrupt:
            print("用户中断")
            log_record.saveLog("用户中断")
        except IOError:
            print("IOError")

    try:
        sched.start()
    except KeyboardInterrupt:
        print("用户中断")
        log_record.saveLog("用户中断")
    except IOError:
        print("IOError")
