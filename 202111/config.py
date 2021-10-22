#!/usr/bin/python
# coding=utf-8

__author__ = 'testerzhang'

MIAO_LOG = "logs/miao.log"

DEVICE_NAME = 'xiaomi'
DEVICE_PORT = '4723'

DESIRED_CAPS = {
    "platformName": "Android",
    "platformVersion": "11",
    # "deviceName": "Android Emulator",
    "deviceName": DEVICE_NAME,
    "appPackage": "com.taobao.taobao",
    "appActivity": "com.taobao.tao.welcome.Welcome",
    # 再次启动不需要再次安装
    "noReset": True,
    # unicode键盘 我们可以输入中文
    # "unicodeKeyboard": True,
    # 操作之后还原回原先的输入法
    # "resetKeyboard": True
}

# 首页是否使用XPATH找入口
HOME_XPATH_FLAG = True

# 执行任务:赚喵糖
DO_COINS_FLAG = True

# 执行任务:收取生产的喵币
# RECEIVE_COINS_FLAG = True

# 任务列表
TASK_LIST = [
    '立即领取',
    '去浏览',
    '去完成',
    '关闭'
]

# 过滤的任务列表
SKIP_LIST = [
    '选择我方格子扔喵糖(0/1)',
    '蚂蚁森林收能量或浇水(0/1)',
    '去农场施肥一次(0/1)',
    '完成跑酷玩法小互动(0/1)',
    '浏览天天领现金(0/1)',
    '完成糖果飞行小互动(0/1)',
    '小互动',
    # 这个还没处理，暂时跳过
    '每日签到领喵糖(0/1)',
]
