#-*- coding: utf-8 -*-

import numpy as np 
from PIL import Image

def get_captcha_text_and_image():
	with open('mappings.txt', 'r') as mp:
		captcha_text = mp.readline()[5:10]
	#print(captcha_text)

	captcha_image = Image.open('0000.jpg')
	captcha_image = np.array(captcha_image)
	#print(captcha_image)
	return captcha_text, captcha_image

if __name__ == '__main__':
	text, image = get_captcha_text_and_image()
	print(text)
	print(image.shape)