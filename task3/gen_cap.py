#-*- coding: utf-8 -*-

import random
import string
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from captcha.image import ImageCaptcha

chars = string.digits + string.ascii_lowercase + string.ascii_uppercase

#生成随机验证码文本
def random_captcha_text(char_set=chars, captcha_size=4):
	captcha_text = []
	for i in range(captcha_size):
		c = random.choice(char_set)
		captcha_text.append(c)
	return ''.join(captcha_text)

#验证码数值化
def gen_captcha_text_and_image():
	captcha_text = random_captcha_text()
	captcha = ImageCaptcha().generate(captcha_text)
	#ImageCaptcha().write(captcha_text, captcha_text + '.png')

	captcha_image = Image.open(captcha)
	captcha_image = np.array(captcha_image)

	return captcha_text, captcha_image

if __name__ == '__main__':
	text, image = gen_captcha_text_and_image()

	#原文本显示在左上角
	f = plt.figure()
	ax = f.add_subplot(111)
	ax.text(0.1, 0.9, text, ha='center', va='center', transform=ax.transAxes)

	plt.imshow(image)
	plt.show()
