#  coding = utf-8 

# @Time : 2021/3/11 18:08
# @Author : HJH
# @File : crop_image.py
# @Software: PyCharm


from PIL import Image
import os


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print('root_dir:', root)  # 当前目录路径
        # print('sub_dirs:', dirs)  # 当前路径下所有子目录
        # print('files:', files)
        if files:
            count = 0
            for file in files:
                image_path = os.path.join(root, file)
                img = Image.open(image_path)
                # print(img.size[1])
                cropped = img.crop((0, 0, img.size[0], img.size[1] - 52))  # (left, upper, right, lower)
                cropped.save(root+'\\'+str(count)+'.jpg')
                os.remove(image_path)
                count += 1

def file_name2(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print('root_dir:', root)  # 当前目录路径
        # print('sub_dirs:', dirs)  # 当前路径下所有子目录
        # print('files:', files)
        if files:
            count = 0
            for file in files:
                image_path = os.path.join(root, file)
                if 'image' in image_path:
                    os.remove(image_path)


if __name__ == '__main__':
    dir = 'E:\\Program Files (x86)\\Python\\pc\\cat'
    file_name(dir)