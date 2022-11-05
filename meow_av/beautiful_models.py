#  coding = utf-8 

# @Time : 2022/11/4 1:29
# @Author : HJH
# @File : beautiful_models.py
# @Software: PyCharm
# @Describe: 保存秀人等网站套图


import time
import datetime
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
        path = 'E:\\Program Files (x86)\\Python\\pc\\cat\\beauty\\' + website_dict[website_selected][
            'name'] + '\\' + fileName + '\\'
        #  print(path)
        if not os.path.exists(path):
            os.mkdir(path)
        count = 0
        for img in imgs:
            image_url = ''.join([path, 'image{0}.jpg'.format(count)])
            count += 1
            with open(image_url, 'wb') as f:
                f.write(base64.b64decode(img))
        print("下载完成{}".format(count))

    else:
        print("无有效目标，下载失败！")


def get_img_content(url):
    # 打开chrome浏览器（需提前安装好chromedriver）
    option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=option)
    # print("正在打开网页...")
    browser.set_page_load_timeout(25)
    try:
        browser.get(url)
        browser.implicitly_wait(15)

        browser.execute_script("window.scrollTo(0, 3500);")
        time.sleep(2)
        for i in range(1, 7):
            gap = "window.scrollTo(0, " + str(3500 + 1000 * i) + ");"
            browser.execute_script(gap)
            time.sleep(5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

        print("正在获取网页数据...")
        soup = BeautifulSoup(browser.page_source, "lxml")
        # print(soup.prettify())

        jpgReg = re.compile(r'data:image/jpg;base64,(.+?)"')
        # 解析出jpg的url列表
        jpgs = re.findall(jpgReg, str(soup.prettify()))

    except Exception as e:
        print('响应超时，重试！')
        try:
            browser.get(url)
            browser.implicitly_wait(15)

            browser.execute_script("window.scrollTo(0, 3500);")
            time.sleep(5)
            for i in range(1, 7):
                gap = "window.scrollTo(0, " + str(3500 + 1000 * i) + ");"
                browser.execute_script(gap)
                time.sleep(5)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            print("正在获取网页数据...")
            soup = BeautifulSoup(browser.page_source, "lxml")
            # print(soup.prettify())

            jpgReg = re.compile(r'data:image/jpg;base64,(.+?)"')
            # 解析出jpg的url列表
            jpgs = re.findall(jpgReg, str(soup.prettify()))
        except Exception as e:
            print(e)
            browser.execute_script('window.stop()')
            print(url)
            jpgs = []


    # try:
    #     # before_time = datetime.datetime.now()  # Timestamp
    #     browser.get(url)
    #     browser.implicitly_wait(3)
    #     # now_time = datetime.datetime.now()  # Timestamp
    #     # print('响应用时'+str((now_time-before_time).seconds))
    #
    #
    #     # print("等待网页响应...")
    #     # 需要等一下，直到页面加载完成
    #     browser.execute_script("window.scrollTo(0, 3500);")
    #     time.sleep(2)
    #     for i in range(1, 7):
    #         gap = "window.scrollTo(0, " + str(3500+1000*i)+");"
    #         browser.execute_script(gap)
    #         time.sleep(5)
    #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(4)
    #
    #     print("正在获取网页数据...")
    #     soup = BeautifulSoup(browser.page_source, "lxml")
    #     # print(soup.prettify())
    #
    #     jpgReg = re.compile(r'data:image/jpg;base64,(.+?)"')
    #     # 解析出jpg的url列表
    #     jpgs = re.findall(jpgReg, str(soup.prettify()))
    #     if len(jpgs) == 0:
    #         browser.get(url)
    #         # print("等待网页响应...")
    #         # 需要等一下，直到页面加载完成
    #         browser.implicitly_wait(3)
    #         browser.execute_script("window.scrollTo(0, 3500);")
    #         time.sleep(3)
    #         for i in range(1, 7):
    #             gap = "window.scrollTo(0, " + str(3500 + 1000 * i) + ");"
    #             browser.execute_script(gap)
    #             time.sleep(5)
    #         browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         time.sleep(10)
    #
    #         print("正在获取网页数据...")
    #         soup = BeautifulSoup(browser.page_source, "lxml")
    #         # print(soup.prettify())
    #
    #         jpgReg = re.compile(r'data:image/jpg;base64,(.+?)"')
    #         # 解析出jpg的url列表
    #         jpgs = re.findall(jpgReg, str(soup.prettify()))
    #     print(len(jpgs))
    #
    #     # jpgReg2 = re.compile(r'<a href="/tupian/(\d+\.html)" target')
    #     # next_url = re.findall(jpgReg2, str(soup.prettify()))
    # except Exception as e:
    #     print(e)
    #     print(url)
    #     jpgs = []

    finally:
        browser.close()

    return jpgs


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

        # jpg_reg = re.compile(r'a href="/(?:meinv|tupian)/(detail-\d+\.html)" target=')
        # 同时提取子页面地址与期号，期号作为文件夹名
        jpg_reg = re.compile(r'a href="/(?:meinv|tupian)/(detail-\d+\.html)" target="_blank" title="(.{5,10})">')
        jpgs = re.findall(jpg_reg, str(soup.prettify()))
        print("page_htmls:" + str(len(jpgs)))
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
    urls_and_titles = get_urls(url)
    success_list = []
    if urls_and_titles:
        for url_and_title in urls_and_titles[:]:
            current_url, title = url_and_title[0], url_and_title[1]
            page = url.split('chapter')[0] + current_url
            contents = get_img_content(page)
            success_list.append(title)
            save_imgs_base64(contents, title)
    return success_list


def download_by_pages(url, start, end):
    for i in range(start, end):
        current_url = url.format(str(i))
        print("Current Page:" + current_url)
        success_list = download_page(current_url)
        with open('E:\\Program Files (x86)\\Python\\pc\\cat\\beauty\\' + website_dict[website_selected][
            'name'] + '\\saved_urls.txt', 'a') as f:
            f.write('\t'.join(success_list))
            f.write('\n')


if __name__ == '__main__':
    website_dict = {1: {'name': 'huayang', 'chapter_num': '63'},
                    2: {'name': 'xiuren', 'chapter_num': '33'},
                    3: {'name': 'youwuguan', 'chapter)num': '57'}}

    start_page, end_page = 1, 36
    website_selected = 2
    start_url = 'https://www.89dc308139a6.com/meinv/chapter-' + website_dict[website_selected][
        'chapter_num'] + '-{}.html'
    # print(get_img_content('https://www.9bb38788ab47.com/meinv/detail-236984.html'))

    download_by_pages(start_url, start_page, end_page)
