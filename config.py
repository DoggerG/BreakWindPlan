#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""项目配置"""
import os

# 获取文件的当前路径（绝对路径）
cur_path = os.path.dirname(os.path.realpath(__file__))
# 获取QR.png的路径
qr_path = os.path.join(cur_path, 'QR.png')
# 获取临时图片文件夹的路径
pic_temp_path = os.path.join(cur_path, 'pic_temp')

# 机器人主人, 使用备注名更安全，只允许一个，可远程控制机器人，如果不设置(空)则将文件助手设置为管理员，但不具备远程控制功能
bot_master_name = 'DoggerX'

# 好友自动回复
is_friend_auto_reply = True
# 此项表示群中是否回复
is_group_reply = True
# True:@本人才回復，上一项开启后此项才生效
is_group_at_reply = False
# 开启防撤回模式
is_forward_revoke_msg = True

# 监听某些好友群聊，如老板
is_listen_friend = False
# 在这些群里监听好友说的话，匹配模式：包含“唯一集团工作群”的群
listen_friend_groups = ''
# 需要监听的人名称，使用备注名更安全，允许多个用|分隔，如：主管|项目经理|产品狗
listen_friend_names = ''

# 打开转发模式，主人发送给机器人的消息都将转发至forward_groups群
is_forward_mode = False
# 需要将消息转发的群，匹配模式同上
forward_groups = '游侠客全球领队颜值担当'

# 群分享监控
is_listen_sharing = True
# 监控群分享，匹配模式同上
listen_sharing_groups = '游侠客全球领队颜值担当' \
                       '|冲鸭!每天学点Python-56' \
                       '|冲鸭!每天学点Python-211' \
                       '|冲鸭!每天学点Python-216' \
                       '|冲鸭!每天学点Python-221' \
                       '|CSDN-Python技术栈-28V' \
                       '|CSDN-Python技术栈-27V' \
                       '|CSDN-Python技术栈-26V'

# 定时提醒：每天几点几分
timing_hour = 7
timing_minute = 30
timing_remind_groups = '游侠客南京站领队群' \
                       '|长营社区党建群' \
                       '|冲鸭!每天学点Python-56' \
                       '|冲鸭!每天学点Python-211' \
                       '|冲鸭!每天学点Python-216' \
                       '|冲鸭!每天学点Python-221' \
                       '|CSDN-Python技术栈-28V' \
                       '|CSDN-Python技术栈-27V' \
                       '|CSDN-Python技术栈-26V'
timing_location = '南京'