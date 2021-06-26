# import mytest
from PIL import Image
from PIL import ImageGrab
import win32api
import win32gui
import win32con
import time
import importlib
import configparser
import os

# target_bat = 1

print("Author:@节能的戈登")
# inp = input("请输入想要刷的类型，1-兄贵/2-魔神英雄传活动，以回车确定：")
# target_bat = int(inp)
# if target_bat != 1 and target_bat != 2:
#     print("输入错误，只能是1-2之间的数字")
#     exit(0)

# if target_bat == 1:
module = importlib.import_module("bat_core")
# elif target_bat == 2:
#     module = importlib.import_module("bat_core_activity")

module.bat_main()
