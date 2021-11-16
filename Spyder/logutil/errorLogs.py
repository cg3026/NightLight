# encoding: utf-8
# @Author : GaoCG
# @File : errorLogs.py

import time
import os

logs_path = './logs'


class ErrorLog:

    def __init__(self):
        current_path = os.getcwd()
        root_path = os.path.dirname(current_path)
        self.root_path = root_path + '\\logs\\'
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)

    def saveLog(self, loginfo):
        log_time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
        log_path = self.root_path + log_time
        if os.path.exists(log_path):
            raise Exception("Log日期出现重复")
        else:
            f = open(log_path, 'a')
            f.write(loginfo)
