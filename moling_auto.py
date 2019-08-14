# coding: utf-8
# 魔灵辅助2.0
import os
import time
import json
import logging
import shutil

from PIL import Image as Images, ImageDraw
import pytesseract

import threading
# import atx
import moling_ui as BaseApp
from tools import *

CUR_PATH = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(message)s")

# 截屏
def pull_screenshot():
    execute_cmd('adb shell screencap -p /sdcard/current.png')
    execute_cmd('adb pull /sdcard/current.png current.png')


# 格式化图片
def binarizing(img, threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


# 保存收货的页面
def save_debug_creenshot():
    execute_cmd('adb shell screencap -p /sdcard/current.png')
    execute_cmd('adb pull /sdcard/current.png current.png')
    shutil.copyfile('current.png', os.path.join(CUR_PATH, 'rune/' + str(time.time()) + '.png'))

class App(BaseApp.Base):
    # 执行状态
    status = False
    # 线程对象
    threadObject = ''
    # 状态文字
    statusTips = '未开始'
    # 选中的脚本
    jiaoben = ''
    # 选中的手机
    mobile = ''
    # 配置脚本
    config = ''
    # 战斗次数
    num = 0
    # 死亡次数
    deathNum = 0
    # 购买能量次数
    buyNum = 0
    # 收取能量次数
    collectNum = 0

    use_crystal = False
    # 是否调试
    debug = False
    lastStatus = ""

    def __init__(self):
        BaseApp.Base.__init__(self, self.start, self.stop)

    # 开始战斗
    def start(self):
        if self.status == True:
            return True
        self.status = True
        self.alertTips.config(text='运行ing')
        self.threadObject = threading.Thread(target=self.__handle, name='LoopThread')
        self.threadObject.start()

    # 暂停
    def stop(self):
        self.status = False
        self.alertTips.config(text='暂停ing')

    # 执行开始
    def __handle(self):
        jiaoben = self.jiaoben.get()
        fileName = 'ta.json'
        if jiaoben == '狗粮':
            fileName = 'gouliang.json'
        elif jiaoben == '地下城':
            fileName = 'dixiacheng.json'
        elif jiaoben == '裂缝':
            fileName = 'liefeng.json'

        with open('./config/' + fileName, 'r', encoding='UTF-8') as f:
            self.config = json.load(f)

        size = git_screen_size()
        with open('./config/mobile/{}.json'.format(size), 'r', encoding='UTF-8') as f:
            self.coordinate = json.load(f)

        while self.status:
            pull_screenshot()
            im = Images.open("./current.png")
            img = im.convert('L')
            img = binarizing(img, 180)
            data = pytesseract.image_to_string(img)
            # self.insertMsg(data)
            data = data.lower()
            self.__handleAction(data, im)
            time.sleep(1)

    # 动作开始
    def __handleAction(self, researchMsg, im):
        print(researchMsg)
        for key in self.config:
            if researchMsg.find(self.config[key]['researchTitle']) != -1:
                msg = self.config[key]['returnMsg']
                if key == 'victory':
                    self.num += 1
                    msg = self.config[key]['returnMsg'].format(self.num)
                    for index, position in enumerate(self.config[key]['coordinate']):
                        if index == 2:
                            save_debug_creenshot()
                        self.__click_position(position)
                        if index != len(self.config[key]['coordinate']) - 1:
                            time.sleep(2)

                elif key == 'death':
                    self.deathNum += 1
                    self.__click_positions(self.config[key]['coordinate'])

                elif key == 'no_energy':
                    self.insertMsg(msg)
                    if self.use_crystal:
                        self.buyNum += 1
                        self.__click_position(self.config[key]['coordinate'][0])
                        self.__click_positions(self.config['shop']['coordinate'])
                        msg = self.config['shop']['returnMsg']
                    else:
                        if self.lastStatus == key:
                            self.use_crystal = True
                            return True

                        self.collectNum += 1
                        self.__click_position(self.config[key]['coordinate'][1])
                        self.__click_positions(self.config['gift']['coordinate'])
                        msg = self.config['gift']['returnMsg']
                elif key == 'prepare':
                    self.__click_positions(self.config[key]['coordinate'])
                    if self.lastStatus != "death" and self.jiaoben.get() == '狗粮':
                        msg = "有魔灵满级了， 需要更换魔灵"
                        self.insertMsg(msg)
                        self.stop()
                        lock_screen()
                        return True
                else:
                    self.__click_positions(self.config[key]['coordinate'])

                # 发送消息提醒
                self.insertMsg(msg)
                countMsg = "战斗{}次\n死亡{}次\n购买能量{}次\n收取能量{}次\n".format(self.num, self.deathNum, self.buyNum, self.collectNum)
                self.countText.config(text=countMsg)
                self.lastStatus = key
                return True

    def open(self):
        BaseApp.Base.mainloop(self)

    def __click_position(self, position):
        if isinstance(position, str):
            self.__click_position(self.coordinate[position])
        else:
            click_position(position[0], position[1])

    def __click_positions(self, positions):
        for index, position in enumerate(positions):
            if type(self.coordinate[position][0]) == list:
                for childen_postion in self.coordinate[position]:
                    self.__click_position(childen_postion)
            else:
                self.__click_position(self.coordinate[position])


app = App()
app.open()
