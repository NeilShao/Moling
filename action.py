# coding : utf-8
from PIL import Image
from img2 import classfiy_histogram_with_split
from tools import click_position, lock_screen
import random
import time
import os

root_path = os.path.dirname(__file__) + '/config/'

class Action(object):
    STATE_SELECT = 1
    STATE_SUCCESS = 2

    STATE_POWERLESS = 4
    STATE_FAILED = 5

    STATE_SUCCESS_END = 6
    STATE_FAILED_END = 7

    STATE_NO_REDWATRT = 8
    STATE_FIVE_START_RUNE = 8



    def __init__(self, config, logging):
        self.is_debug = False
        self.logging = logging
        self.script = config.get("name")

        self.state_select = Image.open(os.path.join(root_path, config["select_image"]))
        self.state_success = Image.open(os.path.join(root_path, config["success_image"]))
        self.state_end = Image.open(os.path.join(root_path, config["victory_image"]))
        self.state_powerless = Image.open(os.path.join(root_path, config["powerless_image"]))
        self.state_failed = Image.open(os.path.join(root_path, config["failed_image"]))
        self.state_no_redwater = Image.open(os.path.join(root_path, config["no_redwater_image"]))
        self.state_resurrection = Image.open(os.path.join(root_path, config["resurrection_image"]))
        self.state_sold_five_star_rune_image = Image.open(os.path.join(root_path, config["sold_five_star_rune_image"]))

        self.powerless_box = tuple(config["powerless_box"])
        self.no_redwater_box = tuple(config["no_redwater_box"])
        self.select_box = tuple(config["select_box"])
        self.success_box = tuple(config["success_box"])
        self.failed_box = tuple(config["failed_box"])
        self.end_box = tuple(config["end_box"])
        self.resurrection_box = tuple(config["resurrection_box"])
        self.five_start_sold_box = tuple(config["five_start_sold_box"])

        self.select_points = config["select_points"]
        self.failed_points = config["failed_points"]
        self.end_points = config["end_points"]

        self.reward_sold_points = config["reward_sold_points"]
        self.reward_keep_points = config["reward_keep_points"]
        self.reward_treasure_points = config["reward_treasure_points"]

        self.is_choose_friend = config["is_choose_friend"]
        self.choose_friend_point = config["choose_friend_point"]

        self.is_sold = config["reward_is_sold"]

        self.is_get_energy_from_gift = config["is_get_energy_from_gift"]
        self.is_get_energy_from_shop = config["is_get_energy_from_shop"]

        self.gift_box_point = config["gift_box_point"]
        self.gift_first_energy = config["gift_first_energy"]
        self.gift_close_point = config["gift_close_point"]

        self.shop_point = config["shop_point"]
        self.shop_energy_point = config["shop_energy_point"]
        self.shop_purchase = config["shop_purchase"]
        self.shop_close_point = config["shop_close_point"]

        self.fix_start_sold_point = config["fix_start_sold_point"]


    def check_state(self,image1):
        # no power
        if self.is_powerless(image1):
            return self.STATE_POWERLESS

        # no red water
        if self.is_no_water(image1):
            return self.STATE_NO_REDWATRT

        # sold five star rune
        if self.sold_five_star_rune(image1):
            return self.STATE_NO_REDWATRT

        # select
        if self.is_select(image1):
            # for
            if self.script == "gouliang" and not self.is_choose_friend:
                #lock_screen()
                exit()
            return self.STATE_SELECT

        # success
        if self.is_success(image1):
            # finish
            if self.is_end(image1):
                return self.STATE_SUCCESS_END
            # not finish
            else:
                return self.STATE_SUCCESS

        # failed
        if self.is_failed(image1):
            # finish
            if self.is_end(image1):
                return self.STATE_FAILED_END
            # not finish
            else:
                return self.STATE_FAILED

        return False

    # select
    def is_select(self, image1):
        image = image1.crop(self.select_box)
        if self.is_debug:
            image.save("select.png")
        rate = classfiy_histogram_with_split(image, self.state_select)
        self.logging.debug("{} rate is {}".format("select", rate))
        if rate >= 90:
            return True
        else:
            return False

    # select
    def is_no_water(self, image1):
        image = image1.crop(self.no_redwater_box)
        if self.is_debug:
            image.save("no_redwater.png")
        rate = classfiy_histogram_with_split(image, self.state_no_redwater)
        self.logging.debug("{} rate is {}".format("no_redwater", rate))
        if rate >= 90:
            return True
        else:
            return False

    def sold_five_star_rune(self, image1):
        image = image1.crop(self.five_start_sold_box)
        if self.is_debug:
            image.save("sold_five_star_rune.png")
        rate = classfiy_histogram_with_split(image, self.state_sold_five_star_rune_image)
        self.logging.debug("{} rate is {}".format("sold_five_star_rune", rate))
        if rate >= 90:
            return True
        else:
            return False

    # success
    def is_success(self, image1):
        image = image1.crop(self.success_box)
        if self.is_debug:
            image.save("success.png")
        rate = classfiy_histogram_with_split(image, self.state_success)
        self.logging.debug("{} rate is {}".format("success", rate))
        if rate >= 80:
            return True
        else:
            return False

    # failed
    def is_failed(self, image1):
        image_re = image1.crop(self.resurrection_box)
        if self.is_debug:
            image_re.save("resurrection.png")
        rate = classfiy_histogram_with_split(image_re, self.state_resurrection)
        self.logging.debug("{} rate is {}".format("resurrection", rate))
        if rate >= 80:
            return True

        image = image1.crop(self.failed_box)
        if self.is_debug:
            image.save("failed.png")
        rate = classfiy_histogram_with_split(image, self.state_failed)
        self.logging.debug("{} rate is {}".format("fail", rate))
        if rate >= 85:
            return True
        else:
            return False

    # end
    def is_end(self,image1):
        image = image1.crop(self.end_box)
        if self.is_debug:
            image.save("end.png")
        rate = classfiy_histogram_with_split(image, self.state_end)
        self.logging.debug("{} rate is {}".format("end", rate))
        if rate >= 60:
            return True
        else:
            return False

    # no power
    def is_powerless(self,image1):
        image = image1.crop(self.powerless_box)
        if self.is_debug:
            image.save("powerless.png")
        rate = classfiy_histogram_with_split(image, self.state_powerless)
        self.logging.debug("{} rate is {}".format("no power", rate))
        if rate >= 80:
            return True
        else:
            return False

    def click_select(self):
        if self.is_choose_friend:
            click_position(self.choose_friend_point[0][0], self.choose_friend_point[0][1])

        for point in self.select_points:
            click_position(point[0], point[1])
            if len(self.select_points) != 1:
                time.sleep(1)

    def click_sold_five_star_rune(self):
        for point in self.fix_start_sold_point:
            click_position(point[0], point[1])
            if len(self.fix_start_sold_point) != 1:
                time.sleep(1)

    def click_reward_open(self):
        if self.is_sold:
            for point in self.reward_sold_points:
                click_position(point[0], point[1])
                if len(self.reward_sold_points) != 1:
                    time.sleep(1)
                else:
                    time.sleep(0.2)
                    click_position(point[0], point[1])
                    time.sleep(0.2)
                    click_position(point[0], point[1])
        else:
            for point in self.reward_keep_points:
                click_position(point[0], point[1])
                if len(self.reward_keep_points) != 1:
                    time.sleep(1)
                else:
                    time.sleep(0.2)
                    click_position(point[0], point[1])
                    time.sleep(0.2)
                    click_position(point[0], point[1])

        for point in self.reward_treasure_points:
            click_position(point[0], point[1])
            if len(self.reward_treasure_points) != 1:
                time.sleep(1)

    def click_not_life(self):
        for point in self.failed_points:
            click_position(point[0], point[1])
            if len(self.failed_points) != 1:
                time.sleep(1)

    def click_victory(self):
        for point in self.end_points:
            click_position(point[0], point[1])
            if len(self.end_points) != 1:
                time.sleep(1)

    def no_power(self, is_shop=False):

            # get energy from gift box
            if not is_shop:
                if self.is_get_energy_form_gift:
                    click_position(self.gift_box_point[0][0], self.gift_box_point[0][1])
                    time.sleep(0.2)
                    click_position(self.gift_first_energy[0][0], self.gift_first_energy[0][1])
                    time.sleep(0.2)
                    click_position(self.gift_close_point[0][0], self.gift_close_point[0][1])
            # get energy from shop
            else:
                if self.is_get_energy_form_shop:
                    click_position(self.shop_point[0][0], self.shop_point[0][1])
                    time.sleep(0.2)
                    click_position(self.shop_energy_point[0][0], self.shop_energy_point[0][1])
                    time.sleep(0.2)
                    click_position(self.shop_purchase[0][0], self.shop_purchase[0][1])
                    time.sleep(0.2)
                    click_position(self.shop_purchase[1][0], self.shop_purchase[1][1])
                    time.sleep(0.2)
                    click_position(self.shop_close_point[0][0], self.shop_close_point[0][1])


if __name__ == '__main__':
   pass