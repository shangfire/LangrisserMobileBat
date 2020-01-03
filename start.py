# encoding:gbk
# import mytest
from PIL import Image
from PIL import ImageGrab
import win32api
import win32gui
import win32con
import time
import importlib

print("Author:@节能的戈登")
# c = __import__('mytest.py')
c = importlib.import_module("mytest")
c.bat_main()
# mytest.bat_main()
