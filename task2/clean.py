#-*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageEnhance

def denoise(img):
    im = Image.open(img)
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(3)
    im = im.convert('1')
    data = im.getdata()
    w, h = im.size

    for x in range(1, w-1):
        l = []
        y = 1
        while(y < h-1):
            m = y
            count = 0
            while(m < h-1 and im.getpixel((x, m)) == 0):
                count = count + 1
                m = m + 1

            if(count <= 2 and count > 0):
                c = count
                while c > 0:
                    l.append(m - c)
                    c = c - 1

            y = y + count + 1

        if len(l) != 0:
            i = 1
            while i < len(l):
                data.putpixel((x, l[i]), 255)
                i = i + 1

    for y in range(1, h-1):
        l = []
        x = 1
        while(x < w-1):
            m = x
            count = 0
            while(m < w-1 and im.getpixel((m, y)) == 0):
                count = count + 1
                m = m + 1

            if(count <= 2 and count > 0):
                c = count
                while c > 0:
                    l.append(m - c)
                    c = c - 1

            x = x + count + 1

        if len(l) != 0:
            i = 1
            while i < len(l):
                data.putpixel((l[i], y), 255)
                i = i + 1

    return im

if __name__ == '__main__':
    img = 'train/0030.jpg'
    new = denoise(img)
    new.save('clean.jpg')




