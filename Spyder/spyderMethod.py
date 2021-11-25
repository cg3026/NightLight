import requests
import json
import os
from contextlib import closing
import time
import datetime
from Spyder.logutil import errorLogs
requests.packages.urllib3.disable_warnings()

log_record = errorLogs.ErrorLog()
# Retrieve access token
params = {
            'client_id': 'eogdata_oidc',
            'client_secret': '2677ad81-521b-4869-8480-6d05b9e57d48',
            'username': 'cg3026@126.com',
            'password': 'gcg0624123',
            'grant_type': 'password'
        }
finish_list = []
token_url = 'https://eogauth.mines.edu/auth/realms/master/protocol/openid-connect/token'
response = requests.post(token_url, data=params, verify=False)
access_token_dict = json.loads(response.text)
access_token = access_token_dict.get('access_token')
# 自行创建，需要有一个初始行 格式为’YYmmdd‘
download_list = 'E:/GCG_storage/storage_code/File_PyCharm/nightLight/data/download_list.txt'
auth = 'Bearer ' + access_token
headers = {'Authorization': auth}
with open(download_list, 'r') as d:
    lines = d.readlines()[-1]
d.close()
start = lines[0:4] + '-' + lines[4:6] + '-' + lines[6:]
end = datetime.datetime.now().strftime("%Y-%m-%d")
datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
while datestart < dateend:
    datestart += datetime.timedelta(days=1)
    data_url = 'https://eogdata.mines.edu/nighttime_light/nightly/rade9d/SVDNB_npp_d' + str(datestart.strftime('%Y%m%d')) + '.rade9d.tif'
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
                    print("\r 文件下载进度：%d%%(%d/%d) - %s" % (now_jd, data_count, content_size, output_file), end="")
            f.close()
            print("\n\033[32m" + os.path.basename(data_url) + '下载完成' + "\033[0m")
            log_record.saveLog(os.path.basename(data_url) + '下载完成')
            with open(download_list, 'a') as d:
                d.write(str(datestart.strftime('%Y%m%d')))
            d.close()
        else:
            print("\n\033[35m" + os.path.basename(data_url) + '下载失败,错误码:' + response.status_code + "\033[0m")
            log_record.saveLog(os.path.basename(data_url) + '下载失败,错误码:' + response.status_code)
    time.sleep(5)
