#!/usr/bin/python
# coding=utf-8
# 公众号:testerzhang
__author__ = 'testerzhang'

import time
import traceback

from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import parse
from loguru import logger

import config

logger.add(config.MIAO_LOG)


def wait_time_pbar(wait_sec):
    logger.debug(f"等待{wait_sec}秒")
    wait_value = 10 * wait_sec

    for i in tqdm(range(wait_value)):
        time.sleep(0.1)

    logger.debug("")


class TaoBao(object):
    def __init__(self):
        device_port = config.DEVICE_PORT

        desired_caps = config.DESIRED_CAPS

        self.skip_list = config.SKIP_LIST

        url = "http://localhost:{}/wd/hub".format(device_port)

        self.driver = webdriver.Remote(url, desired_caps)

        logger.debug("1.打开淘宝")
        wait_time_pbar(2)

    # 关闭
    def close(self):
        wait_time_pbar(5)
        logger.debug("6.关闭淘宝")
        self.driver.quit()

    # 判断某些任务是不是直接跳过
    def continue_task(self, content):
        is_continue = True
        for skip in self.skip_list:
            if skip in content:
                logger.warning(f"任务=[{content}]暂时不做")
                is_continue = False
                break

        return is_continue

    # 首页查找入口
    def active_page(self):
        sleep_time = 2
        logger.debug(f"2.查找喵币入口")

        # 如果屏幕小，可能需要滑动一下
        # self.start_x = 26
        # self.start_y = 540
        # self.distance = 200
        #
        # self.driver.swipe(self.start_x, self.start_y, self.start_x, self.start_y - self.distance)
        # wait_time_pbar(1)

        wait_time_pbar(sleep_time)

        try:
            img_div = '//android.widget.FrameLayout[contains(@index,15)]'

            img_button = self.driver.find_elements_by_xpath(img_div)
            logger.debug(f"img_button={img_button},img_button_len={len(img_button)}")
            if len(img_button) > 0:
                logger.debug("开始点击喵币入口")
                img_button[0].click()
                logger.debug("点击喵币入口完毕")

        except NoSuchElementException as msg:
            img_button = self.driver.find_elements_by_xpath(img_div)
            logger.debug(f"img_button={img_button}")
            if len(img_button) > 0:
                logger.debug("尝试第二次点击喵币入口")
                img_button[0].click()
                logger.debug("点击第二次喵币入口完毕")
        except:
            raise Exception("找不到喵币入口")

        # 加载新页面时间
        wait_time_pbar(5)

    #  gzh:testerzhang 做任务列表，还不能做全部，后续再看看。
    def do_task(self):
        wait_time_pbar(4)

        # 未做：下单可得大额喵币(0/2)  参与合伙赚喵币(0/1), adidas合成赢大礼(0/3) 关键字 赢
        task_list = config.TASK_LIST

        for task in task_list:

            while True:
                # 先检查是否存在
                if task != '/20)' and task != '/2)' \
                        and task != '/3)' and task != '/5)' \
                        and task != '逛' and task != '搜':
                    try:
                        logger.debug(f"检查任务:【{task}】是否存在")
                        task_div = f'//*[@text="{task}"]'
                        task_button = self.driver.find_element_by_xpath(task_div)
                    except:
                        logger.warning(f"该任务:【{task}】不执行")
                        # logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                        break

                logger.debug(f"开始真正做任务列表:【{task}】")

                if task == "领取奖励" or task == "领取" \
                        or task == "签到" or task == "关闭":
                    try:
                        logger.debug(f"开始做任务列表:【{task}】")
                        task_button.click()
                    except:
                        logger.warning(f"【{task}】点击异常={traceback.format_exc()}")
                    else:
                        wait_time_pbar(8)

                # todo:目前没这个，先保留
                elif task == "参与组队领红包(0/1)":
                    try:
                        logger.debug(f"开始做任务列表:【{task}】")
                        task_button.click()
                    except:
                        logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                    else:
                        wait_time_pbar(8)

                        try:
                            logger.debug(f"开始做任务列表:【{task}】")
                            return_div = f'//*[@text="返回我的猫"]'
                            self.driver.find_element_by_xpath(return_div).click()
                        except:
                            logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                        else:
                            wait_time_pbar(8)

                elif task == "去搜索" or task == "去浏览":
                    try:
                        logger.debug(f"开始做任务列表:【{task}】")
                        task_button.click()
                    except:
                        logger.warning(f"【{task}】点击异常={traceback.format_exc()}")
                    else:
                        wait_time_pbar(5 + 20)

                        logger.debug(f"返回一下")
                        self.driver.back()
                        wait_time_pbar(8)

                elif (')' in task) or ('逛' in task) or ('搜' in task):
                    try:
                        wait_time_pbar(5)

                        logger.debug(f"开始做多任务列表:【{task}】")
                        task_title_div = f'//android.view.View[contains(@text, "{task}")]'
                        # task_title_div = f'//*[starts-with(@text, {task})]'
                        task_title_button = self.driver.find_element_by_xpath(task_title_div)
                        logger.debug(f"task_title_div:{task_title_div}")
                        logger.debug(f"task_title_button.text:{task_title_button.text}")

                        if task_title_button.text == '':
                            logger.warning(f"任务【{task}】退出:没有找到文本内容")
                            break

                    except NoSuchElementException as msg:
                        logger.warning(f"任务【{task}】退出:没找到元素")
                        break

                    except:
                        logger.warning(f"任务【{task}】退出")
                        logger.warning(f"【{task}】点击异常={traceback.format_exc()}")
                        break
                    else:

                        try:
                            task_title_content = task_title_button.text
                            logger.debug(f"task_title_content={task_title_content}")

                            try:
                                # 找当前节点的后面一个节点，拿到文字内容
                                brother_browse_div = f'//android.view.View[contains(@text, "{task}")]/following-sibling::android.view.View/android.view.View'
                                brother_browse_text = self.driver.find_element_by_xpath(brother_browse_div)
                                task_text = brother_browse_text.text
                                logger.debug(f"任务副标题:{task_text}")

                                # 判断是否任务跳过
                                is_continue = self.continue_task(task_text)

                                if not is_continue:
                                    logger.warning(f"满足跳过任务关键字，退出2")
                                    break

                            except:
                                logger.warning(f"找兄弟节点的文字内容异常=[{traceback.format_exc()}]")

                            # 判断是否任务跳过
                            is_continue = self.continue_task(task_title_content)

                            if not is_continue:
                                logger.warning(f"满足跳过任务关键字，退出")
                                break

                            result = parse.parse("{temp}({now_times}/{total_times})", f"{task_title_content}")
                            now_times = int(result['now_times'])
                            total_times = int(result['total_times'])
                            logger.debug(f"now_times={now_times},total_times={total_times}")
                            if now_times == total_times and total_times > 0:
                                break
                            else:
                                while now_times <= total_times:
                                    task_title_button.click()
                                    wait_time_pbar(5 + 20)

                                    logger.debug(f"返回一下")
                                    self.driver.back()
                                    wait_time_pbar(8)

                                    now_times = now_times + 1
                        except:
                            logger.warning(f"【{task}】点击异常={traceback.format_exc()}")
                            break
                else:
                    logger.warning(f"其他任务不做:【{task}】")
                    break

        return

    #  gzh:testerzhang 点击生产出来的喵币
    def click_coin(self):
        try:
            logger.debug("开始点击【自生产猫币】图标")
            feed_div = '//*[contains(@text, "自生产猫币")]'
            feed_button = self.driver.find_element_by_xpath(feed_div)
            logger.debug(f"feed_button.text=[{feed_button.text}]")
            feed_button.click()
        except:
            logger.warning(f"【自生产猫币】点击异常={traceback.format_exc()}")

        return

    #  gzh:testerzhang 点击领喵币，然后进入具体的任务列表
    def do_coins(self, button_name):

        try:
            logger.debug(f"开始点击[{button_name}]按钮")
            button_div = f'//*[@text="{button_name}"]'
            self.driver.find_element_by_xpath(button_div).click()
        except:
            logger.warning(f"【{button_name}】点击异常={traceback.format_exc()}")
        else:
            wait_time_pbar(5)

            # 最新任务列表签到
            self.do_task()

    #  gzh:testerzhang 喵星人首页按钮处理
    def feed_cat(self, key_name):
        # 加多一层最大喂养次数，防止循环。
        max_times = 3

        if key_name == "喂猫升级":
            logger.debug("欢迎进入【喂猫升级】")

            # 亲爱的主人我去淘宝人生玩耍了快来找我回家吧~
            # try:
            #     logger.debug(f"检查小猫是否跑走了")
            #     find_cat_div = f'//*[@text="亲爱的主人我去淘宝人生玩耍了快来找我回家吧~"]'
            #     find_cat_button = self.driver.find_element_by_xpath(find_cat_div)
            # except:
            #     # logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
            #     pass
            # else:
            #     try:
            #         logger.debug(f"开始点击【找猫猫】")
            #         find_cat_button.click()
            #     except:
            #         logger.warning(f"【找猫猫】点击异常={traceback.format_exc()}")
            #         return
            #     else:
            #         wait_time_pbar(5)
            #
            #         # todo: class="android.widget.Image" 找到这个元素退出
            #         self.driver.back()
            #         wait_time_pbar(8)

            times = 1
            logger.debug(f"开始执行，最大执行次数={max_times}次")

            while True:
                logger.debug(f"开始执行第{times}次")
                if times > max_times:
                    break

                try:
                    logger.debug("开始点击【喂猫领红包】入口")
                    # 喂猫领红包,每次消耗60000喵币,再升1级领红包
                    feed_div = '//*[contains(@text, "喂猫领红包,")]'
                    self.driver.find_element_by_xpath(feed_div).click()
                except NoSuchElementException as msg:
                    logger.warning(f"【喂猫领红包】点击无法找到元素")
                    break
                except:
                    logger.warning(f"【喂猫领红包】点击异常={traceback.format_exc()}")
                    break
                else:
                    wait_time_pbar(5)

                    close_div = '//*[contains(@text, "关闭")]'
                    try:
                        self.driver.find_element_by_xpath(close_div).click()
                        wait_time_pbar(5)
                        break
                    except:
                        # logger.debug(f"【关闭】异常={traceback.format_exc()}")
                        pass

                    receive_div = '//*[contains(@text, "开心收下，喵")]'
                    try:
                        self.driver.find_element_by_xpath(receive_div).click()
                        wait_time_pbar(5)
                    except:
                        # logger.debug(f"【开心收下】异常={traceback.format_exc()}")
                        pass

                times = times + 1

        return

    #  gzh:testerzhang 进入H5页面
    def cat(self):

        # 获取入口
        self.active_page()

        logger.debug("3.准备切换H5页面")
        wait_time_pbar(5)

        # 下面需要切换view
        source = self.driver.page_source
        # ['NATIVE_APP']
        web_view = self.driver.contexts
        logger.debug(web_view)

        if config.DO_COINS_FLAG:
            # 领喵币
            self.do_coins('领喵币')

        # 点击收取生产的喵币
        if config.RECEIVE_COINS_FLAG:
            self.click_coin()

        # 开始喂猫
        self.feed_cat('喂猫升级')


def main():
    taobao = TaoBao()
    taobao.cat()
    taobao.close()
    exit("退出")


if __name__ == '__main__':
    main()
