#!/usr/bin/python
# coding:utf-8

import requests
import re
import ssl
import os


# 根据url获取网页html内容
def getHtmlContent(url):
    page = requests.get(url, verify=False)
    return page.text


# 从html中解析出所有jpg图片的url
# 百度贴吧html中jpg图片的url格式为：<img ... src="XXX.jpg" width=...>
def getJPGs(html):
    # 解析jpg图片url的正则
    #jpgReg = re.compile(r'<img.+?src="(.+?\.jpg)" alt')  # 注：这里最后加一个'width'是为了提高匹配精确度
    jpgReg = re.compile(r"<img src='(.+?\.jpg)' alt")
    # 解析出jpg的url列表
    jpgs = re.findall(jpgReg, html)
    print(len(jpgs))
    return jpgs


# 用图片url下载图片并保存成制定文件名
def downloadJPG(imgUrl, fileName):
    # 可自动关闭请求和响应的模块
    from contextlib import closing
    with closing(requests.get(imgUrl,stream=True, verify=False)) as resp:
        with open(fileName, 'wb') as f:
            for chunk in resp.iter_content(128):
                f.write(chunk)


# 批量下载图片，默认保存到当前目录下
def batchDownloadJPGs(imgUrls, suffix):
    # 用于给图片命名
    #count = 1
    global count
    path = 'E:\\Program Files (x86)\\Python\\pc\\nvshen'+suffix+'\\'
    #  print(path)
    if not os.path.exists(path):
        os.mkdir(path)
    for url in imgUrls:
        downloadJPG(url, ''.join([path, 'image{0}.jpg'.format(count)]))
        print('下载完成第{0}张图片'.format(count))
        count += 1


# 封装：从百度贴吧网页下载图片
def download(url, suffix):
    html = getHtmlContent(url)
    jpgs = getJPGs(html)
    batchDownloadJPGs(jpgs, suffix)


def get_page(url):
    content = getHtmlContent(url)
    # < a href = "/p/2314539885?pn=31" >尾页 < / a >
    pattern = r'<a href="/p/.*?pn=(.*)">尾页</a>'
    return int(re.findall(pattern, content)[0])


def create_url(url, page):
    url_list = []
    for i in range(page):
        print("第%s页" %(i+1))
        new_url = url+'?pn=%d' %(i+1)
        url_list.append(new_url)
    return url_list


def get_html_list(url):
    html = getHtmlContent(url)
    #print(html)
    a = "<ul><li class='galleryli'><div class='galleryli_div'><a class='galleryli_link' href='/g/29658/' ><img alt='Musubu Funaki"
    urlReg = re.compile(r"<a class='galleryli_link' href='(/g/\d+/)' ><")
    urls = re.findall(urlReg, html)
    #print(len(urls))
    return urls


def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://www.nvshens.com/gallery/meitui/3.html'
    url_list = get_html_list(url)
    for j in url_list:
        global count
        count = 1
        for i in range(10):
            try:
                each_url = 'https://www.nvshens.com'+j+'{}.html'.format(i+1)
                print(each_url)
                download(each_url, j[2:8])
            except:
                continue


if __name__ == '__main__':
    main()
