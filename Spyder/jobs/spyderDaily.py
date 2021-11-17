# encoding: utf-8
# @Author : GaoCG
# @File : spyderDaily.py

import time
import requests
import json
import os
from contextlib import closing
from Spyder.logutil import errorLogs

requests.packages.urllib3.disable_warnings()


class SpyderDaily:
    log_record = errorLogs.ErrorLog()

    # test method
    def pri_job(self):
        print(self.current_time)

    def Spyder(self):
        params = {
            'client_id': 'eogdata_oidc',
            'client_secret': '2677ad81-521b-4869-8480-6d05b9e57d48',
            'username': 'cg3026@126.com',
            'password': 'gcg0624123',
            'grant_type': 'password'
        }
        finish_list = []
        token_url = 'https://eogauth.mines.edu/auth/realms/master/protocol/openid-connect/token'
        response = requests.post(token_url, data=params)
        access_token_dict = json.loads(response.text)
        access_token = access_token_dict.get('access_token')
        download_list = 'E:/GCG_storage/storage_code/File_PyCharm/nightLight/data/download_list.txt'
        auth = 'Bearer ' + access_token
        headers = {'Authorization': auth}
        with open(download_list, 'r') as d:
            line = d.readlines()[-1]
        current_time = time.strftime('%Y%m%d', time.localtime(time.time()))
        for download_time in range(int(line) + 1, int(current_time) + 1):
            data_url = 'https://eogdata.mines.edu/nighttime_light/nightly/rade9d/SVDNB_npp_d' + download_time + '.rade9d.tif'
            output_file = 'E:/GCG_storage/storage_code/File_PyCharm/nightLight/data/' + os.path.basename(data_url)
            with closing(requests.get(data_url, headers=headers, stream=True)) as response:
                if not response.status_code == '404':
                    chunk_size = 1024  # 单次请求最大值
                    content_size = int(response.headers['content-length'])  # 内容体总大小
                    data_count = 0
                    with open(output_file, 'wb') as f:
                        for data in response.iter_content(chunk_size=chunk_size):
                            f.write(data)
                            data_count = data_count + len(data)
                            now_jd = (data_count / content_size) * 100
                            print("\r 文件下载进度：%d%%(%d/%d) - %s" % (now_jd, data_count, content_size, output_file),
                                  end="")
                    f.close()
                    self.log_record.saveLog(os.path.basename(data_url) + '下载完成')
                    finish_list.append(download_time)
                else:
                    self.log_record.saveLog(os.path.basename(data_url) + '下载失败,错误码:' + response.status_code)
        d.close()
        with open(download_list, 'a') as d:
            for date in finish_list:
                d.write(date)
        d.close()
