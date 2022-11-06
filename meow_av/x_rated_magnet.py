#  coding = utf-8 

# @Time : 2022/11/4 0:33
# @Author : HJH
# @File : x_rated_magnet.py
# @Software: PyCharm
# @Describe: 保存片子magnet及封面


import time
import datetime
import os
import re
import base64

from bs4 import BeautifulSoup
from selenium import webdriver


# 用图片url下载图片并保存成制定文件名
def save_imgs_base64(imgs, file_name, page):
    if imgs:
        # 可自动关闭请求和响应的模块
        path = urls_dict['saved_path'] + urls_dict[download_type]['saved_name'] + '\\' + str(page) + '\\'
        #  print(path)
        if not os.path.exists(path):
            os.mkdir(path)
        image_url = path + file_name + '.jpg'
        with open(image_url, 'wb') as f:
            f.write(base64.b64decode(imgs[0]))
        print("下载完成" + file_name)

    else:
        print("无有效目标，下载失败！")


# 解析网页，抓取图片及磁力链接
def get_img_content(url):
    # 打开chrome浏览器（需提前安装好chromedriver）
    option = webdriver.ChromeOptions()
    # option.add_argument('--headless') #无头模式，页面不显示，会导致页面加载失败，暂未解决
    browser = webdriver.Chrome(chrome_options=option)
    # print("正在打开网页...")
    browser.set_page_load_timeout(25)
    try:
        browser.get(url)
        browser.implicitly_wait(15)

        browser.execute_script("window.scrollTo(0, 3000);")
        time.sleep(2)
        # for i in range(1, 7):
        #     gap = "window.scrollTo(0, " + str(3500 + 1000 * i) + ");"
        #     browser.execute_script(gap)
        #     time.sleep(5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        print("正在获取网页数据...")
        soup = BeautifulSoup(browser.page_source, "lxml")
        # print(soup.prettify())

        jpgReg = re.compile(r'data:image/jpg;base64,(.+?)"')
        magnetReg = re.compile(r'<a href="(magnet:\?xt=urn:btih:.{20,100})">')
        # 解析出jpg的url列表
        jpg = re.findall(jpgReg, str(soup.prettify()))
        magnet = re.findall(magnetReg, str(soup.prettify()))

    except Exception as e:
        print('响应超时，重试！')
        try:
            browser.get(url)
            browser.implicitly_wait(15)

            browser.execute_script("window.scrollTo(0, 3000);")
            time.sleep(2)
            # for i in range(1, 7):
            #     gap = "window.scrollTo(0, " + str(3500 + 1000 * i) + ");"
            #     browser.execute_script(gap)
            #     time.sleep(5)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            print("正在获取网页数据...")
            soup = BeautifulSoup(browser.page_source, "lxml")
            # print(soup.prettify())

            jpgReg = re.compile(r'data:image/jpg;base64,(.+?)"')
            magnetReg = re.compile(r'<a href="(magnet:\?xt=urn:btih:.{20,100})">')
            # 解析出jpg的url列表
            jpg = re.findall(jpgReg, str(soup.prettify()))
            magnet = re.findall(magnetReg, str(soup.prettify()))
        except Exception as e:
            print(e)
            browser.execute_script('window.stop()')
            print(url)
            jpg = []
            magnet = []
    finally:
        browser.close()

    return jpg, magnet


# 解析网页抓取所有子页面地址
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
        jpg_reg = re.compile(r'a href="/cili/(detail-\d+\.html)" .{0,150}target="_blank" title="(.{5,100})">')
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


# 下载单页数据
def download_page(url, page):
    urls_and_titles = get_urls(url)
    success_list = []
    if urls_and_titles:
        for url_and_title in urls_and_titles[:]:
            current_url, title = url_and_title[0], url_and_title[1]
            page_url = url.split('list')[0] + current_url
            content, magnets = get_img_content(page_url)
            for i in magnets:
                title += '\t' + i
            success_list.append(title)
            save_imgs_base64(content, title.split(' ')[0], page)
    return success_list


# 下载多页数据
def download_by_pages(page_range):
    saved_path = urls_dict['saved_path'] + urls_dict[download_type]['saved_name']
    url = urls_dict['domain'] + urls_dict[download_type]['url']
    if not os.path.exists(saved_path):
        os.mkdir(saved_path)
    for i in range(page_range[0], page_range[1]):
        current_url = url.format(str(i))
        print("Current Page:" + current_url)
        success_list = download_page(current_url, i)
        with open(saved_path + '\\saved_magnets.txt', 'a', encoding="utf-8") as f:
            f.write('\n'.join(success_list))
            f.write('\n')


if __name__ == '__main__':
    download_type = 1
    saved_page_range = [1, 40]
    urls_dict = {'domain': 'https://www.fc75ecc6aa65.com/',
                 'saved_path': 'E:\\Program Files (x86)\\Python\\pc\\cat\\',
                 1: {'url': 'cili/list-%E7%B4%A0%E4%BA%BA%E7%B3%BB%E5%88%97-{}.html',
                     'name': '素人系列',
                     'saved_name': 'suren'},
                 2: {'url': 'cili/list-%E5%8A%A8%E6%BC%AB%E7%B2%BE%E5%93%81-{}.html',
                     'name': '动漫精品',
                     'saved_name': 'cartoon_avi'},
                 3: {'url': 'cili/list-%E9%AB%98%E6%B8%85%E4%B8%AD%E6%96%87-{}.html',
                     'name': '高清中文',
                     'saved_name': 'high_definition'},
                 4: {'url': 'cili/list-%E5%9B%BD%E4%BA%A7%E5%8E%9F%E5%88%9B-{}.html',
                     'name': '国产原创',
                     'saved_name': 'domestic_original'},
                 }

    'https://www.177a592bb3c0.com/cili/list-%E7%B4%A0%E4%BA%BA%E7%B3%BB%E5%88%97-1.html'
    start_url = 'https://www.177a592bb3c0.com/cili/list-%E5%8A%A8%E6%BC%AB%E7%B2%BE%E5%93%81-{}.html'
    # print(get_img_content('https://www.9bb38788ab47.com/meinv/detail-236984.html'))

    download_by_pages(saved_page_range)
    # print(get_urls('https://www.89dc308139a6.com/cili/list-%E5%8A%A8%E6%BC%AB%E7%B2%BE%E5%93%81-4.html'))
    # img, magnet = get_img_content('https://www.89dc308139a6.com/cili/detail-206723.html')
    # print(img)
    # print(magnet)
