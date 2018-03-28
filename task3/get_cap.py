#-*- coding: utf-8 -*-

import numpy as np 
from PIL import Image

def reduce_size(img):
	im = img.resize((160, 60), Image.ANTIALIAS)
	return np.array(im)

def get_captcha_text_and_image(line, img_name):
	with open('train/mappings.txt', 'r') as mp:
		captcha_text = mp.readlines()[line][5:10]
	#print(captcha_text)

	captcha_image = Image.open(img_name)
	#captcha_image.show()
	#print(np.array(captcha_image).shape)
	captcha_image = reduce_size(captcha_image)
	#print(captcha_image)
	return captcha_text, captcha_image

if __name__ == '__main__':
	text, image = get_captcha_text_and_image(0, 'train/0000.jpg')
	print(text)
	print(image.shape)