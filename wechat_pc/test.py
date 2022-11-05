#  coding = utf-8 

# @Time : 2021/2/22 15:24
# @Author : HJH
# @File : test.py
# @Software: PyCharm

import re

# x = "my precious"
# dami = [x for x in 'ABC']
# print(x)
# print(dami)
# a, b, *rest = range(5)
# print(a, b, rest)

# a = lambda i : sum(x for x in range(i))
# b = a(100)
# print(b)

# a = [1, 1, 1, 2, 2, 3, 4, 4, 4]
# print([x for x in set(a)])


ttt = r'a href="/tupian/22222.html" target=a href="/meinv/1111111.html" target='
jpg_reg = re.compile(r'a href="/(?:meinv|tupian)/(\d+)\.html" target=')
jpgs = re.findall(jpg_reg, ttt)
print(jpgs)
