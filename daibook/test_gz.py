#  coding = utf-8 

# @Time : 2021/3/7 14:30
# @Author : HJH
# @File : test_gz.py
# @Software: PyCharm

from selenium.webdriver.common.keys import Keys    #模仿键盘,操作下拉框的
from bs4 import BeautifulSoup    #解析html的
from selenium import webdriver    #模仿浏览器的
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re




def search(browser):
    try:
        # browser.get("https://www.taobao.com")
        # total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(29)")))
        target = browser.find_element_by_css_selector('body > div:nth-child(29)')
        actions = ActionChains(browser)
        actions.move_to_element(target)
        actions.perform()
    except TimeoutException:
        print("Retry")
        search(browser)

# driver = webdriver.Chrome()  # 打开浏览器
# driver.get('https://www.de5abb5b95ee.com/tupian/132953.html')  # 打开你的访问地址
#
# driver.implicitly_wait(10)
# driver.maximize_window()  # 将页面最大化
#
# driver.execute_script("window.scrollTo(0, 4000);")
# time.sleep(3)
# driver.execute_script("window.scrollTo(0, 10000);")
# time.sleep(3)
# driver.execute_script("window.scrollTo(0, 15000);")
# time.sleep(3)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# # driver.find_element_by_xpath('//input[@class="readerImg"]').send_keys(Keys.HOME)  # 下拉条置顶
# #
# # driver.find_element_by_xpath('//input[@class="readerImg"]').send_keys(Keys.DOWN)
#
# # search(driver)
#
# a = time.time()
#
# time.sleep(3)
#
# b = time.time() - a
# print(b)
#
# html = BeautifulSoup(driver.page_source, "lxml")
#
#
#
# print(html)
#
# driver.close()
