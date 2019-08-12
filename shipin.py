# python
# -*- coding:utf-8 -*-
# author:Only time:2019/8/10


from tkinter import messagebox  # 返回信息
import tkinter as tk  # 制作桌面编程
import re
import webbrowser  # 控制浏览器
from urllib import parse  # url解析视频播放地址的模块


class Procedure:

    # 初始化
    def __init__(self, width=500, height=100):
        self.w = width
        self.h = height
        self.title = '视频破解助手'
        self.root = tk.Tk(className=self.title)
        # 初始化位置大小
        self.root.geometry('+500+200')

        # 视频播放地址 StringVar() 定义字符串变量
        self.url = tk.StringVar()

        # 定义Frame 空间
        frame = tk.Frame(self.root)

        # 控件内容设置
        label_1 = tk.Label(frame, text='请输入电影/电视剧网址：', font=('华文行楷', 12), fg='blue')
        # 输入框声明
        entry = tk.Entry(frame, textvariable=self.url, width=35)
        go = tk.Button(frame, text='播放', font=('微软雅黑', 14), fg='Purple', width=2, height=1, command=self.video_go)

        # 控件布局 显示控件在软件上
        frame.pack()

        # 确定控件的位置 row  column
        label_1.grid(row=0, column=0)
        entry.grid(row=0, column=1)

        # ipadx x方向的外部填充  ipady y 方向的内部填充
        # ipadx ：设置控件里面水平方向空白区域大小； ipady ：设置控件里面垂直方向空白区域大小；
        go.grid(row=0, column=3, ipadx=30, ipady=20)

    def video_go(self):
        # 视频解析网站地址
        port = 'http://www.wmxz.wang/video.php?url='

        # 正则表达式判定是否为合法网址链接
        # match 这个方法从我们要匹配的字符串的头部开始，当匹配到string的尾部还没有匹配结束时，返回None;
        # 当匹配过程中出现了无法匹配的字母，返回None。
        if re.match(r'^https?:/{2}\w.+$', self.url.get()):

            # 取出用户输入的视频网址
            ip = self.url.get()
            # 视频链接加密
            ip = parse.quote_plus(ip)
            # 用浏览器打开网址
            webbrowser.open(port + ip)


        else:
            messagebox.showerror('错误', message='视频网址无效，请重新输入!')

    # 启动函数
    def loop(self):
        self.root.resizable(True, True)
        self.root.mainloop()


if __name__ == '__main__':
    procedure = Procedure()
    procedure.loop()
