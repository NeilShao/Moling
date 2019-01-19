#coding : utf-8
import logging
import shutil
import time
import json
from action import Action
from img2 import *
from tools import *

jingyan_map = {
    "1": 15120,
    "2": 35822,
    "3": 82182,
    "4": 189750,
    "5": 446647,
    "6": 1005419
}

CUR_PATH = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(message)s")

battle_config = json.load(open("config/config.json", 'r'))

class Moling(object):
    def __init__(self, script):
        self.script = script

        self.win_count = 0
        self.lose_count = 0
        self.current_state = 0

        self.gift_count = 0
        self.shop_count = 0

        self.is_shootscreen = True
        self.enable_shop = False

        self.conf = Action(battle_config[script], logging)

    def play(self):
        execute_cmd('adb shell screencap -p /sdcard/current.png')
        execute_cmd('adb pull /sdcard/current.png current.png')

        image = Image.open("./current.png")

        self.current_state = self.conf.check_state(image)
        if self.current_state is not False:
            if self.current_state == self.conf.STATE_SELECT:
                logging.info("Battle Start...")
                #exit()
                self.conf.click_select()
                time.sleep(battle_config[self.script].get("sleep_time", 0))
            elif self.current_state == self.conf.STATE_SUCCESS:
                logging.info("Battle Success")
                self.conf.click_reward_open()
                # try:
                #     shutil.copyfile('current.png', os.path.join(CUR_PATH, 'rune/' + str(time.time()) + '.png'))
                # except:
                #     pass
            elif self.current_state == self.conf.STATE_SUCCESS_END:
                self.enable_shop = False
                self.win_count += 1
                logging.info("Battle win [{}] times".format(self.win_count))
                self.is_shootscreen = True
                self.conf.click_victory()
                logging.info("Battle Start...")
                time.sleep(battle_config[self.script].get("sleep_time", 0))
            elif self.current_state == self.conf.STATE_FAILED_END:
                self.enable_shop = False
                self.lose_count += 1
                logging.info("Battle fail [{}] times".format(self.lose_count))
                self.conf.click_victory()
                logging.info("Battle Start...")
                time.sleep(battle_config[self.script].get("sleep_time", 0))
            elif self.current_state == self.conf.STATE_FAILED:
                logging.info("Battle failed")
                self.conf.click_not_life()
            elif self.current_state == self.conf.STATE_FIVE_START_RUNE:
                logging.info("Sold five star rune!")
                self.conf.click_sold_five_star_rune()
            elif self.current_state == self.conf.STATE_POWERLESS:
                if self.enable_shop:
                    self.conf.no_power(is_shop=True)
                    self.shop_count += 1
                    logging.info("Charge energy by shop [{}] times".format(self.shop_count))
                else:
                    self.conf.no_power(False)
                    self.gift_count += 1
                    logging.info("Charge energy by gift box [{}] times".format(self.gift_count))

                    self.enable_shop = True
            elif self.current_state == self.conf.STATE_NO_REDWATRT:
                logging.info("No red water, Over!")
                exit(0)
        else:
            logging.debug("... ...")

        time.sleep(1)


    def run(self):
        try:
            while True:
                self.play()
        except KeyboardInterrupt:
                pass

if __name__ == '__main__':
    #G = Moling("gouliang")
    G = Moling("dixiacheng")
    #G = Moling("dragon")
    #G = Moling("tower")
    G.run()

    #os.system('adb sh ell input keyevent 26')

    # os.system('adb pull /sdcard/current.png current.png')
    #
    # image = Image.open("./current.png")
    #
    # conf = config1.Config()
    #
    #
    # print self.conf.is_powerless(image)
    pass
