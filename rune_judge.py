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

im = Images.open(r"D:\SBD\Python\Moling\rune\1565752876.1422284.png")
img = im.convert('L')
img = binarizing(img, 150)
data = pytesseract.image_to_string(img)
print(data)
print(judge_delete_rune(data))