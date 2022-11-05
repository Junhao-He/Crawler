#  coding = utf-8 

# @Time : 2022/8/19 9:50
# @Author : HJH
# @File : xyz.py
# @Software: PyCharm

import time
import json
import re
import base64
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


def get_html_content(html):
    r = requests.get(html)
    return r.text


def get_img_content_sleep(url):
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
    text = """<div class="titletablerow">
      <div class="titletablecell titletablegreen"><a href="/amyg_1193504.html" target="_self">【中文字幕】SNIS866 和女高中生甜蜜散歩 羽咲美晴[MP4/3.77GB]</a></div>
      <div class="titletablecell titletableblue">08-18</div>
    </div>
<div class="titletablerow">
      <div class="titletablecell titletablegreen"><a href="/amyg_1193503.html" target="_self">【中文字幕】SNIS621 褐色少女闪电復活啦！扒开小穴特别篇 高千穗铃[MP4/3.93GB]</a></div>
      <div class="titletablecell titletableblue">08-18</div>
    </div>
<div class="titletablerow">
      <div class="titletablecell titletablegreen"><a href="/amyg_1193502.html" target="_self">【中文字幕】SGA076 性慾超旺瑜珈教练下海啦 夏希结爱 32岁[MP4/4GB]</a></div>
      <div class="titletablecell titletableblue">08-18</div>
    </div>
    <div class="titletablerow">
      <div class="titletablecell titletablegreen"><a href="/amyg_1193244.html" target="_self">[dgcesd773] ★配信限定！特典映像付★神纳花的Egzu责备岬梓&amp;叶月桃一边流眼泪一边逝世！被2人责备了的神纳花也…喷水失禁一边虾翘绝顶！！[MP4/7.89GB]</a></div>
      <div class="titletablecell titletableblue">08-18</div>
    </div>
<div class="titletablerow">
      <div class="titletablecell titletablegreen"><a href="/amyg_1193243.html" target="_self">[chrv086] 认真的优等生妹妹爆乳百闻不如一见！G罩杯97cm光[MP4/6.30GB]</a></div>
      <div class="titletablecell titletableblue">08-18</div>
    </div>"""
    jpgReg2 = re.compile(r'href="(/amyg.+\.html)".+[】|>\[]([0-9a-zA-Z]+)[\s|\]]')
    next_url = re.findall(jpgReg2, str(text))
    print(next_url[0][0])
    return next_url


# rule=r'href="(/amyg.+\.html)".+[】|>\[]([0-9a-zA-Z]+)[\s|\]|\u4e00-\u9fa5]'
def get_page_urls(url, rule=r'href="(/amyg.+\.html)".+>(.+GB])'):
    page = requests.get(url, verify=False)
    # print(page.text)
    jpgReg2 = re.compile(rule)
    jpgs = re.findall(jpgReg2, str(page.text))
    results = list(set(jpgs))
    print('Page numbers: {}'.format(len(results)))

    return results


def get_magnet(url):
    page = requests.get(url, verify=False)
    # print(page.text)
    jpgReg2 = re.compile(r'(magnet.+[0-9A-Z]{30,50})')
    magnet = re.findall(jpgReg2, str(page.text))
    results = list(set(magnet))
    # print(len(results))

    return results[0]


# 主程序 输入网址拉取磁力链接
def get_magnets(url, id_dict):
    amyg_urls = get_page_urls(url)

    for i in amyg_urls:
        amyg_magnet = 'http://0341.xyz' + i[0]
        id_dict[i[1]] = get_magnet(str(amyg_magnet))
    return id_dict


def get_magnets_by_pages(start):
    id_dict = {}
    start_html = 'http://0341.xyz/qdge_39_'

    for i in range(start, start + 10):
        cur_html = start_html + str(i) + '.html'
        print("读取页面：第" + str(i) + "页")
        try:
            id_dict.update(get_magnets(cur_html, id_dict))
        except Exception as e:
            print("程序错误，最后完成页面：第" + str(i - 1) + "页")
            time.sleep(60)
    return id_dict


if __name__ == '__main__':
    # html = 'http://0341.xyz/qdge_39_4.html'
    # print(get_page_urls(html))
    # print(get_html_content(html))

    # print(get_html_content('http://0341.xyz/amyg_1193506.html'))
    # print(get_magnet('http://0341.xyz/amyg_1193506.html'))

    # id_dict = {}
    # print(get_magnets(html, id_dict))
    id_dict = {}
    with open('./magnet_saver.txt', 'a', encoding='utf-8') as f:
        for pages in range(10, 20):
            id_dict = get_magnets_by_pages(pages * 10)
            # 将dic dumps json 格式进行写入
            # f.write(json.dumps(id_dict, ensure_ascii=False))
            for key in id_dict:
                f.write(key)
                f.write('\t')
                f.write(id_dict[key])
                f.write('\n')
