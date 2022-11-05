#  coding = utf-8 

# @Time : 2021/1/20 16:03
# @Author : HJH
# @File : wechat_official_accounts.py
# @Software: PyCharm


import os
import requests
import re


def get_content(html):
    r = requests.get(html)
    return r.text


# 从html中解析出所有jpg图片的url
def getJPGs(html):
    # 解析jpg图片url的正则
    # jpgReg = re.compile(r'data-src=".+')  # 注：这里最后加一个'width'是为了提高匹配精确度
    jpgReg = re.compile(r'data-src="(.+?=jpeg)" ')
    # 解析出jpg的url列表
    jpgs = re.findall(jpgReg, html)
    print(len(jpgs))
    return jpgs


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
    # count = 1
    global count
    path = 'E:\\Program Files (x86)\\Python\\pc\\wechat' + suffix + '\\'
    #  print(path)
    if not os.path.exists(path):
        os.mkdir(path)
    for url in imgUrls:
        downloadJPG(url, ''.join([path, 'image{0}.jpg'.format(count)]))
        print('下载完成第{0}张图片'.format(count))
        count += 1


if __name__ == '__main__':
    # website = 'https://mp.weixin.qq.com/s/k12ffH1UQUadd5RI-7O-5w'
    website = 'https://mp.weixin.qq.com/s/wDePso7LwoXtVNrbqjg53g'
    con = get_content(website)
    # print(con)
    # print(getJPGs(con))
    count = 0
    batchDownloadJPGs(getJPGs(con), '_3')
