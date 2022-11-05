#  coding = utf-8 

# @Time : 2021/10/26 17:22
# @Author : HJH
# @File : concede.py
# @Software: PyCharm

import cv2
import pyautogui
import os
import random
import numpy as np
import time
from PIL import Image


class Screen():

    def resize(self, img_file, size=(496, 348), new_file=None, T=-1):
        """
        调整图片大小，便于识别以及引入图像识别。
        img_file : 要缩放或放大的图片路径。
        new_file : 新图片保留路径。若为None,自动补后缀_R,为''则返回新图像。
        size : 输出图像大小。
        """

        img = cv2.imread(img_file, T)
        height, width = size
        img_n = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        if new_file == '':
            return img_n
        if new_file is None:
            new_file = img_file[:img_file.index('.')] + '_R' + img_file[img_file.index('.'):]
        cv2.imwrite(new_file, img_n)
        return cv2.imread(new_file, T)

    def in_old(self, img_file, new_file, height1, width1, height0=0, width0=0):
        """
        是从已有图像中提取一部分进行分析， 避免多次截图。
        img_file : 已有图像路径名。
        new_file : 要保留图像路径名。
        height0 : int, 左上角，height1 : 图像高。
        width0 : int, 左上角，width1图像宽。
        """
        img = cv2.imread(img_file)
        img2 = img[height0:height1 + height0, width0:width1 + width0]
        cv2.imwrite(new_file, img2)

    def get_screen(self, img2='scree.jpg', region=(0, 0, 2560, 1440)):
        '''
        截屏
        ----------
        img2 : 图片存储路径. 默认'scree.jpg'.
        region : (x1,y1,width,hight) 截取矩形左顶点(x1,y1) 与矩形width,hight
        '''
        if region == 'default':
            region = (0, 0, 2560, 1440)
        elif len(region) < 4:
            raise ValueError('region值错误 截取矩形左顶点(x1,y1) 与矩形width,hight')
        try:
            pyautogui.screenshot(img2, region=region)
        except OSError:
            os.system("shutdown -s -t  60 ")

    def is_sim(self, img1='', img2='default', s=0.75, K1=True, N=True, region='default', mul=False, mul_I=[],
               thresh=None, T=-1, resize1=None, resize2=None):
        '''

        判断img2里是否有img1
        进行多图像匹配时,需要参数mul,img2,mul_I,region.
        多图像匹配时返回每个模板的匹配值
        ----------
        img1 :  The default is ''.
        img2 :  默认为'img1_1',格式与img1相同.
        s : 匹配最小值. The default is 0.75.
        K1 : 用于匹配值较小时使用,仅在测试时设置为False.
        N : 不截屏,而是使用已有图像,默认截屏.
        region : 传给get_screen.
        mul : 截图,匹配多图像,返回每个对象匹配值;
                若thresh不为None,则先二值化再匹配.
        mul_I : 图像中含有对象,list.
        T : 0表示灰度读取,-1表示彩色读取.传给cv2.imread().
        thresh : 不为None,则表示二值化后匹配,目前用于识别费用.不为None则T应该为0.
        resize : 是否需要对模板或图像进行调整大小后进行匹配。1表示对img1进行， 注意在N为True时可能产生异常。
                不为None时应直接指定size

        '''
        if mul:
            if N:
                self.get_screen(img2, region=region)
            if resize2 != None:
                im2 = self.resize(img2, size=resize2)
            else:
                im2 = cv2.imread(img2, T)
            if thresh != None:
                assert T == 0
                im2 = cv2.adaptiveThreshold(im2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                            cv2.THRESH_BINARY, 11, 2)
            M = []
            for i in mul_I:
                if resize1 == None:
                    im1 = cv2.imread(i, T)
                else:
                    im1 = self.resize(i, resize1)
                if thresh != None:
                    im1 = cv2.adaptiveThreshold(im1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                cv2.THRESH_BINARY, 11, 2)
                res = cv2.matchTemplate(im2, im1, cv2.TM_CCOEFF_NORMED)
                M.append(res.max())
            return M
        if resize1 == None:
            im1 = cv2.imread(img1, T)
        else:
            im1 = self.resize(img1, resize1)
        if img2 == 'default':
            img2 = img1[:img1.index('.')] + '_1' + img1[img1.index('.'):]
        if N:
            self.get_screen(img2, region=region)
        if resize2 == None:
            im2 = cv2.imread(img2, T)
        else:
            im2 = self.resize(img2, resize2)
        res = cv2.matchTemplate(im2, im1, cv2.TM_CCOEFF_NORMED)
        if not K1:
            return res.max()
        if res.max() < s:
            return False
        return True

    def get_position(self, img1='', img2='default', s=0.75, M=True, K1=True, N=True, region='default', T=-1,
                     thresh=None):
        '''
        建议设置img2参数,避免多进程抢资源.

        ----------
        img1 : 路径名,需要在屏幕上查找的图片

        img2 : 截图时临时存放位置. 默认为'img1_1',格式与img1相同.
        s : 不大于1的正数,传递给is_sim函数.
        M : BOOL, optional
            为False时,未查找到返回(100,100)点. The default is True.
        K1 : False 取消阈值 默认True.
        N  :    False表示不截图,直接进行图像对比, 默认True.
        region : 传给get_screen.
        T : 0表示灰度读取,-1表示彩色读取.传给cv2.imread().
        thresh : 不为None,则表示二值化后匹配,目前用于识别费用.
        Returns
        -------
        (X,Y) 图像中心点坐标
        '''

        if img2 == 'default':
            img2 = img1[:img1.index('.')] + '_1' + img1[img1.index('.'):]
        while K1 and self.is_sim(img1=img1, img2=img2, s=s, K1=K1, N=N, region=region, T=T, thresh=thresh) is not True:
            if M is True:
                continue
            else:
                return (100, 100)
        if N:
            self.get_screen(img2, region)
        d = Image.open(img1).size

        im = cv2.imread(img1, T)
        if thresh != None:
            im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                       cv2.THRESH_BINARY, 11, 2)
        im2 = cv2.imread(img2, T)
        if thresh != None:
            im2 = cv2.adaptiveThreshold(im2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                        cv2.THRESH_BINARY, 11, 2)
        res = cv2.matchTemplate(im2, im, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res == res.max())

        X = int(loc[1] + d[0] / 2)
        Y = int(loc[0] + d[1] / 2)
        if region != 'default':
            X += region[0]
            Y += region[1]
        return (X, Y)

    def click(self, x, y, t=20, button='primary'):
        '''
        点击给定点附近,所有非强制要求点应使用该方法
        -------
        x,y : 位置(x,y)
        t : 默认20
        button : 默认'primary',可设为'left'/'right'/'middle'
        '''
        pyautogui.click(x + random.randint(-t, t), y + random.randint(-t, t), button=button)

    def move(self, x, y, t=20):
        '''
        移到给定点附近
        '''
        pyautogui.moveTo(x + random.randint(-t, t), y + random.randint(-t, t))

    def drag(self, x0, y0, x1, y1, t=5):
        '''
        从当前位置(x0,y0)拖拽到指定位置(x1,y1)
        '''

        def mousedown(x, y, t):
            pyautogui.mouseDown(x + random.randint(-t, t), y + random.randint(-t, t))

        def mouseup(x, y, t):
            pyautogui.mouseUp(x + random.randint(-t, t), y + random.randint(-t, t))

        mousedown(x0, y0, t)
        self.move(x1, y1, t)
        time.sleep(0.5)
        mouseup(x1, y1, t)




