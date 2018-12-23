# coding : utf-8
from __future__ import division
from PIL import Image


def calculate(image1, image2):
    g = image1.histogram()
    s = image2.histogram()
    assert len(g) == len(s), "error"

    data = []

    for index in range(0, len(g)):
        if g[index] != s[index]:
            data.append(1 - abs(g[index] - s[index]) / max(g[index], s[index]))
        else:
            data.append(1)

    return sum(data) / len(g)


def split_image(image, part_size):
    pw, ph = part_size
    w, h = image.size

    sub_image_list = []

    assert w % pw == h % ph == 0, "error"

    for i in range(0, w, pw):
        for j in range(0, h, ph):
            sub_image = image.crop((i, j, i + pw, j + ph)).copy()
            sub_image_list.append(sub_image)

    return sub_image_list


def classfiy_histogram_with_split(image1, image2, size=(256, 256), part_size=(64, 64)):

    img1 = image1.resize(size).convert("RGB")
    sub_image1 = split_image(img1, part_size)

    img2 = image2.resize(size).convert("RGB")
    sub_image2 = split_image(img2, part_size)

    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)

    x = size[0] / part_size[0]
    y = size[1] / part_size[1]

    pre = round((sub_data / (x * y)), 6)
    return pre * 100


if __name__ == '__main__':
    image_1 = Image.open("./1.png")
    image_2 = Image.open("./test.png")
    print(classfiy_histogram_with_split(image_1, image_2))
