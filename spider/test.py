#  coding = utf-8 

# @Time : 2022/10/13 6:36
# @Author : HJH
# @File : test.py
# @Software: PyCharm


import scrapy
import re








if __name__ == '__main__':
    aaa = '''<td class="name">
          <a href="magnet:?xt=urn:btih:699E2316B01EF5F9D15D5C117CF95EE60207030D">
           magnet:?xt=urn:btih:699E2316B01EF5F9D15D5C117CF95EE60207030D
          </a>
          <span class="hd">
           高清
          </span>
         </td>
         <td class="action">
          <a class="copy" onclick="copyText('magnet:?xt=urn:btih:699E2316B01EF5F9D15D5C117CF95EE60207030D')">
           复制
          </a>'''

    jpg_reg = re.compile(r'a href="magnet:\?xt=urn:btih:699E2316B01EF5F9D15D5C117CF95EE60207030D">')
    jpgs = re.findall(jpg_reg, aaa)
    print(jpgs)