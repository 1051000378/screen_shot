# -*- coding: utf-8 -*- #
import datetime
import os
import subprocess
import sys
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QGridLayout, QLineEdit

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

    def screen(self, file_name):  # 在手机上截图
        file_name_tem = self.get_file_name(".png").strip()
        file_name1 = file_name.strip()
        print(file_name1)
        path = os.getcwd()
        print(path)
        cmd_screen = r"adb shell /system/bin/screencap -p /sdcard/" + file_name_tem  # 命令1：在手机上截图3.png为图片名
        cmd_pull = r"adb pull /sdcard/" + file_name_tem + " " + path #不加strip()会有空格导致不能上传图片
        print(cmd_screen)
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
        time.sleep(1)
        screenExecute.terminate()

        os.rename(os.path.join(path, file_name_tem), os.path.join(path, file_name1 + ".jpg"))


    def get_file_name(self, name):
        return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + name


    def screen_record(self, file_name):
        # adb shell screenrecord /sdcard/123.mp4（保存到SDCard）
        # adb pull /sdcard/123.mp4/ Users/uojie/Desktop/123.mp4（保存到电脑）
        file_name_temp = self.get_file_name(".mp4").strip() # 两个file_name的原因： 如果输入框是中文，传输过程中就会出现找不到文件的问题，中文会转化成bytes，但是不知道该如何转化
        file_name1 = file_name.strip()
        print(file_name1)
        path = os.getcwd()
        print(path)
        cmd1 = r"adb shell screenrecord --time-limit 10 /sdcard/" + file_name_temp # 命令1：在手机上截图3.png为图片名
        cmd2 = r"adb pull /sdcard/" + file_name_temp + " " + path
        print(cmd1)
        print(cmd2)

        screen_recored_Execute = subprocess.Popen(str(cmd1), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = screen_recored_Execute.communicate()
        # 输出执行命令结果结果
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        print(stdout)
        print(stderr)

        screen_recored_Execute = subprocess.Popen(str(cmd2), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = screen_recored_Execute.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        print(stdout)
        print(stderr)
        screen_recored_Execute.terminate()   # 重点：adb 命令执行完后要关闭 terminate
        os.rename(os.path.join(path, file_name_temp), os.path.join(path, file_name1 + ".mp4"))


class ScreenUI(QWidget):

    def __init__(self):
        super().__init__()
        self.screen1 = Screenshot()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        layout = QGridLayout()
        self.setWindowTitle("截图工具1.0")
        # 这种静态的方法设置一个用于显示工具提示的字体。我们使用10px滑动字体
        QToolTip.setFont(QFont('ScansSerif', 10))

        #显示一个button按钮 截图控件
        btn = QPushButton('截图', self)
        btn.resize(btn.sizeHint()) # 设置默认尺寸
        # btn.move(50, 50)
        btn.clicked.connect(self.on_click)  # 监听点击事件

        # 录制视频控件
        btn_record = QPushButton("开始录制",self)
        btn_record.resize(btn_record.sizeHint())
        btn_record.clicked.connect(self.on_click1)

        # todo 暂时没有想到可以停止录屏的功能，该功能暂时放弃


        # 输入框
        self.edit_text = QLineEdit(" ")

        layout.addWidget(self.edit_text, 1, 0)
        layout.addWidget(btn, 2, 0)
        layout.addWidget(btn_record, 3, 0)


        self.setLayout(layout)

        self.show()

    '''创建截图点击事件'''

    def on_click(self):
        name = self.edit_text.text()
        print(name)
        self.screen1.screen(name)

    '''视频点击事件'''
    def on_click1(self):
        name = self.edit_text.text()
        self.screen1.screen_record(name)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    screen = ScreenUI()

    sys.exit(app.exec_())




