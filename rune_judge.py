import re

class Rune(object):
    def __init__(self, data):
        self.info = data[:data.find("Set")]

        self.level = 0
        self.position = 1
        self.start = 0
        self.main_attr = ()
        self.sub_attr = {}

        self.init_rune()
        pass

    def init_rune(self):
        if self.set_position():
            self.set_position()
            self.set_level()
            self.set_attr()
            self.set_star()

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
            cur_attr = attr
            if id == 0:
                self.main_attr = [cur_attr[1], cur_attr[0]]
            else:
                self.sub_attr[cur_attr[1]] = cur_attr[0]

    def set_position(self):
        position = re.findall(r'Rune \((\d)\)', self.info)
        if position:
            self.position = int(position[0])
            return True
        else:
            return False

    def set_star(self):
        if self.main_attr[1] in ["HP +11%", "HP +360", "ATK +11%", "ATK +22", "DEF +11%", "DEF +22", "SPD +7",
                                 "CRI Rate +7%", "CRI Dmg +11%", "Resistance +12%", "Accuracy +12%"]:
            self.start = 6
        else:
            self.start = 5

    def is_sell_rune(self):
        # 2,4,6号位符文 加固定值除速度符文 直接扔
        if self.position % 2 == 0:
            if self.main_attr[1].find("%") == -1 or self.main_attr[0].find("SPD") != -1:
                return True

        # 五星英雄以下直接卖
        if self.start == 5 and self.level < 3:
            return True

        # 六星副属性至少两个百分比
        if self.start == 6:
            per_count = 0
            for key in self.sub_attr:
                if key == "SPD" or self.sub_attr[key].find("%") != -1:
                    per_count += 1
            if per_count >= 2:
                return False
            else:
                return True

        return False


if __name__ == '__main__':
    from PIL import Image as Images, ImageDraw
    import pytesseract

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

    im = Images.open(r"C:\Project\Python\Moling\rune\1566114545.8649945sell_.png")
    region = (im.size[0] * 0.31, im.size[1] * 0.25, im.size[0] * 0.69, im.size[1] * 0.75)
    im = im.crop(region)
    img = im.convert('L')
    img = binarizing(img, 120)
    img.show()
    data = pytesseract.image_to_string(img)

    print(data)
    a = Rune(data)
    print(a.is_sell_rune())


