#-*- coding: utf-8 -*-

import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt

def get_captcha_text_and_image(line, img_name):
	with open('train/mappings.txt', 'r') as mp:
		captcha_text = mp.readlines()[line][5:10]

	captcha_image = Image.open(img_name)
	captcha_image = np.array(captcha_image)
	return captcha_text, captcha_image

if __name__ == '__main__':
	text, image = get_captcha_text_and_image(2, 'clean2.jpg')
	print(text)
	print(image.shape)
	'''
	f = plt.figure()
	ax = f.add_subplot(111)
	ax.text(0.1, 0.9, text, ha='center', va='center', transform=ax.transAxes)
	'''
	plt.imshow(image)
	plt.show()