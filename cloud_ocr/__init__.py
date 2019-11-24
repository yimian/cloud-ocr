# -*- coding: utf-8 -*-

# @File    : __init__.py
# @Date    : 2019-11-20
# @Author  : skym

import requests
import time
import hashlib
import base64
import json
from functools import wraps
from datetime import datetime, timedelta

from aip import AipOcr


class Throttle(object):
    """
    Decorator that prevents a function from being called more than once every
    time period.
    To create a function that cannot be called more than once a minute:
        @throttle(minutes=1)
        def my_fun():
            pass
    """

    def __init__(self, seconds=1, minutes=0, hours=0):
        self.throttle_period = timedelta(
            seconds=seconds, minutes=minutes, hours=hours
        )
        self.time_of_last_call = datetime.min

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            now = datetime.now()
            time_since_last_call = now - self.time_of_last_call

            if time_since_last_call > self.throttle_period:
                self.time_of_last_call = now
                return fn(*args, **kwargs)
            else:
                time.sleep(max((self.throttle_period - time_since_last_call).total_seconds(), 0.1))
                self.time_of_last_call = datetime.now()
                return fn(*args, **kwargs)

        return wrapper


class BaiduOcr:
    def __init__(self, app_id, app_key, secret_key, direction=True, language='CHN_ENG'):
        self.client = AipOcr(app_id, app_key, secret_key)
        self.url_map = {
            'general': self.client.general,
            'basicGeneral': self.client.basicGeneral,
            'basicAccurate': self.client.basicAccurate,
            'accurate': self.client.accurate,
            'number': self.client.numbers
        }
        self.options = {
            'detect_direction': "true" if direction else "false",
            'language': language
        }

    def analyze(self, img_path, url='general'):
        img = get_file_content(img_path)
        return self.url_map.get(url, 'general')(img, self.options)


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


class XunFeiOcr:
    def __init__(self, app_id, app_key, location=True):
        self.url = 'http://webapi.xfyun.cn/v1/service/v1/ocr/general'
        self.app_id = app_id
        self.app_key = app_key

        self.header = self._get_header(location)

    def _get_header(self, location=True):
        #  当前时间戳
        cur_time = str(int(time.time()))
        #  支持语言类型和是否开启位置定位(默认否)
        param = {"language": "cn|en", "location": "true" if location else "false"}
        param = json.dumps(param)
        param_base64 = base64.b64encode(param.encode('utf-8'))

        m2 = hashlib.md5()
        str1 = self.app_key + cur_time + str(param_base64, 'utf-8')
        m2.update(str1.encode('utf-8'))
        check_sum = m2.hexdigest()
        # 组装http请求头
        header = {
            'X-CurTime': cur_time,
            'X-Param': param_base64,
            'X-Appid': self.app_id,
            'X-CheckSum': check_sum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    # 上传文件并进行base64位编码
    def analyze(self, image_path):
        image = get_file_content(image_path)
        f1_base64 = str(base64.b64encode(image), 'utf-8')
        data = {
            'image': f1_base64
        }
        r = requests.post(self.url, data=data, headers=self.header)
        result = r.json()

        return result
