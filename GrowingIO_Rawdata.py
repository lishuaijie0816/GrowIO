#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import hmac
import time
import requests
import json
import datetime
import os
import urllib


threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=1))


class GrowingIO:

    def __init__(self, secret, project, ai, pubkey):

        ''' (secret:私钥; project:项目UID; ai:项目ID; tm:时间戳; pubkey:公钥) '''
        self.secret = secret
        self.project = project
        self.ai = ai
        self.pubkey = pubkey

    def authToken(self):

        ''' 获取auth加密串 '''
        tm = int(round(time.time() * 1000))
        message = (
            'POST\n/auth/token\nproject={0}&ai={1}&tm={2}'.format(str(self.project), str(self.ai), str(tm))).encode(
            'utf-8')
        signature = hmac.new(bytes(self.secret.encode('utf-8')), bytes(message), digestmod=hashlib.sha256).hexdigest()

        '''  获取API认证 '''
        url = "https://www.growingio.com/auth/token"
        payload = 'project={0}&ai={1}&tm={2}&auth={3}'.format(self.project, self.ai, tm, signature)
        headers = {
            'X-Client-Id': self.pubkey,
            'Content-Type': "text/plain,text/plain"
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        code = json.loads(response.text).get('code')
        return code

    def get_downlinkes(self, code, data_type):

        ''' 获取下载链接 '''
        otherStyleTime = threeDayAgo.strftime("%Y%m%d%H%M")
        url = 'https://www.growingio.com/v2/insights/day/{0}/{1}/{2}.json?expire=60'.format(data_type, self.ai,
                                                                                            otherStyleTime)
        headers = {
            'X-Client-Id': self.pubkey,
            'Authorization': code
            }
        response = requests.request("GET", url, headers=headers)
        json_date = json.loads(response.text)
        return json_date

    def get_data(self, url, data_type, dw_time):

        ''' 下载数据 '''
        path = '/Users/weiche/PycharmProjects/github/GrowIO/' + dw_time + "/" + data_type
        filename = url.split('/')[3].split('_')[-1]
        filepath = (path + "/" + filename + ".csv.gz")
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                urllib.request.urlretrieve(url, filename=filepath)
            else:
                urllib.request.urlretrieve(url, filename=filepath)
        except Exception as e:
            print("Error occurred when downloading file, error message:")
            print(e)

if __name__ == '__main__':
    info = ["secret:私钥", "project:项目UID", "ai:项目ID", "pubkey:公钥"]
    data_type = ['visit', 'page', 'action', 'action_tag', 'custom_event', 'ads_track_activation', 'ads_track_click',
                 'pvar', 'evar', 'vstr']
    dw_time = threeDayAgo.strftime("%Y%m%d")
    f = GrowingIO(info[0], info[1], info[2], info[3])
    code = f.authToken()
    for x in range(len(data_type)):
        dwl = f.get_downlinkes(code, data_type[x])
        if dwl['status'] == 'FINISHED' and not dwl['downloadLinks'] == []:
            for y in dwl['downloadLinks']:
                f.get_data(y, data_type[x], dw_time)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + data_type[x] + ' ' + 'Download successful')