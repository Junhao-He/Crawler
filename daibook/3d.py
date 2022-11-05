#  coding = utf-8 

# @Time : 2021/3/3 11:57
# @Author : HJH
# @File : 3d.py
# @Software: PyCharm

import requests
import re
import os
import gzip
import base64
import json
from io import StringIO



class WebCrawler:
    def get_content(self, html):
        r = requests.get(html)
        return r.text

    # 从html中解析出所有jpg图片的url
    def getJPGs(self, html):
        # 解析jpg图片url的正则
        # jpgReg = re.compile(r'data-src=".+')  # 注：这里最后加一个'width'是为了提高匹配精确度
        content = requests.get(html).text
        print(content)
        jpgReg = re.compile(r'href="(.+?.html)" class=')
        # 解析出jpg的url列表
        jpgs = re.findall(jpgReg, content)
        print(len(jpgs))
        return jpgs

    # 用图片url下载图片并保存成制定文件名
    def downloadJPG(self, imgUrl, fileName):
        # 可自动关闭请求和响应的模块
        from contextlib import closing
        with closing(requests.get(imgUrl, stream=True, verify=False)) as resp:
            with open(fileName, 'wb') as f:
                for chunk in resp.iter_content(128):
                    f.write(chunk)

    # 批量下载图片，默认保存到当前目录下
    def batchDownloadJPGs(self, imgUrls, suffix):
        # 用于给图片命名
        # count = 1
        global count
        path = 'E:\\Program Files (x86)\\Python\\pc\\wechat' + suffix + '\\'
        #  print(path)
        if not os.path.exists(path):
            os.mkdir(path)
        for url in imgUrls:
            self.downloadJPG(url, ''.join([path, 'image{0}.jpg'.format(count)]))
            print('下载完成第{0}张图片'.format(count))
            count += 1

    def test(self, url):

        headers = {
            'Accept': 'application/gzip'
        }
        response = requests.get(url=url, headers=headers)
        print(response.headers['Content-Encoding'])
        print(response.content)
        gf = gzip.GzipFile(fileobj=StringIO(response.text), mode="r")
        data = gf.read()
        print(type(data))
        # compressedstream = StringIO(response.text)
        # re = gzip.GzipFile(fileobj=compressedstream)
        # print(json.loads(response.text))
        gf.close()
        return data


if __name__ == '__main__':
    # so = WebCrawler()
    # print(so.test('https://ss.qysrdjg.com/tp/fulitupian/qingchun/958/17.jpg.txt'))
    # print(so.get_content('https://www.d50462024196.com/tupian/132396.html'))

    gz_file = gzip.open("test.txt.gz", "rb")
    img_file_buf = gz_file.read()
    print(type(img_file_buf), len(img_file_buf))
    import cv2
    import numpy as np
    img = cv2.imdecode(np.frombuffer(img_file_buf, np.uint8), 1)
    cv2.imshow("", img)
    gz_file.close()
