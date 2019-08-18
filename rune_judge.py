from PIL import Image as Images, ImageDraw
import pytesseract
import re

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


class Rune(object):
    def __init__(self, data):
        self.info = data[:data.find("Set")]

        self.level = ""
        self.position = ""
        self.main_attr = ()
        self.sub_attr = {}

        self.set_level()
        self.set_attr()
        self.set_position()
        pass

    def set_level(self):
        level_map = {
            "Normal": 0,
            "Magic" : 1,
            "Rare"  : 2,
            "Hero"  : 3,
            "Legend": 4
        }

        for key in level_map:
            if key in self.info:
                self.level = level_map[key]

    def set_attr(self):
        attribute = re.findall(r"((HP|DEF|ATK|SPD|CRI Rate|CRI Dmg|Resistance|Accuracy) ?\+\d+%?)", self.info)
        for id, attr in enumerate(attribute):
            cur_attr = attribute[attr]
            if id == 1:
                self.main_attr = []
            self.attr[attribute[attr][1]] = attribute[attr][0]

    def set_position(self):
        position = re.findall(r'Rune \((\d)\)', self.info)
        self.position = int(position[0])

    def set_star(self):

        pass



def judge_delete_rune(data):

    data = data[:data.find("Set")]

    position = re.findall(r'Rune \((\d)\)', data)
    if position and int(position[0]) % 2 == 0 or True:
        # 2,4,6号位符文 加固定值除速度符文 直接扔
        attribute = re.findall(r"((HP|DEF|ATK|SPD|CRI Rate|CRI Dmg|Resistance|Accuracy) ?\+\d+%?)", data)
        print(attribute)
        if attribute[0][0].find("%") == -1 and attribute[0][0].find("SPD") == -1:
            return True

    return False

im = Images.open(r"C:\Project\Python\Moling\rune\1565743012.3344986.png")
img = im.convert('L')
img = binarizing(img, 150)
data = pytesseract.image_to_string(img)
print(data)
print(judge_delete_rune(data))