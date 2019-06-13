# -*- coding: utf-8 -*- #
import platform

from android import *
from tkinter import *

import pythoncom


__author__ = 'jiashumeng'
'''
Description: 
'''

import time

import win32gui, win32ui, win32con, win32api

def window_capture(filename):

  hwnd = 0 # 窗口的编号，0号表示当前活跃窗口

  # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）

  hwndDC = win32gui.GetWindowDC(hwnd)

  # 根据窗口的DC获取mfcDC

  mfcDC = win32ui.CreateDCFromHandle(hwndDC)

  # mfcDC创建可兼容的DC

  saveDC = mfcDC.CreateCompatibleDC()

  # 创建bigmap准备保存图片

  saveBitMap = win32ui.CreateBitmap()

  # 获取监控器信息

  MoniterDev = win32api.EnumDisplayMonitors(None, None)

  w = MoniterDev[0][2][2]

  h = MoniterDev[0][2][3]

  # print w,h　　　#图片大小

  # 为bitmap开辟空间

  saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

  # 高度saveDC，将截图保存到saveBitmap中

  saveDC.SelectObject(saveBitMap)

  # 截取从左上角（0，0）长宽为（w，h）的图片

  saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)

  saveBitMap.SaveBitmapFile(saveDC, filename)

# beg = time.time()
#
# for i in range(10):
#
#   window_capture("haha%s.jpg" % i)
#
# end = time.time()
#
# print(end - beg)


def loop(device):
    while True:
        user_answer = input("是否需要截图 y/n：\n")
        if user_answer == 'y':
            shot.screen_shot(adb, device, config.save_path, config.delete_shot)
        elif user_answer == 'n':
            exit(0)
        else:
            print("无法识别你的答案,请重新输入!")
        pass



if __name__ == '__main__':

    # root = Tk()
    # root.title('截图工具1.0')
    # root.geometry('300*400')
    # root.resizable(width=True, height=True)
    #
    # # 输入框
    # image_name = Entry(root, bd = 5)
    #
    # # 截图按钮
    # btn_screenshot = Button(root, text = "开始截图", command=)

    config = config()

    # 对adb进行初始化
    adb = adb()

    # 获取当前连接了多少台设备
    count = len(adb.get_devices())
    if count > 0:
        shot = screen_shot()
        if 0 < count <= 1:
            # 取第一个设备
            loop(adb.get_devices()[0])
            pass
        # 有多个设备的时候
        else:
            illegal = True
            while illegal:
                index = input("请输入设备序号来选择截图的设备：\n")
                index = int(index)
                if 0 <= index <= count - 1:
                    illegal = False
                    loop(adb.get_devices()[index])
                else:
                    print("输入的设备序号非法！请重新输入")
    else:
        print(platform.system())
        name = input("请输入你要截图的名称：")
        # 调用截屏函数
        window_capture(name + ".jpg")