#  coding = utf-8 

# @Time : 2021/3/15 9:38
# @Author : HJH
# @File : tieba.py
# @Software: PyCharm

import time
import os
import re
import base64
import requests
requests.packages.urllib3.disable_warnings()
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver



# 用图片url下载图片并保存成制定文件名
def downloadJPG(imgUrl, fileName):
    # 可自动关闭请求和响应的模块
    from contextlib import closing
    # proxies = {
    #     'http': 'socks5h://127.0.0.1:1080',
    #     'https': 'socks5h://127.0.0.1:1080'
    # }
    with closing(requests.get(imgUrl, stream=True, verify=False)) as resp:
        with open(fileName, 'wb') as f:
            for chunk in resp.iter_content(128):
                f.write(chunk)


# 批量下载图片，默认保存到当前目录下
def batchDownloadJPGs(imgUrls, suffix, count):
    # 用于给图片命名
    if imgUrls:
        path = 'E:\\Program Files (x86)\\Python\\pc\\tieba\\'+suffix+'\\'
        #  print(path)
        if not os.path.exists(path):
            os.mkdir(path)
        for url in imgUrls:
            # if count == 17:
            #     print(url)
            downloadJPG(url, ''.join([path, 'image{0}.jpg'.format(count)]))
            print('下载完成第{0}张图片'.format(count))
            count += 1
    else:
        print('无有效图片！')

    return count


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


def get_pages(url):
    page = requests.get(url, verify=False)
    # print(page.text)
    jpgReg2 = re.compile(r'\?pn=(\d{1,3})">尾页</a>')
    jpgs = re.findall(jpgReg2, str(page.text))
    if jpgs:
        results = int(jpgs[0])
        print('Page numbers: {}'.format(results))
    else:
        print('Page error!')
        results = 0
    return results


def get_images(url):
    page = requests.get(url, verify=False)
    # print(page.text)
    jpgReg2 = re.compile(r' src="(http.{50,300}\.jpg)" ')
    jpgs = re.findall(jpgReg2, str(page.text))
    results = list(set(jpgs))
    # print(len(results))

    return results


def download_tieba(url):
    pages = get_pages(url)
    count = 0
    if pages > 0:
        for i in range(1, pages+1):
            print("第{0}页".format(i))
            images = get_images(url[:-1]+str(i))
            new_count = batchDownloadJPGs(images, url.split('/')[-1][:-5], count)
            count = new_count


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

    # downloadJPG('https://s1.daibook.com/images/2021/03/13/005vT2WTly1goi44ccfjsj30m80xc77e.jpg','test.jpg')
    download_tieba('https://tieba.baidu.com/p/3097685300?pn=1')


    # get_urls('https://tieba.baidu.com/p/7257662774?pid=138286995348&cid=138331676859#138331676859')

