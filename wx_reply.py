#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import re

import config as conf
import utils.picture_processing as pic_pro
import utils.lunar as lunar
import utils.metro_timetable as metro
import utils.music_platform as music
import utils.weather as weather
import utils.rubbish as rubbish
import utils.maoyan_movie as movie
import utils.love_live as love_live
import utils.train_time as train_time
import utils.cai_hong_pi as cai_hong_pi
import utils.yi_qing as yi_qing


# 好友功能
def auto_accept_friends(msg):
    """自动接受好友"""
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('我已自动接受了您的好友请求')


def auto_reply(msg, chat_type):
    """自动回复"""
    # 关键字回复
    keyword_reply(msg, chat_type)


def handle_system_msg(msg):
    """处理系统消息"""
    raw = msg.raw
    # 4表示消息状态为撤回
    if raw['Status'] == 4 and msg.bot.is_forward_revoke_msg:
        # 转发撤回的消息
        forward_revoke_msg(msg)


def forward_revoke_msg(msg):
    """转发撤回的消息"""
    # 获取被撤回消息的ID
    revoke_msg_id = re.search('<msgid>(.*?)</msgid>', msg.raw['Content']).group(1)
    # bot中有缓存之前的消息，默认200条
    for old_msg_item in msg.bot.messages[::-1]:
        # 查找撤回的那条
        if revoke_msg_id == str(old_msg_item.id):
            # 判断是群消息撤回还是好友消息撤回
            if old_msg_item.member:
                sender_name = '群「{0}」中的「{1}」'.format(old_msg_item.chat.name, old_msg_item.member.name)
            else:
                sender_name = '「{}」'.format(old_msg_item.chat.name)
            # 名片无法转发
            if old_msg_item.type == 'Card':
                sex = '男' if old_msg_item.card.sex == 1 else '女' or '未知'
                msg.bot.master.send('「{0}」撤回了一张名片：\n名称：{1}，性别：{2}'.format(sender_name, old_msg_item.card.name, sex))
            else:
                # 转发被撤回的消息
                old_msg_item.forward(msg.bot.master,
                                     prefix='{}撤回了一条{}：'.format(sender_name, get_msg_chinese_type(old_msg_item.type)))
            return None


def get_msg_chinese_type(msg_type):
    """转中文类型名"""
    if msg_type == 'Text':
        return '文本'
    if msg_type == 'Map':
        return '位置'
    if msg_type == 'Card':
        return '名片'
    if msg_type == 'Note':
        return '提示'
    if msg_type == 'Sharing':
        return '分享'
    if msg_type == 'Picture':
        return '图片'
    if msg_type == 'Recording':
        return '语音'
    if msg_type == 'Attachment':
        return '文件'
    if msg_type == 'Video':
        return '视频'
    if msg_type == 'Friends':
        return '好友请求'
    if msg_type == 'System':
        return '系统'


def keyword_reply(msg, chat_type):
    """关键字回复"""
    text = msg.text.strip().lower()
    if text.startswith('tp'):
        place = text.lstrip('tp').strip()
        if place:
            msg.reply(f"传送到{place}失败")
    elif text.startswith('tq'):
        info = tq_info(text)
        msg.reply(info)
    elif text.startswith('yq'):
        info = yi_qing_info(text)
        msg.reply(info)
    # elif text.startswith('dt'):
    #     info = dt_info(text, 'dt')
    #     return msg.reply(info)
    elif text == '看个黄历':
        info = lunar.get()
        msg.reply(info)
    # elif text.startswith('mc'):
    #     info = mc_info(text, 'mc')
    #     return msg.reply(info)
    elif text.startswith('爱上'):
        if chat_type == 'group':
            user = msg.member
        else:
            user = msg.chat
        pic_path = pic_info(user, text)
        msg.reply_image(pic_path)
    elif text.startswith('lj'):
        info = rubbish_info(text)
        msg.reply(info)
    elif text == '看个票房':
        info = movie.get()
        msg.reply(info)
    elif text == '来段土味情话':
        info = love_live.get()
        msg.reply(info)
    # elif text.startswith('lc'):
    #     info = train_time_info(text)
    #     msg.reply(info)
    elif text == '来段彩虹屁':
        info = cai_hong_pi.get()
        msg.reply(info)
    elif text == '小布':
        info = '根据以下提示回复相应内容：\r\n' \
               '0.实时疫情：yq省份\r\n' \
               '1.查询天气：tq地名\r\n' \
               '2.查看黄历：看个黄历\r\n' \
               '3.垃圾分类：lj垃圾名\r\n' \
               '4.当日票房：看个票房\r\n' \
               '5.土味情话：来段土味情话\r\n' \
               '6.听彩虹屁：来段彩虹屁\r\n' \
               '7.1.头像加CSDN水印：爱上csdn\r\n' \
               '7.2.头像加游侠客水印：爱上游侠客\r\n' \
               '7.3.头像加海贼王水印：爱上海贼王'
        msg.reply(info)


def tq_info(text):
    dm = text.lstrip('tq').strip()
    if len(dm) > 0:
        info = weather.get(dm)
        return info
    return None


def dt_info(text, tag):
    dm = text.lstrip(tag).strip()
    if len(dm) > 0:
        dms = dm.split(' ')
        if len(dms) == 2:
            info = metro.get(dms[0], dms[1])
            return info
        if len(dms) == 1:
            info = metro.get(dms[0], '')
            return info
    return None


def mc_info(text, tag):
    dm = text.lstrip(tag).strip()
    if len(dm) > 0:
        info = music.get(dm)
        return info
    return None


def pic_info(friend, text):
    """回复图片"""
    content = text.lstrip('爱上').strip()
    if len(content) > 0:
        if content == '纳龙':
            water_mark_type = 'nl'
        elif content == '游侠客':
            water_mark_type = 'yxk'
        elif content.lower() == 'csdn':
            water_mark_type = 'csdn'
        elif content.lower() == '海贼王':
            water_mark_type = 'hzw'
        else:
            return None

        pic_rename = friend.user_name[:8] + '.jpg'
        pic_path = os.path.join(conf.pic_temp_path, 'head_pic', pic_rename)
        friend.get_avatar(pic_path)
        pic_with_watermark_path = os.path.join(conf.pic_temp_path, 'head_pic_with_water_mark',
                                               water_mark_type + '_' + pic_rename)
        water_mark_path = os.path.join(conf.pic_temp_path, 'head_water_mark', water_mark_type + '.png')
        pic_pro.create_nike_image(pic_path, water_mark_path, pic_with_watermark_path)
        return pic_with_watermark_path
    return None


def rubbish_info(text):
    lj = text.lstrip('lj').strip()
    if len(lj) > 0:
        info = rubbish.get(lj)
        return info
    return None


def train_time_info(text):
    lc = text.lstrip('lc').strip()
    if len(lc) > 0:
        info = train_time.get(lc)
        return info
    return None


def yi_qing_info(text):
    yq = text.lstrip('yq').strip()
    if len(yq) > 0:
        info = yi_qing.get(yq)
        return info
    return None
