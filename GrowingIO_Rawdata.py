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


threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 1))


class GIO:


    def __init__(self, secret, project, ai, pubkey):

        ''' (secret:私钥; project:项目UID; ai:项目ID; tm:时间戳; pubkey:公钥)'''
        self.secret = secret
        self.project = project
        self.ai = ai
        self.pubkey = pubkey


    def authToken(self):

        ''' 获取auth加密串 '''
        tm = int(round(time.time() * 1000))
        message = ("POST\n/auth/token\nproject=" + str(self.project) + "&ai=" + str(self.ai) + "&tm=" + str(tm)).encode('utf-8')
        signature = hmac.new(bytes(self.secret.encode('utf-8')), bytes(message), digestmod=hashlib.sha256).hexdigest()

        '''  获取API认证 '''
        url_1 = "https://www.growingio.com/auth/token"
        payload = 'project={0}&ai={1}&tm={2}&auth={3}'.format(self.project, self.ai, tm, signature)
        headers_1 = {
            'X-Client-Id': self.pubkey,
            'Content-Type': "text/plain,text/plain"
            }
        response_1 = requests.request("POST", url_1, data=payload, headers=headers_1)
        code = json.loads(response_1.text).get('code')
        return code


    def get_downlinkes(self, code, data_type):

        ''' 获取下载链接 '''
        # threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 16))
        otherStyleTime = threeDayAgo.strftime("%Y%m%d%H%M")        
        url_2 = "https://www.growingio.com/v2/insights/day/" + data_type + "/" + self.ai + "/" + otherStyleTime + ".json"
        querystring = {"expire":"5"}
        headers_2 = {
            'X-Client-Id': self.pubkey,
            'Authorization': code
            }
        response_2 = requests.request("GET", url_2, headers=headers_2, params=querystring)
        json_date = json.loads(response_2.text)
        dw_list = json_date['downloadLinks']
        return dw_list


    def get_data(self, url, data_type, dw_time):

        ''' 下载数据 '''
        path = '/Users/weiche/data/GrowingIO/' + dw_time + "/" + data_type
        filename = url.split('/')[3].split('_')[-1]
        filepath = (path + "/" + filename + ".csv.gz")
        if os.path.exists(path):
            try:
                urllib.request.urlretrieve(url, filename=filepath)
            except Exception as e:
                print("Error occurred when downloading file, error message:")
                print(e)
        else:
            try:
                os.makedirs(path)
                urllib.request.urlretrieve(url, filename=filepath)
            except Exception as e:
                print("Error occurred when downloading file, error message:")
                print(e)

 
if __name__ == '__main__':
    ''' 错误输出没写、代码冗杂待优化 '''
    ''' 输入项目各项值  '''
    info = ["secret:私钥","project:项目UID","ai:项目ID","pubkey:公钥"]

    data_type = ['visit', 'page', 'action', 'action_tag', 'custom_event', 'ads_track_activation', 'ads_track_click', 'pvar', 'evar']
    ''' 下载日期 '''
    dw_time = threeDayAgo.strftime("%Y%m%d")
    f = GIO(info[0], info[1], info[2], info[3])
    code = f.authToken()
    for x in range(len(data_type)):
        dwl = f.get_downlinkes(code, data_type[x])
        for y in dwl:
            f.get_data(y, data_type[x], dw_time)
