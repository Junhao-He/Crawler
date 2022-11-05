#  coding = utf-8 

# @Time : 2021/11/2 10:29
# @Author : HJH
# @File : yb.py
# @Software: PyCharm

from hs import concede

import os,time
import pyautogui as pag
import random


def get_position():
    try:
        while True:
                print("Press Ctrl-C to end")
                x,y = pag.position() #返回鼠标的坐标
                posStr="Position:"+str(x).rjust(4)+','+str(y).rjust(4)
                print (posStr)#打印坐标
                time.sleep(1)
                os.system('cls')#清楚屏幕
    except  KeyboardInterrupt:
        print ('end....')


def click(x, y, t=20, button='primary'):
    """
    点击给定点附近,所有非强制要求点应使用该方法
    -------
    x,y : 位置(x,y)
    t : 默认20
    button : 默认'primary',可设为'left'/'right'/'middle'
    """
    pag.click(x + random.randint(-t, t), y + random.randint(-t, t), button=button)


def move(x, y, t=20):
    """
    移到给定点附近
    """
    pag.moveTo(x + random.randint(-t, t), y + random.randint(-t, t))


def drag(x0, y0, x1, y1, t=5):
    """
    从当前位置(x0,y0)拖拽到指定位置(x1,y1)
    """

    def mousedown(x, y, t):
        pag.mouseDown(x + random.randint(-t, t), y + random.randint(-t, t))

    def mouseup(x, y, t):
        pag.mouseUp(x + random.randint(-t, t), y + random.randint(-t, t))

    mousedown(x0, y0, t)
    move(x1, y1, t)
    time.sleep(0.5)
    mouseup(x1, y1, t)
        
        
def auto_1_1():
    """
    自动点击通关1-1
    :return: 
    """
    start_x, start_y = 111, 222
    click(start_x, start_y)
    time.sleep(3)
    

if __name__ == '__main__':


    # a = concede.Screen()
    # img_path = 'D:\\pyProjects\\crawler\\hs\\ssyy.jpeg'
    # a.resize(img_path)

    # for i in range(2, 11):
    #     pag.moveTo(400, 175 + i * 20,
    #                  duration=0.5)

    get_position()