# encoding: utf-8
# @Author : GaoCG
# @File : spyderDaily.py

import time


class SpyderDaily:

    def __init__(self, config):
        # 在此处配置
        self.current_time = time.localtime(time.time())
        self.url = config.url
        self.username = config.username
        self.password = config.password

    # test method
    def pri_job(self):
        print(self.current_time)
        print(self.url)
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    def Spyder(self):
        kid_url = self.url
        username = self.username
        data = {}
        print(kid_url)
