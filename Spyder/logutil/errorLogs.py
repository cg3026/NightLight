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
        log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        log_path = self.root_path + 'log.txt'
        f = open(log_path, 'a')
        f.write("[" + log_time + "]  " + loginfo + '\n')

