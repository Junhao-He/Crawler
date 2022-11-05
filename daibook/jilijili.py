#  coding = utf-8 

# @Time : 2021/3/11 21:48
# @Author : HJH
# @File : jilijili.py
# @Software: PyCharm


import time
import os
import re
import base64
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver



# 用图片url下载图片并保存成制定文件名
def downloadJPG(imgUrl, fileName):
    # 可自动关闭请求和响应的模块
    from contextlib import closing
    with closing(requests.get(imgUrl, stream=True, verify=False)) as resp:
        with open(fileName, 'wb') as f:
            for chunk in resp.iter_content(128):
                f.write(chunk)


# 批量下载图片，默认保存到当前目录下
def batchDownloadJPGs(imgUrls, suffix):
    # 用于给图片命名
    count = 0
    if imgUrls:
        path = 'E:\\Program Files (x86)\\Python\\pc\\jili\\'+suffix+'\\'
        #  print(path)
        if not os.path.exists(path):
            os.mkdir(path)
        for url in imgUrls:
            downloadJPG(url, ''.join([path, 'image{0}.jpg'.format(count)]))
            print('下载完成第{0}张图片'.format(count))
            count += 1
    else:
        print('无有效图片！')


def get_img_content(url):
    # 打开chrome浏览器（需提前安装好chromedriver）
    browser = webdriver.Chrome()
    # browser = webdriver.PhantomJS()
    # print("正在打开网页...")

    try:
        browser.get(url)
        # print("等待网页响应...")
        # 需要等一下，直到页面加载完成
        browser.execute_script("window.scrollTo(0, 4000);")
        time.sleep(5)
        browser.execute_script("window.scrollTo(0, 10000);")
        time.sleep(10)
        browser.execute_script("window.scrollTo(0, 16000);")
        time.sleep(10)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        print("正在获取网页数据...")
        soup = BeautifulSoup(browser.page_source, "lxml")
        # print(soup.prettify())

        jpgReg = re.compile(r'data:image/jpg;base64,(.+?)" title=')
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
    page = requests.get(url, verify=False)
    # print(page.text)
    jpgReg2 = re.compile(r'href="(.+\.html)"')
    jpgs = re.findall(jpgReg2, str(page.text))
    results = list(set(jpgs))
    print('Page numbers: {}'.format(len(results)))

    return results


def get_images(url):
    page = requests.get(url, verify=False)
    # print(page.text)
    jpgReg2 = re.compile(r'<img src="(https://.{50,100}\.jpg)" alt=')
    jpgs = re.findall(jpgReg2, str(page.text))
    results = list(set(jpgs))
    print(len(results))

    return results


def download_jili(url):
    image_urls = get_urls(url)
    print(image_urls)
    for image_url in image_urls:
        images = get_images(image_url)
        batchDownloadJPGs(images, image_url.split('/')[-1].split('.')[0])


def get_html_content(url):
    browser = webdriver.Chrome()
    # browser = webdriver.PhantomJS()
    print("正在打开网页...")

    browser.get(url)
    # print("等待网页响应...")
    # 需要等一下，直到页面加载完成
    browser.execute_script("window.scrollTo(0, 4000);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    print("正在获取网页数据...")
    soup = BeautifulSoup(browser.page_source, "lxml")
    print(soup.prettify())

    # jpg_reg = re.compile(r'a href="/tupian/(\d+)\.html" target=')
    # jpgs = re.findall(jpg_reg, str(soup.prettify()))
    # print(len(jpgs))
    browser.close()


if __name__ == '__main__':
    download_jili('https://www.jiligame.com/category/cosplay/page/2')

    # print(len("https://s1.jiligame.com/images/2020/11/11/2711a34090dcc07c2766318672671a0a.jpg"))


    # download_cat("https://www.jiligame.com/category/cosplay")
    #
    # with open('E:\\Program Files (x86)\\Python\\pc\\cat\\saved_urls.txt', 'a') as f:
    #     f.write('\n'.join(successed_list))
