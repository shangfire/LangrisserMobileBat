# coding=utf-8
from PIL import Image
from PIL import ImageGrab
import win32api
import win32gui
import win32con
import pytesseract


# 单击
def single_click(window_handle, x, y):
    win32gui.PostMessage(window_handle, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x, y))
    win32gui.PostMessage(window_handle, win32con.WM_LBUTTONUP, 1, win32api.MAKELONG(x, y))
    return


# 拖拽至底部
def drag_to_bottom(window_handle, x, y, distance):
    step_length = 10
    win32gui.PostMessage(window_handle, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x, y))
    while y < distance:
        y = y + step_length
        win32gui.PostMessage(window_handle, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(x, y))
        win32api.Sleep(50)
    win32gui.PostMessage(window_handle, win32con.WM_LBUTTONUP, 1, win32api.MAKELONG(x, y))
    return


# 拖拽至顶部
def drag_to_top(window_handle, x, y):
    win32gui.PostMessage(window_handle, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x, y))
    win32gui.PostMessage(window_handle, win32con.WM_LBUTTONUP, 1, win32api.MAKELONG(x, y))
    return


print('hello,world')

handle_target = 0x001C0952
handle_toolbar = 0x000B07F6
handle_list = 0x0014099A
# win32gui.SetWindowPos(handle_target, win32con.HWND_TOPMOST, 0, 0, 1000, 1000, win32con.SWP_NOZORDER)
# single_click(handle_toolbar, 52, 2)
drag_to_bottom(handle_list, 511, 50, 300)

# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'
# text = pytesseract.image_to_string(Image.open("3.jpg"), lang="chi_sim")
# text = text.replace(" ", "")
# print(text)

# size = (300, 300, 400, 400)
# img = ImageGrab.grab(size)
# img.save("cut.jpg")
# img.show()

# text = pytesseract.image_to_string(Image.open("cut.jpg"), lang="chi_sim")
# text = text.replace(" ", "")
# print(text)

raw_input("输入回车以结束\n")
