#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
import json


def get_ncov_data() -> dict:
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    data = requests.get(url).json()['data']
    result = json.loads(data)
    return result


def get_daily_data() -> list:
    return get_ncov_data()['chinaDayList']


def get(province_name) -> str:
    all = get_ncov_data()
    china_total = all['chinaTotal']
    china_today = all['chinaAdd']
    info = list()
    info.append(f"截至{all['lastUpdateTime']}")
    info.append(f"全国：")
    info.append(f" 确诊{china_total['confirm']}[+{china_today['confirm']}]")
    info.append(f" 疑似{china_total['suspect']}[+{china_today['suspect']}]")
    info.append(f" 治愈{china_total['heal']}[+{china_today['heal']}]")
    info.append(f" 死亡{china_total['dead']}[+{china_today['dead']}]")
    info.append("-----------------------------")

    # 第一层：国家 get China data
    china = all['areaTree'][0]
    # 第二层：省
    provinces = [item for item in china['children'] if province_name.replace('省', '') in item['name']]
    if provinces:
        prov = provinces[0]
        info.append(format_data(prov['name'], prov['total'], prov['today'], '\r\n '))
        info.append("-----------------------------")
        # 第三层：市
        for city in prov['children']:
            info.append(format_data(city['name'], city['total'], city['today']))

    info.append("-----------------------------")
    info.append('+:新增人数,已包含在总人数中.')
    info.append('这些都不是数字,而是真正的人.')
    info.append('注意保护好自己，爱你们.')
    info.append('中国加油！武汉加油！')
    return '\r\n'.join(info)


def format_data(name, total, today, spe_str=' '):
    message_list = list()
    message = f"确诊{total['confirm']}"
    if today['confirm']:
        message += f"[+{today['confirm']}]"
    message_list.append(message)

    # message = f"疑似{total['suspect']}"
    # if today['suspect']:
    #     message += f"[+{today['suspect']}]"
    # message_list.append(message)

    message = f"治愈{total['heal']}"
    if today['heal']:
        message += f"[+{today['heal']}]"
    message_list.append(message)

    message = f"死亡{total['dead']}"
    if today['dead']:
        message += f"[+{today['dead']}]"
    message_list.append(message)

    return f"{name}:\r\n {spe_str.join(message_list)}"


if __name__ == '__main__':
    result = get('江苏省')
    print(result)