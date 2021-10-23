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


def wait_time_bar(wait_sec):
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
        wait_time_bar(2)

    # 关闭
    def close(self):
        wait_time_bar(5)
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
        search_result = False

        sleep_time = 5
        logger.debug(f"2.查找喵币入口")
        # source = self.driver.page_source
        # logger.debug(f"首页source:{source}")

        # 如果屏幕小，可能需要滑动一下
        # self.start_x = 26
        # self.start_y = 540
        # self.distance = 200
        #
        # self.driver.swipe(self.start_x, self.start_y, self.start_x, self.start_y - self.distance)
        # wait_time_bar(1)

        wait_time_bar(sleep_time)

        if not config.HOME_XPATH_FLAG:
            logger.debug(f"使用位置来点击入口")
            # 每个手机位置不一样，需要根据bounds（(如：[26,1025][540,1290]）重新设定
            self.driver.tap([(26, 1025), (540, 1290)], 100)
            search_result = True
        else:
            try:
                # 每个手机展示的内容不一样，这个index可能不一样，需要动态修改。
                img_div = '//android.widget.FrameLayout[contains(@index,16)]'

                img_button = self.driver.find_elements_by_xpath(img_div)

                # logger.debug(f"img_button={img_button},img_button_len={len(img_button)}")
                if len(img_button) > 0:
                    logger.debug("开始点击喵币入口")
                    img_button[0].click()
                    search_result = True
                    logger.debug("点击喵币入口完毕")

            except NoSuchElementException as msg:
                img_button = self.driver.find_elements_by_xpath(img_div)
                logger.debug(f"img_button={img_button}")
                if len(img_button) > 0:
                    logger.debug("尝试第二次点击喵币入口")
                    img_button[0].click()
                    search_result = True
                    logger.debug("点击第二次喵币入口完毕")

            except:
                raise Exception("找不到喵币入口")

        if search_result:
            # 加载新页面时间
            wait_time_bar(5)

        return search_result

    #  gzh:testerzhang 做任务列表，还不能做全部，后续再看看。
    def do_task(self):
        # source = self.driver.page_source
        # logger.debug(f"做任务source:{source}")

        # 未做：下单可得大额喵币(0/2)  参与合伙赚喵币(0/1), adidas合成赢大礼(0/3) 关键字 赢
        task_list = config.TASK_LIST

        for task in task_list:

            while True:
                # 先检查是否存在
                diff_task_lists = [
                    '/20)', '/2)', '/3)', '/5)',
                    '逛', '搜'
                ]
                if task not in diff_task_lists:
                    try:
                        logger.debug(f"检查任务:【{task}】是否存在")
                        task_div = f'//*[@text="{task}"]'
                        task_button = self.driver.find_element_by_xpath(task_div)
                    except:
                        logger.warning(f"该任务:【{task}】不执行")
                        # logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                        break

                # 开始做任务
                logger.debug(f"开始真正做任务列表:【{task}】")

                if task in ["领取奖励", "立即领取", "签到", "关闭"]:
                    try:
                        logger.debug(f"开始做任务列表:【{task}】")
                        task_button.click()

                        # todo: 立即领取后有弹窗，未处理。

                    except:
                        logger.warning(f"【{task}】点击异常={traceback.format_exc()}")
                    else:
                        wait_time_bar(8)

                # todo:目前没这个，先保留
                elif task in ["参与组队领红包(0/1)"]:
                    try:
                        logger.debug(f"开始做任务列表:【{task}】")
                        task_button.click()
                    except:
                        logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                    else:
                        wait_time_bar(8)

                        try:
                            logger.debug(f"开始做任务列表:【{task}】")
                            return_div = f'//*[@text="返回我的猫"]'
                            self.driver.find_element_by_xpath(return_div).click()
                        except:
                            logger.debug(f"【{task}】点击异常={traceback.format_exc()}")
                        else:
                            wait_time_bar(8)

                elif task in ["去搜索", "去浏览"]:
                    try:
                        logger.debug(f"开始做任务列表:【{task}】")
                        task_button.click()
                    except:
                        logger.warning(f"【{task}】点击异常={traceback.format_exc()}")
                    else:
                        wait_time_bar(5)

                        # browse_times = 1
                        # browse_max_times = 11
                        # browse_10_times = True
                        # while browse_times <= browse_max_times:
                        #     try:
                        #         logger.debug(f"browse_times={browse_times}")
                        #         # 进入种草喵币城
                        #         browse_div = f'//android.view.View[@text="逛店最多"]'
                        #         browse_button = self.driver.find_element_by_xpath(browse_div)
                        #         browse_button.click()
                        #         wait_time_bar(20)
                        #         logger.debug(f"返回一下")
                        #         self.driver.back()
                        #         wait_time_bar(2)
                        #     except NoSuchElementException:
                        #         logger.warning(f"没有在【种草喵币城】找到【逛店】的按钮")
                        #         browse_10_times = False
                        #         break
                        #     finally:
                        #         browse_times = browse_times + 1
                        #
                        # if not browse_10_times and browse_times == 2:
                        #     wait_time_bar(20)
                        # else:
                        #     wait_time_bar(2)
                        wait_time_bar(20)

                        logger.debug(f"返回一下")
                        self.driver.back()
                        wait_time_bar(5)

                # 先保留
                # elif (')' in task) or ('逛' in task) or ('搜' in task):
                #     try:
                #         wait_time_bar(5)
                #
                #         logger.debug(f"开始做多任务列表:【{task}】")
                #         task_title_div = f'//android.view.View[contains(@text, "{task}")]'
                #         # task_title_div = f'//*[starts-with(@text, {task})]'
                #         task_title_button = self.driver.find_element_by_xpath(task_title_div)
                #         logger.debug(f"task_title_div:{task_title_div}")
                #         logger.debug(f"task_title_button.text:{task_title_button.text}")
                #
                #         if task_title_button.text == '':
                #             logger.warning(f"任务【{task}】退出:没有找到文本内容")
                #             break
                #
                #     except NoSuchElementException as msg:
                #         logger.warning(f"任务【{task}】退出:没找到元素")
                #         break
                #
                #     except:
                #         logger.warning(f"任务【{task}】退出")
                #         logger.warning(f"【{task}】点击异常={traceback.format_exc()}")
                #         break
                #     else:
                #
                #         try:
                #             task_title_content = task_title_button.text
                #             logger.debug(f"task_title_content={task_title_content}")
                #
                #             try:
                #                 # 找当前节点的后面一个节点，拿到文字内容
                #                 brother_browse_div = f'//android.view.View[contains(@text, "{task}")]/following-sibling::android.view.View/android.view.View'
                #                 brother_browse_text = self.driver.find_element_by_xpath(brother_browse_div)
                #                 task_text = brother_browse_text.text
                #                 logger.debug(f"任务副标题:{task_text}")
                #
                #                 # 判断是否任务跳过
                #                 is_continue = self.continue_task(task_text)
                #
                #                 if not is_continue:
                #                     logger.warning(f"满足跳过任务关键字，退出2")
                #                     break
                #
                #             except:
                #                 logger.warning(f"找兄弟节点的文字内容异常=[{traceback.format_exc()}]")
                #                 self.driver.back()
                #
                #             # 判断是否任务跳过
                #             is_continue = self.continue_task(task_title_content)
                #
                #             if not is_continue:
                #                 logger.warning(f"满足跳过任务关键字，退出")
                #                 break
                #
                #             result = parse.parse("{temp}({now_times}/{total_times})", f"{task_title_content}")
                #             now_times = int(result['now_times'])
                #             total_times = int(result['total_times'])
                #             logger.debug(f"now_times={now_times},total_times={total_times}")
                #             if now_times == total_times and total_times > 0:
                #                 break
                #             else:
                #                 while now_times <= total_times:
                #                     task_title_button.click()
                #                     wait_time_bar(5 + 20)
                #
                #                     logger.debug(f"返回一下")
                #                     self.driver.back()
                #                     wait_time_bar(8)
                #
                #                     now_times = now_times + 1
                #         except:
                #             logger.warning(f"【{task}】点击异常={traceback.format_exc()}")
                #             break

                elif '去完成' in task:
                    go_continue = 0

                    try:
                        wait_time_bar(3)
                        logger.debug(f"开始解析任务:【{task}】")
                        task_title_div = f'//android.widget.Button[contains(@text, "{task}")]'
                        task_title_button_lists = self.driver.find_elements_by_xpath(task_title_div)
                        logger.debug(f"task_title_button_lists:{len(task_title_button_lists)}")

                        if len(task_title_button_lists) == 0:
                            logger.warning(f"没找到元素，退出")
                        else:
                            go_continue = 1
                    except NoSuchElementException as msg:
                        logger.warning(f"任务【{task}】退出:没找到元素")
                    except:
                        logger.warning(f"任务【{task}】退出")
                        logger.warning(f"【{task}】点击异常={traceback.format_exc()}")

                    if go_continue == 1:
                        task_title_div = f'{task_title_div}//preceding-sibling::android.view.View/android.view.View'
                        task_title_button_lists = self.driver.find_elements_by_xpath(task_title_div)

                        for i, task_title_button in enumerate(task_title_button_lists):
                            try:
                                logger.debug(f"开始第{i}个按钮")

                                if go_continue == 0:
                                    logger.warning(f"任务【{task}】退出!")
                                    break

                                task_text = task_title_button.text
                                logger.debug(
                                    f"task_text={task_text}")
                                if task_text == '':
                                    logger.warning(f"任务【{task}】退出:没有找到文本内容")
                                    continue

                                # 判断是否任务跳过
                                is_continue = self.continue_task(task_text)

                                if not is_continue:
                                    logger.warning(f"满足跳过任务关键字，退出2")
                                    continue

                            except:
                                logger.warning(f"找兄弟节点的文字内容异常=[{traceback.format_exc()}]")
                                break

                            result = parse.parse("{temp}({now_times}/{total_times})", f"{task_text}")
                            now_times = int(result['now_times'])
                            total_times = int(result['total_times'])
                            logger.debug(f"now_times={now_times},total_times={total_times}")
                            if now_times == total_times and total_times > 0:
                                continue
                            else:
                                while now_times <= total_times:
                                    task_title_button.click()
                                    wait_time_bar(5 + 20)

                                    logger.debug(f"返回一下")
                                    self.driver.back()
                                    wait_time_bar(8)

                                    now_times = now_times + 1

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
            wait_time_bar(5)

            # 最新任务列表签到
            self.do_task()

    #  gzh:testerzhang 喵星人首页按钮处理
    def feed_cat(self, key_name):
        # 加多一层最大喂养次数，防止循环。
        max_times = 10

        if key_name == "喂猫升级":
            logger.debug("欢迎进入【喂猫升级】")

            try:
                logger.debug(f"检查【当前进度】信息")
                progress_div = '//android.view.View[contains(@text, "厨师,进度")]'
                progress_div_button = self.driver.find_element_by_xpath(progress_div)
                # logger.debug(f"获取【当前进度】")
                progress_info = progress_div_button.text
                logger.debug(f"当前进度={progress_info}")
                wait_time_bar(1)
            except NoSuchElementException:
                # logger.warning(f"【升级】弹窗点击异常={traceback.format_exc()}")
                logger.warning(f"获取【当前进度】失败")

            times = 1
            logger.debug(f"开始执行，最大执行次数={max_times}次")

            while True:
                logger.debug(f"开始执行第{times}次")
                if times > max_times:
                    break

                try:
                    wait_time_bar(2)
                    logger.debug("开始点击【喂猫领红包】入口")
                    # 喂猫领红包,每次消耗60000喵币,再升1级领红包
                    feed_div = '//*[contains(@text, "喂猫领红包,")]'
                    self.driver.find_element_by_xpath(feed_div).click()
                except NoSuchElementException:
                    logger.warning(f"无法找到【喂猫领红包】这个元素")
                    # 可能是因为弹窗了，暂时没修复。
                    # logger.debug(f"返回一下")
                    break
                except:
                    logger.warning(f"【喂猫领红包】点击异常={traceback.format_exc()}")
                    break
                else:
                    wait_time_bar(5)

                    upgrade_div = '//*[contains(@text, "元红包待领取")]'
                    try:
                        self.driver.find_element_by_xpath(upgrade_div).click()
                        wait_time_bar(3)
                        continue
                    except NoSuchElementException:
                        # logger.warning(f"点击【升级】弹窗异常={traceback.format_exc()}")
                        pass

                    close_div = '//*[contains(@text, "关闭")]'
                    try:
                        self.driver.find_element_by_xpath(close_div).click()
                        wait_time_bar(3)
                        break
                    except:
                        # logger.warning(f"【关闭】异常={traceback.format_exc()}")
                        pass

                    # receive_div = '//*[contains(@text, "开心收下，喵")]'
                    # try:
                    #     self.driver.find_element_by_xpath(receive_div).click()
                    #     wait_time_bar(5)
                    # except:
                    #     # logger.debug(f"【开心收下】异常={traceback.format_exc()}")
                    #     pass

                times = times + 1

        return

    #  gzh:testerzhang 进入H5页面
    def cat(self):

        # 获取入口
        search_result = self.active_page()
        if not search_result:
            logger.warning("找不到入口，退出")
            return

        logger.debug("3.准备切换H5页面")
        wait_time_bar(3)

        # 下面需要切换view
        source = self.driver.page_source
        # ['NATIVE_APP']
        web_view = self.driver.contexts
        logger.debug(web_view)

        if config.DO_COINS_FLAG:
            # 领喵币
            #self.do_coins('赚喵糖')
            self.do_coins('赚糖领红包')

        # # 点击收取生产的喵币
        # if config.RECEIVE_COINS_FLAG:
        #     self.click_coin()
        #
        # # 开始喂猫
        # self.feed_cat('喂猫升级')


def main():
    tao_bao = TaoBao()
    tao_bao.cat()
    tao_bao.close()
    exit("退出")


if __name__ == '__main__':
    main()
