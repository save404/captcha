# coding:utf-8
from PIL import Image,ImageDraw
#import pytesseract
import os
from PIL import ImageEnhance

#tessdata_dir = '--tessdata-dir "C:\\Tesseract-OCR\\tessdata"'

#去除干扰线
im = Image.open('train/0011.jpg') # PIL库加载图片
#图像二值化
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(3)
im = im.convert('1')
data = im.getdata()
w,h = im.size


for x in range(1,w-1):
    list = []
    y=1
    while(y<h-1):
        m=y
        count = 0
        while (m<h-1 and im.getpixel((x,m))==0):#当y点是黑色的，就跳入循环来计数y点下面的黑点个数
            count=count+1
            m = m+1
        # print(count)
        if (count <=2 and count>0):#判断黑色的线条垂直宽度是否小于2px，如果小于2px就跳入循环，把他们记录到list表里
            # print(count)
            c=count
            while c>0:
                list.append(m-c)
                c=c-1

        y=y+count+1


# 去掉纵向的干扰线，把找到的黑点改成白点

    if len(list)!=0:
        # print('list content')
        i=1
        while i < len(list):
            # print(x,list[i])
            data.putpixel((x,list[i]),255)
            i=i+1

for y in range(1,h-1):
    list = []
    x=1
    while(x<w-1):
        m=x
        count = 0
        while (m<w-1 and im.getpixel((m,y))==0):#当x点是黑色的，就跳入循环来计数x点下面的黑点个数
            count=count+1
            m = m+1
        # print(count)
        if (count <=2 and count>0):#判断黑色的线条水平宽度是否小于2px，如果小于2px就跳入循环，把他们记录到list表里
            # print(count)
            c=count
            while c>0:
                list.append(m-c)
                c=c-1

        x=x+count+1


# 去掉横向的干扰线，把找到的黑点改成白点

    if len(list)!=0:
        # print('list content')
        i=1
        while i < len(list):
            # print(x,list[i])
            data.putpixel((list[i],y),255)
            i=i+1
im.save('show.jpg')

#code = pytesseract.image_to_string(image=im,config=tessdata_dir)
# print('code:'+code )
#print(code)







