#!/usr/bin/python
# coding=utf-8
# 公众号:testerzhang
__author__ = 'testerzhang'

from loguru import logger

logger.add('11.log')

import time
import traceback

from appium import webdriver
from tqdm import tqdm
from parse import *


def wait_time_pbar(wait_sec):
    wait_value = 10 * wait_sec

    for i in tqdm(range(wait_value)):
        time.sleep(0.1)

    logger.debug("")


class TaoBao(object):
    def __init__(self):
        device_name = 'xiaomi-max phone'
        device_port = '4723'

        desired_caps = {
            "platformName": "Android",
            "platformVersion": "7.0",
            # "deviceName": "Android Emulator",
            "deviceName": device_name,
            "appPackage": "com.taobao.taobao",
            "appActivity": "com.taobao.tao.welcome.Welcome",
            # 再次启动不需要再次安装
            "noReset": True,
            # unicode键盘 我们可以输入中文
            "unicodeKeyboard": True,
            # 操作之后还原回原先的输入法
            "resetKeyboard": True
        }

        url = "http://localhost:{}/wd/hub".format(device_port)

        self.driver = webdriver.Remote(url, desired_caps)

        logger.debug("1.打开淘宝，并等待2秒")
        # time.sleep(4)
        wait_time_pbar(2)

    # 关闭
    def close(self):
        wait_time_pbar(5)
        logger.debug("6.关闭淘宝")
        self.driver.quit()

    # 首页查找入口
    def active_page(self):
        logger.debug("2.查找喵币入口")

        wait_time_pbar(2)

        img_div = '//android.widget.FrameLayout[@content-desc="主互动"]/android.widget.ImageView'
        img_button = self.driver.find_elements_by_xpath(img_div)

        if len(img_button) > 0:
            logger.debug("开始点击喵币入口")
            img_button[0].click()
            logger.debug("点击喵币入口完毕")
        else:
            raise Exception("找不到喵币入口")

        wait_time_pbar(10)

    #  gzh:testerzhang 做任务列表，还不能做全部，后续再看看。
    def do_task(self):
        wait_time_pbar(5)

        # 未做：去施肥
        taskList = ['签到', '领取', '去浏览', '去搜索',
                    '去观看', '领取奖励',
                    '参与组队领红包(0/1)', '参与人气比拼赢红包(0/1)',
                    '/20)', '/2)', '/3)', '关闭']

        for task in taskList:

            while True:

                if task != '/20)' and task != '/2)' and task != '/3)':
                    try:
                        logger.debug(f"检查任务:{task}是否存在")
                        task_div = f'//*[@text="{task}"]'
                        task_button = self.driver.find_element_by_xpath(task_div)
                    except Exception:
                        # logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                        break

                logger.debug(f"开始真正做任务列表:{task}")

                if task == "领取奖励" or task == "领取" \
                        or task == "签到" or task == "关闭":
                    try:
                        logger.debug(f"开始做任务列表:{task}")
                        task_button.click()
                    except Exception:
                        logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                        pass
                    else:
                        logger.debug("等待8秒")
                        wait_time_pbar(8)

                elif task == "参与组队领红包(0/1)":
                    try:
                        logger.debug(f"开始做任务列表:{task}")
                        task_button.click()
                    except Exception:
                        logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                        pass
                    else:
                        logger.debug("等待8秒")
                        wait_time_pbar(8)

                        try:
                            logger.debug(f"开始做任务列表:{task}")
                            return_div = f'//*[@text="返回我的猫"]'
                            self.driver.find_element_by_xpath(return_div).click()
                        except Exception:
                            logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                            pass
                        else:
                            logger.debug("等待8秒")
                            wait_time_pbar(8)

                # todo:新任务，还没测试通过
                elif task == '参与人气比拼赢红包(0/1)':
                    try:
                        logger.debug(f"开始做任务列表:{task}")
                        task_button.click()
                    except Exception:
                        logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                        pass
                    else:
                        logger.debug("等待8秒")
                        wait_time_pbar(8)

                        # 关闭弹窗
                        close_div = f'//*[@text="关闭"]'
                        try:
                            self.driver.find_element_by_xpath(close_div).click()
                            wait_time_pbar(5)
                            break
                        except Exception:
                            # logger.debug(f"【关闭】异常={traceback.format_exc()}")
                            pass

                        logger.debug("等待5秒")
                        wait_time_pbar(5)

                        logger.debug("返回")
                        self.driver.back()
                        wait_time_pbar(8)


                elif task == "去搜索" or task == "去浏览":
                    try:
                        logger.debug(f"开始做任务列表:{task}")
                        task_button.click()
                    except Exception:
                        logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                        pass
                    else:
                        logger.debug("等待5秒")
                        wait_time_pbar(5)

                        logger.debug("等待20秒")
                        wait_time_pbar(20)

                        self.driver.back()
                        wait_time_pbar(8)

                elif ')' in task:
                    try:
                        logger.debug("等待5秒")
                        wait_time_pbar(5)

                        logger.debug(f"开始做任务列表:{task}")
                        browse_div = f'//android.view.View[contains(@text, "{task}")]'
                        # browse_div = f'//*[starts-with(@text, {task})]'
                        browse_button = self.driver.find_element_by_xpath(browse_div)
                        logger.debug(f"browse_div:{browse_div}")

                        if browse_button.text == 0:
                            logger.debug("没有找到[去完成]相关元素，退出")
                            break

                        # browse_button.click()
                    except Exception:
                        # logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                        break
                    else:

                        try:
                            content = browse_button.text
                            logger.debug(f"text={content}")

                            result = parse("{temp}({now_times}/{total_times})", f"{content}")
                            now_times = int(result['now_times'])
                            total_times = int(result['total_times'])
                            logger.debug(f"now_times={now_times},total_times={total_times}")
                            if now_times == total_times and total_times > 0:
                                break
                            else:
                                while now_times <= total_times:
                                    browse_button.click()

                                    logger.debug("等待5秒")
                                    wait_time_pbar(5)

                                    logger.debug("等待20秒")
                                    wait_time_pbar(20)

                                    self.driver.back()
                                    wait_time_pbar(8)

                                    now_times = now_times + 1
                        except:
                            # logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                            break
                else:
                    logger.debug(f"其他任务不做:{task}")
                    break

        return

    #  gzh:testerzhang 喵星人首页按钮处理
    def feed_cat(self, key_name):
        # 加多一层最大喂养次数，防止循环。
        max_times = 20

        if key_name == "喂猫升级":
            logger.debug("欢迎进入【喂猫升级】")

            # 亲爱的主人我去淘宝人生玩耍了快来找我回家吧~
            try:
                logger.debug(f"检查小猫是否跑走了")
                find_cat_div = f'//*[@text="亲爱的主人我去淘宝人生玩耍了快来找我回家吧~"]'
                find_cat_button = self.driver.find_element_by_xpath(find_cat_div)
            except Exception:
                # logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                pass
            else:
                try:
                    logger.debug(f"开始点击【找猫猫】")
                    find_cat_button.click()
                except Exception:
                    logger.debug(f"【找猫猫】点击异常={traceback.format_exc()}")
                    return
                else:
                    logger.debug("等待5秒")
                    wait_time_pbar(5)

                    logger.debug("等待20秒")
                    wait_time_pbar(20)

                    # todo: class="android.widget.Image" 找到这个元素退出
                    self.driver.back()
                    wait_time_pbar(8)

            times = 1

            while True:
                if times > max_times:
                    break

                try:
                    logger.debug("开始点击喵币入口")
                    feed_div = '//*[contains(@text, "喂猫升级,")]'
                    self.driver.find_element_by_xpath(feed_div).click()
                except Exception:
                    logger.debug(f"【喂猫升级】点击异常={traceback.format_exc()}")
                    break
                else:
                    wait_time_pbar(5)

                    close_div = '//*[contains(@text, "关闭")]'
                    try:
                        self.driver.find_element_by_xpath(close_div).click()
                        wait_time_pbar(5)
                        break
                    except Exception:
                        # logger.debug(f"【关闭】异常={traceback.format_exc()}")
                        pass

                    receive_div = '//*[contains(@text, "开心收下，喵")]'
                    try:
                        self.driver.find_element_by_xpath(receive_div).click()
                        wait_time_pbar(5)
                    except Exception:
                        # logger.debug(f"【开心收下】异常={traceback.format_exc()}")
                        pass

                times = times + 1

        return

    #  gzh:testerzhang 点击领喵币，然后进入具体的任务列表
    def do_coins(self, button_name):

        try:
            logger.debug(f"开始点击[{button_name}]按钮")
            button_div = f'//*[@text="{button_name}"]'
            self.driver.find_element_by_xpath(button_div).click()
        except Exception:
            logger.debug(f"【{button_name}】点击异常={traceback.format_exc()}")
        else:
            wait_time_pbar(5)

            logger.debug("等待5秒")

            # 最新任务列表签到
            self.do_task()

    #  gzh:testerzhang 进入H5页面
    def cat(self):

        # 获取入口
        self.active_page()

        logger.debug("3.准备切换H5页面")
        wait_time_pbar(5)

        # 下面需要切换view
        source = self.driver.page_source
        # ['NATIVE_APP']
        WebView = self.driver.contexts
        logger.debug(WebView)

        # 赚喵币
        self.do_coins('赚喵币')
        # 开始喂猫
        self.feed_cat('喂猫升级')


def main():
    taobao = TaoBao()
    taobao.cat()
    taobao.close()
    exit("退出")


if __name__ == '__main__':
    main()
