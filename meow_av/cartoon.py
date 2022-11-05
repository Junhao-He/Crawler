#  coding = utf-8 

# @Time : 2021/3/7 9:27
# @Author : HJH
# @File : cartoon.py
# @Software: PyCharm
# @Describe: 保存动漫图片


import time
import os
import re
import base64
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# 用图片url下载图片并保存成制定文件名
def save_imgs_base64(imgs, fileName):
    if imgs:
        # 可自动关闭请求和响应的模块
        path = 'E:\\Program Files (x86)\\Python\\pc\\cat\\cartoon\\' + fileName.split('-')[1] + '\\'
        #  print(path)
        if not os.path.exists(path):
            os.mkdir(path)
        count = 0
        for img in imgs:
            image_url = ''.join([path, 'image{0}.jpg'.format(count)])
            count += 1
            with open(image_url, 'wb') as f:
                f.write(base64.b64decode(img))
            # print("下载完成{}".format(count))

    else:
        print("无有效目标，下载失败！")


def get_img_content(url):
    # 打开chrome浏览器（需提前安装好chromedriver）
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=option)
    # print("正在打开网页...")

    try:
        browser.get(url)
        browser.implicitly_wait(3)
        # print("等待网页响应...")
        # 需要等一下，直到页面加载完成
        browser.execute_script("window.scrollTo(0, 3500);")
        time.sleep(3)
        for i in range(1, 7):
            gap = "window.scrollTo(0, " + str(3500+1000*i)+");"
            browser.execute_script(gap)
            time.sleep(5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        print("正在获取网页数据...")
        soup = BeautifulSoup(browser.page_source, "lxml")
        # print(soup.prettify())

        jpgReg = re.compile(r'data:image/jpg;base64,(.+?)"')
        # 解析出jpg的url列表
        jpgs = re.findall(jpgReg, str(soup.prettify()))
        if len(jpgs) == 0:
            browser.get(url)
            # print("等待网页响应...")
            # 需要等一下，直到页面加载完成
            browser.execute_script("window.scrollTo(0, 3500);")
            time.sleep(3)
            for i in range(1, 7):
                gap = "window.scrollTo(0, " + str(3500 + 1000 * i) + ");"
                browser.execute_script(gap)
                time.sleep(5)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            print("正在获取网页数据...")
            soup = BeautifulSoup(browser.page_source, "lxml")
            # print(soup.prettify())

            jpgReg = re.compile(r'data:image/jpg;base64,(.+?)"')
            # 解析出jpg的url列表
            jpgs = re.findall(jpgReg, str(soup.prettify()))
        print(len(jpgs))

        # jpgReg2 = re.compile(r'<a href="/tupian/(\d+\.html)" target')
        # next_url = re.findall(jpgReg2, str(soup.prettify()))
    except Exception as e:
        print(e)
        print(url)
        jpgs = []

    finally:
        browser.close()

    return jpgs


def test_re():
    text = """<div class="photo-content-title-text-main ad-container" id="photo-content-title-text-main-foot" style="display: inherit;">
</div>
<div class="next-page">
<div class="content-next1 text-ellipsis">上一篇: <a href="/tupian/132951.html" target="_blank">丰满的美乳美女 </a></div>
<div class="content-next2 text-ellipsis">下一篇: <a href="/tupian/132954.html" target="_blank">若隐若现的乳头，看了就会上火 </a></div>
</div>
<div class="photo--content-title-bottomx--foot ad-container" id="photo--content-title-bottomx--foot" style="display: inherit;"></div>
</main>"""
    jpgReg2 = re.compile(r'<a href="/tupian/(\d+\.html)" target')
    next_url = re.findall(jpgReg2, str(text))
    return next_url


def get_urls(url):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=option)
    # browser = webdriver.PhantomJS()
    print("正在打开网页...")

    try:
        browser.get(url)
        browser.implicitly_wait(3)
        # print("等待网页响应...")
        # 需要等一下，直到页面加载完成
        browser.execute_script("window.scrollTo(0, 4000);")
        time.sleep(5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

        print("正在获取网页数据...")
        soup = BeautifulSoup(browser.page_source, "lxml")
        # print(soup.prettify())

        jpg_reg = re.compile(r'a href="/(?:meinv|tupian)/(detail-\d+\.html)" target=')
        jpgs = re.findall(jpg_reg, str(soup.prettify()))
        print("page_htmls:"+str(len(jpgs)))
        # print(jpgs)

    except Exception as e:
        print(e)
        jpgs = []
    finally:
        browser.close()
    if not jpgs:
        print("No target detected!!!")
    return jpgs


def download_page(url):
    image_urls = get_urls(url)
    flag = 0
    successed_list = []
    if len(image_urls) > 0:
        images_sum = []
        for image_url in image_urls:
            # print(url.split('list')[0] + image_url)
            page = url.split('list')[0] + image_url
            images_sum.extend(get_img_content(page))
            successed_list.append(page.split('/')[-1].split('.')[0].split('-')[1])
            if flag < 4:
                flag += 1
            else:
                flag = 0
                save_imgs_base64(images_sum, page.split('/')[-1].split('.')[0])
                images_sum = []
    return successed_list


def download_by_pages(url, num):

    for i in range(1, num):
        current_url = url.format(str(i))
        print("Current Page:"+current_url)
        successed_list = download_page(current_url)
        with open('E:\\Program Files (x86)\\Python\\pc\\cat\\cartoon\\saved_urls.txt', 'a') as f:
            f.write('\t'.join(successed_list))
            f.write('\n')


if __name__ == '__main__':
    # 动漫
    pages = 10
    start_url = 'https://www.9bb38788ab47.com/tupian/list-%E5%8D%A1%E9%80%9A%E5%8A%A8%E6%BC%AB-{}.html'

    download_by_pages(start_url, pages)



