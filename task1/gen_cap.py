#-*- coding: utf-8 -*-

import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from image import ImageCaptcha

number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
number1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
symbol = ['+', '-', '*']
chars = number + number1 + symbol
# 生成随机验证码文本


def random_captcha_text():
	captcha_text = []

	for i in range(3):
		if i >= 1:
			captcha_text.append(random.choice(symbol));
		w = random.randint(1, 2);
		if w == 1:
			captcha_text.append(str(random.choice(number)));
		else:
			captcha_text.append(str(random.choice(number1)));
			captcha_text.append(str(random.choice(number)));
	return "".join(captcha_text)


#验证码数值化
def gen_captcha_text_and_image():
	captcha_text = random_captcha_text()
	captcha = ImageCaptcha().generate(captcha_text)
	#ImageCaptcha().write(captcha_text, captcha_text + '.png')

	captcha_image = Image.open(captcha)
	captcha_image = np.array(captcha_image)

	return captcha_text, captcha_image


if __name__ == '__main__':
	while True:
		text, image = gen_captcha_text_and_image()
		if (text.find("0") >= 0):
			print(text)
			print(image.shape)

			# 原文本显示在左上角
			f = plt.figure()
			ax = f.add_subplot(111)
			ax.text(0.1, 0.9, text, ha='center', va='center', transform=ax.transAxes)

			plt.imshow(image)
			plt.show()





