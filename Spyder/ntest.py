import requests
import json
import os
from contextlib import closing
requests.packages.urllib3.disable_warnings()
# Retrieve access token
params = {    
    'client_id': 'eogdata_oidc',
    'client_secret': '2677ad81-521b-4869-8480-6d05b9e57d48',
    'username': 'cg3026@126.com',
    'password': 'gcg0624123',
    'grant_type': 'password'
}
token_url = 'https://eogauth.mines.edu/auth/realms/master/protocol/openid-connect/token'
response = requests.post(token_url, data=params)
access_token_dict = json.loads(response.text)
access_token = access_token_dict.get('access_token')
print(access_token)
data_url = 'https://eogdata.mines.edu/nighttime_light/nightly/rade9d/SVDNB_npp_d20211115.rade9d.tif'
auth = 'Bearer ' + access_token
headers = {'Authorization': auth}
output_file = os.path.basename(data_url)
with closing(requests.get(data_url, headers=headers, stream=True, verify=False)) as response:
    chunk_size = 1024  # 单次请求最大值
    content_size = int(response.headers['content-length'])
    data_count = 0
    with open(output_file, 'wb') as f:
        for data in response.iter_content(chunk_size=chunk_size):
            f.write(data)
            content_size = int(response.headers['content-length'])
            data_count = data_count + len(data)
            now_jd = (data_count / content_size) * 100
            print("\r 文件下载进度：%d%%(%d/%d) - %s" % (now_jd, data_count, content_size, output_file), end=" ")
