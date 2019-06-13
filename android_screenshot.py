# -*- coding: utf-8 -*- #
import datetime
import os
import subprocess
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton

__author__ = 'jiashumeng'
'''
Description: 
'''

'''
1.执行adb命令获取设备
2.截图保存到本地
3.将图片pull到电脑上


'''


class Screenshot():  # 截取手机屏幕并保存到电脑
    def __init__(self):
        # 查看连接的手机
        connect = subprocess.Popen("adb devices", stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = connect.communicate()  # 获取返回命令
        # 输出执行命令结果结果
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        print(stdout)
        print(stderr)

    def screen(self):  # 在手机上截图
        file_name = self.get_file_name()
        path = os.getcwd()
        print(path)
        cmd_screen = r"adb shell /system/bin/screencap -p /sdcard/" + file_name  # 命令1：在手机上截图3.png为图片名
        cmd_pull = r"adb pull /sdcard/" + file_name + " " + path

        screenExecute = subprocess.Popen(str(cmd_screen), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = screenExecute.communicate()
        # 输出执行命令结果结果
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        print(stdout)
        print(stderr)

        screenExecute = subprocess.Popen(str(cmd_pull), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = screenExecute.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        # 输出执行命令结果结果
        # stdout = stdout.decode("utf-8")
        # stderr = stderr.decode("utf-8")
        print(stdout)
        print(stderr)

    # def saveComputer(self, cmd):  # 将截图保存到电脑
    #     screenExecute = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    #     stdout, stderr = screenExecute.communicate()
    #     stdout = stdout.decode("utf-8")
    #     stderr = stderr.decode("utf-8")
    #     # 输出执行命令结果结果
    #     # stdout = stdout.decode("utf-8")
    #     # stderr = stderr.decode("utf-8")
    #     print(stdout)
    #     print(stderr)


    def get_file_name(self):
        return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.png'


    def screen_record(self):
        # adb shell screenrecord /sdcard/123.mp4（保存到SDCard）
        # adb pull /sdcard/123.mp4/ Users/uojie/Desktop/123.mp4（保存到电脑）
        file_name = self.get_file_name()
        path = os.getcwd()
        print(path)
        cmd1 = r"adb shell screenrecord /sdcard" + file_name  # 命令1：在手机上截图3.png为图片名
        cmd2 = r"adb pull /sdcard/" + file_name + " " + path

        screenExecute = subprocess.Popen(str(cmd1), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = screenExecute.communicate()
        # 输出执行命令结果结果
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        print(stdout)
        print(stderr)

        screenExecute = subprocess.Popen(str(cmd2), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = screenExecute.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        print(stdout)
        print(stderr)

class ScreenUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 这种静态的方法设置一个用于显示工具提示的字体。我们使用10px滑动字体
        QToolTip.setFont(QFont('ScansSerif', 10))

        #显示一个button按钮 截图控件
        btn = QPushButton('截图', self)
        btn.resize(btn.sizeHint()) # 设置默认尺寸
        btn.move(50, 50)
        btn.clicked.connect(self.on_click)  # 监听点击事件

        # 录制视频控件
        btn_record = QPushButton("开始录制",self)
        btn_record.resize(btn.sizeHint())
        btn_record.clicked.connect(self.on_click1)



        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("截图工具1.0")
        self.show()

    '''创建截图点击事件'''
    @pyqtSlot()
    def on_click(self):
        screen = Screenshot()
        screen.screen()

    def on_click1(self):
        pass



if __name__ == '__main__':
    # os.system("adb devices")

    # current_time = time.strftime('%Y-%m-%d-%H-%M-%S ', time.localtime(time.time()))+".png"
    # cmd1 = r"adb shell /system/bin/screencap -p /sdcard/"+ current_time  # 命令1：在手机上截图3.png为图片名
    # cmd2 = r"adb pull /sdcard/"+ current_time +" "+"D:\\123"  # 命令2：将图片保存到电脑 d:/3.png为要保存到电脑的路径

    app = QApplication(sys.argv)
    screen = ScreenUI()

    sys.exit(app.exec_())




