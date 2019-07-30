import os
import time
import random
import platform

press_time = 1

def execute_cmd(cmd):
    cur_os = platform.system().lower()
    if "windows" in cur_os:
        stdout = 'NUL'
    else:
        stdout = '/dev/null'
    os.system(cmd + " >" + stdout + " 2>&1")
    #\  os.system(cmd)


def click_position(x, y):
    rand_int = random.randint(-5, 5)
    x += rand_int
    y += rand_int

    cmd = 'adb shell input swipe {} {} {} {} {}'.format(x, y, x, y, press_time)
    os.system(cmd)
    pass

def click_positions(positions):
    for index, position in enumerate(positions):
        click_position(position[0], position[1])
        if index != len(position) - 1:
            time.sleep(1)

def lock_screen():
    os.system('adb shell input keyevent 26')





