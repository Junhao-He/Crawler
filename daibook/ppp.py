#  coding = utf-8 

# @Time : 2021/6/7 22:14
# @Author : HJH
# @File : ppp.py
# @Software: PyCharm


import numpy as np
import math
import matplotlib.pyplot as plt
x = np.arange(0.2, 100, 0.1)
y = []
for t in x:
    y_1 = (math.log(t) +1) / t
    y.append(y_1)
plt.plot(x, y, label="sigmoid")
plt.xlabel("x")
plt.ylabel("y")
plt.ylim(0, 1)
plt.legend()
plt.show()
