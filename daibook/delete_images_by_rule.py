#  coding = utf-8 

# @Time : 2021/3/15 11:50
# @Author : HJH
# @File : delete_images_by_rule.py
# @Software: PyCharm

import os


def delete_files(dir):
    for file in os.listdir(dir):
        filename = dir + '\\' + file
        fsize = os.path.getsize(filename)
        if (fsize < 15000):
            # print(fsize)
            os.remove(filename)


if __name__ == '__main__':
    dir = r'E:\Program Files (x86)\Python\pc\tieba\3097685300'
    delete_files(dir)
