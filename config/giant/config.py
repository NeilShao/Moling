# coding : utf-8
from PIL import Image
from img2 import classfiy_histogram_with_split
import random
import os

class Config(object):
    STATE_SELECT = 1
    STATE_SUCCESS = 2
    STATE_REWARD = 3
    STATE_REWARD_OPEN = 4
    STATE_VICTORY = 5
    STATE_POWERLESS = 6
    STATE_FAILED = 7
    STATE_FAILED_OPEN = 8
    STATE_FAILED_OVER = 9

    def __init__(self):
        self.state_select = Image.open("./config/giant/select.png")
        self.state_success = Image.open("./config/giant/success.png")
        self.state_reward = Image.open("./config/giant/reward.png")
        self.state_reward_open1 = Image.open("./config/giant/reward_open.png")
        self.state_reward_open2 = Image.open("./config/giant/reward_open.png")
        self.state_reward_open3 = Image.open("./config/giant/reward_open.png")
        self.state_victory = Image.open("./config/giant/victory.png")
        self.state_powerless = Image.open("./config/giant/powerless.png")
        self.state_failed = Image.open("./config/giant/failed.png")
        self.state_failed_open = Image.open("./config/giant/failed_open.png")
        self.state_failed_over = Image.open("./config/giant/failed_over.png")

    def check_state(self,image1):
        # 选择
        if self.is_select(image1):
            return self.STATE_SELECT
        # 胜利
        if self.is_success(image1):
            return self.STATE_SUCCESS
        # 失败
        if self.is_failed(image1):
            return self.STATE_FAILED
        # 失败结算
        if self.is_failed_open(image1):
            return self.STATE_FAILED_OPEN
        # 失败结束
        if self.is_failed_over(image1):
            return self.STATE_FAILED_OVER
        # 奖品
        if self.is_reward(image1):
            return self.STATE_REWARD
        # 打开奖品
        if self.is_reward_open(image1):
            return self.STATE_REWARD_OPEN
        # 胜利完成
        if self.is_victory(image1):
            return self.STATE_VICTORY
        # 缺少能量
        if self.is_powerless(image1):
            return self.STATE_POWERLESS

        return False

    # 选择
    def is_select(self,image1):
        rate = classfiy_histogram_with_split(image1, self.state_select)
        if rate >= 80:
            print('选择界面')
            return True
        else:
            return False

    # 胜利
    def is_success(self,image1):
        rate = classfiy_histogram_with_split(image1, self.state_success)
        if rate >= 80:
            print('胜利界面')
            return True
        else:
            return False

    # 失败
    def is_failed(self,image1):
        rate = classfiy_histogram_with_split(image1, self.state_failed)
        if rate >= 80:
            print('失败界面')
            return True
        else:
            return False

    # 失败结算
    def is_failed_open(self,image1):
        rate = classfiy_histogram_with_split(image1, self.state_failed_open)
        if rate >= 80:
            print('失败结算界面')
            return True
        else:
            return False

    # 失败结束
    def is_failed_over(self,image1):
        rate = classfiy_histogram_with_split(image1, self.state_failed_over)
        if rate >= 80:
            print('失败结束界面')
            return True
        else:
            return False

    # 奖品
    def is_reward(self,image1):
        rate = classfiy_histogram_with_split(image1, self.state_reward)
        if rate >= 73:
            print('宝箱界面')
            return True
        else:
            return False

    # 打开奖品
    def is_reward_open(self,image1):
        rate1 = classfiy_histogram_with_split(image1, self.state_reward_open1)
        rate2 = classfiy_histogram_with_split(image1, self.state_reward_open2)
        rate3 = classfiy_histogram_with_split(image1, self.state_reward_open3)

        if rate1 >= 70 or rate2 >= 70 or rate3 >= 70:
            print('打开奖品界面')
            return True
        else:
            return False

    # 胜利完成
    def is_victory(self,image1):
        rate = classfiy_histogram_with_split(image1, self.state_victory)
        if rate >= 80:
            print('胜利完成界面')
            return True
        else:
            return False

    # 缺少能量
    def is_powerless(self,image1):
        rate = classfiy_histogram_with_split(image1, self.state_powerless)
        if rate >= 80:
            print('能量耗尽')
            return True
        else:
            return False

    def click_select(self):
        press_h, press_w = random.randint(1936,2376), random.randint(920,1112)
        press_time = 1
        cmd = 'adb shell input swipe {} {} {} {} {}'.format(press_h, press_w, press_h, press_w, press_time)
        os.system(cmd)

    def click_success(self):
        press_h, press_w = random.randint(1936,2376), random.randint(920,1112)
        press_time = 1
        cmd = 'adb shell input swipe {} {} {} {} {}'.format(press_h, press_w, press_h, press_w, press_time)
        os.system(cmd)

    def click_reward(self):
        press_h, press_w = random.randint(1712,1745), random.randint(426,462)
        press_time = 1
        cmd = 'adb shell input swipe {} {} {} {} {}'.format(press_h, press_w, press_h, press_w, press_time)
        os.system(cmd)

    def click_reward_open(self):
        press_h, press_w = random.randint(1720,1730), random.randint(350,370)
        press_time = 1
        cmd = 'adb shell input swipe {} {} {} {} {}'.format(press_h, press_w, press_h, press_w, press_time)
        os.system(cmd)

        press_w = random.randint(440,460)
        cmd = 'adb shell input swipe {} {} {} {} {}'.format(press_h, press_w, press_h, press_w, press_time)
        os.system(cmd)

    def click_victory(self):
        press_h, press_w = random.randint(450,1190), random.randint(710,860)
        press_time = 1
        cmd = 'adb shell input swipe {} {} {} {} {}'.format(press_h, press_w, press_h, press_w, press_time)
        os.system(cmd)

    def click_failed(self):
        press_h, press_w = random.randint(1640,1660), random.randint(940,960)
        press_time = 1
        cmd = 'adb shell input swipe {} {} {} {} {}'.format(press_h, press_w, press_h, press_w, press_time)
        os.system(cmd)
