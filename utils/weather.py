#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import json
import re

import requests
import xml.dom.minidom as xmldom


def get(city_name):
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + translate(city_name)
    response = requests.get(url)
    weather_json = json.loads(response.text)
    info = list()
    if "data" not in weather_json:
        info.append('未查询到{}'.format(city_name))
    else:
        a = weather_json['data']
        info.append('{0} 当前温度：{1}℃'.format(a['city'], a['wendu']))
        info.append('温馨提示：{}'.format(a['ganmao']))
        info.append("-----------------------------")
        for i in range(0, 3):
            info.append('{0} {1}'.format(a["forecast"][i]['date'], a["forecast"][i]['type']))
            feng_li = re.findall(r".*<!\[CDATA\[(.*)\]\]>.*", a["forecast"][i]['fengli'])[0]
            info.append('{0} {1}'.format(a["forecast"][i]['fengxiang'], feng_li))

            high_list = re.findall(r'[+-]?\d+(?:\.\d+)?', a["forecast"][i]['high'])
            high = high_list[0] if len(high_list) > 0 else '未知'
            low_list = re.findall(r'[+-]?\d+(?:\.\d+)?', a["forecast"][i]['low'])
            low = low_list[0] if len(low_list) > 0 else '未知'
            info.append('温度：{0}℃/{1}℃'.format(low, high))
            info.append("-----------------------------")
    return '\r\n'.join(info)


def translate(city_name):
    pattern = "[\u4e00-\u9fa5]+"
    regex = re.compile(pattern)
    results = regex.findall(city_name)
    return ''.join(results)


def get_timing(city_name):
    city_name = translate(city_name)
    url = 'http://ws.webxml.com.cn//WebServices/WeatherWS.asmx/getWeather?theCityCode={}&theUserID='.format(city_name)
    response = requests.get(url)
    dom_obj = xmldom.parseString(response.text)
    # 得到元素对象
    obj_list = dom_obj.documentElement.getElementsByTagName("string")
    info_list = [item.firstChild.data for item in obj_list]
    info = list()
    if len(info_list) == 1:
        info.append('暂查询不到{}'.format(city_name))
    else:
        # 0: 省份 地区/洲 国家名（国外）
        # 1: 查询的天气预报地区名称
        city = info_list[0] if info_list[1] in info_list[0] else '{} {}'.format(info_list[0], info_list[1])
        info.append('{}：'.format(city))
        # 4: 当前实况：气温、风向/风力、湿度
        live_situations = info_list[4][7:].split('；')
        if len(live_situations) == 3:
            info.append('当前{}'.format(live_situations[0]))
            info.append(live_situations[1])
            info.append(live_situations[2])
        # 5: 当前空气质量、紫外线强度
        info.append(info_list[5])
        # 6: 当前天气和生活指数
        info.append(info_list[6].rstrip('\n'))
        info.append("-----------------------------")
        # 7: 当前天气 概况 格式：M月d日 天气概况
        info.append(info_list[7])
        # 8: 当前气温
        info.append('最低/高温：{}'.format(info_list[8]))
        # 9: 当前 风力/风向
        info.append('风力/风向：{}'.format(info_list[9]))
        info.append("-----------------------------")
        # 12: 明天天气 概况 格式：M月d日 天气概况
        info.append(info_list[12])
        # 13: 明天气温
        info.append('最低/高温：{}'.format(info_list[13]))
        # 14: 明天 风力/风向
        info.append('风力/风向：{}'.format(info_list[14]))
        info.append("-----------------------------")
        # 17: 后天天气 概况 格式：M月d日 天气概况
        info.append(info_list[17])
        # 18: 后天气温
        info.append('最低/高温：{}'.format(info_list[18]))
        # 19: 后天 风力/风向
        info.append('风力/风向：{}'.format(info_list[19]))
        info.append("-----------------------------")
    return '\r\n'.join(info)


if __name__ == '__main__':
    result = get('南京')
    print(result)
