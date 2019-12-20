#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import datetime
import json
import time

import requests


def get_week_day():
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = datetime.datetime.now().weekday()
    return week_day_dict[day]


def request_get(url, params):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    response = requests.get(url=url, params=params, headers=header)
    result = json.loads(response.text, encoding='utf8')
    if result['status'] == 200:
        return result['data']
    return None


def generate_time(format_="%Y-%m-%d"):
    """获取当前日期"""

    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime(format_, local_time)
    return data_head


def get():
    url = 'https://www.sojson.com/open/api/lunar/json.shtml'
    hl = request_get(url=url, params={'date': generate_time()})
    if hl is None:
        return '暂查不到黄历'
    content = list()
    jie_ri = ','.join(hl['festivalList'])
    content.append('今天: {}年{}月{}日 {}'.format(hl['year'], hl['month'], hl['day'], get_week_day()))
    content.append('农历: {}月{}'.format(hl['cnmonth'], hl['cnday']))
    if jie_ri:
        content.append('节日: {}'.format(jie_ri))
    content.append('适宜: {}'.format(hl['suit']))
    content.append('忌讳: {}'.format(hl['taboo']))
    return '\r\n'.join(content)


if __name__ == '__main__':
    result = get()
