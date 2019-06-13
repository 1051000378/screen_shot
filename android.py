# -*- coding: utf-8 -*- #
import datetime
import json
import os
import platform
import subprocess
import time
from tkinter import *

__author__ = 'jiashumeng'
'''
Description: 
'''
# 截取设备的名字串
def handler_name(device_name):
    return device_name.split("\t")[0]


class adb():

    def __init__(self):
        # 获取主程序执行的路径
        # main_dir = os.getcwd()
        main_dir = ".\\"
        # 拼接路径
        if platform.system() == 'Windows':
            self.adb_path = os.path.join(main_dir, "tools", 'adb.exe')
            print(self.adb_path)
            # 系统的换行符号
            self.enter_char = '\r\n'
        else:
            self.adb_path = os.path.join(main_dir, "tools", 'adb')
            self.enter_char = '\n'

        # 保存所有已连接的设备
        self.all_device = []
        self.adb_version()

    def adb_version(self):
        # 获取当前adb的版本号
        result = self.run("version").split(self.enter_char)
        print("ADB版本信息：\n\t", result[0])

        self.has_device()
        pass

# 查看是否有Android设备
    def has_device(self):
        has_device = False
        while not has_device:
            result = self.run("devices")
            if result == ('List of devices attached' + self.enter_char + self.enter_char):
                print("请连接Android设备...")
            else:
                # 找到了设备
                print("找到以下设备：")
                devices = result.split(self.enter_char)
                all_device = []
                index = 0
                for device in devices:
                    # 获取所有设备
                    if device.endswith('device') or device.endswith('unauthorized'):
                        # 去除\t
                        all_device.append(handler_name(device))
                        print('\t设备序号：%d\t设备名称：%s' % (index, device))
                        has_device = True
                        index += 1
                self.all_device = all_device
            time.sleep(3)



    """ 
    执行adb命令
    最终拼接成 adb version/devices   
    """

    def run(self, cmd):
        # Mac平台需要指定shell=True
        process = subprocess.Popen(self.adb_path + " " + cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=True)
        output = process.communicate()
        return output[0].decode('utf8')

    def get_adb_path(self):
        return self.adb_path

    def get_devices(self):
        return self.all_device

class config():

    def __init__(self):
        # 获取主程序执行的路径
        # main_dir = os.getcwd()
        main_dir = '.\\'
        # 拼接路径
        file_config = os.path.join(main_dir, "tools", 'config.json')
        with open(file_config, 'r') as c:
            config = json.load(c)
            # 保存配置
            self.save_path = config['save_path']
            self.delete_shot = config['delete_shot']


class screen_shot():
    """
    adb adb对象
    save_path 截图保存的路径
    delete_shot 截图完成是否需要删除手机上的截图
    """

    def screen_shot(self, adb, device, save_path, delete_shot):
        file_name = self.get_file_name()
        screen_cap = adb.run("-s " + device + " shell screencap -p /sdcard/" + file_name)
        if self.check_result(screen_cap):
            # 截图失败
            print('截图失败：' + screen_cap)
            return
        pull = adb.run("-s " + device + " pull /sdcard/" + file_name + " " + save_path)
        if self.check_result(pull):
            # 拷贝出错了
            print('拷贝截图失败：' + pull)
            return
        print("截图成功，文件已保存至：" + save_path + file_name)
        # 删除截图
        if delete_shot:
            adb.run("shell rm /sdcard/" + file_name)
        pass

    def get_file_name(self):
        return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.png'

    # 分析返回结果
    def check_result(self, result):
        if result.startswith('adb: error'):
            return True


def loop(device):
    # while True:
    #     user_answer = input("是否需要截图 y/n：\n")
    #     if user_answer == 'y':
    #         shot.screen_shot(adb, device, config.save_path, config.delete_shot)
    #     elif user_answer == 'n':
    #         exit(0)
    #     else:
    #         print("无法识别你的答案,请重新输入!")
    #     pass
    # shot.screen_shot(adb, device, config.save_path, config.delete_shot)
    shot.screen_shot(adb, device, "C:/Users/Arrow/Desktop/", True)


if __name__ == '__main__':

    # root = Tk()
    # root.title("截图工具1.0")
    # root.geometry('300*400')
    # root.resizable(width=True, height=True)

    # 获取配置
    # config = config()

    # 对adb进行初始化
    adb = adb()

    # 获取当前连接了多少台设备
    count = len(adb.get_devices())
    print(count)
    shot = screen_shot()
    if 0 <= count <= 1:
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