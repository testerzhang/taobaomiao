#!/usr/bin/python
# coding=utf-8

__author__ = 'testerzhang'

MIAO_LOG = "logs/miao.log"

DEVICE_NAME = 'xiaomi'
DEVICE_PORT = '4723'

DESIRED_CAPS = {
    "platformName": "Android",
    "platformVersion": "10",
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

# 执行任务:领喵币
DO_COINS_FLAG = True

# 执行任务:收取生产的喵币
RECEIVE_COINS_FLAG = True

# 任务列表
TASK_LIST = [
    '签到', '领取', '去浏览',
    '去搜索', '去观看', '领取奖励',
    '逛',
    '搜',
    # '参与组队领红包(0/1)',
    # '参与人气比拼赢红包(0/1)',
    '/4)', '/20)', '/2)', '/3)', '/5)',
    '关闭'
]

# 过滤的任务列表
SKIP_LIST = [
    '下单可得大额喵币(0/2)',
    '参与合伙赚喵币(0/1)',
    '赢',
    '天猫会员店9.9元一箱奶(0/1)',
    '邀',
    '小互动'
]
