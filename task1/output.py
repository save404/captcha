#-*- coding: utf-8 -*-

import numpy as np 
import tensorflow as tf 
from PIL import Image
from get_cap import get_captcha_text_and_image
from train import MAX_CAPTCHA
from train import CHAR_SET_LEN
from train import X
from train import keep_prob
from train import convert_to_gray
from train import vec_to_text
from train import crack_captcha_cnn
from clean import denoise, NaiveRemoveNoise

dir_name = 'test/'

def deal(text):
	cnt = 0
	i = 0
	idx = 5
	for c in text:
		if c == '+' or c == '-' or c == '*':
			cnt += 1

		if cnt == 2:
			idx = i
			break
		i += 1

	d = 0
	for j in range(idx+1, len(text)):
		if text[j-1]!=text[j]:
			d += 1

	f = False
	if text[idx+d] == '-' or text[idx+d] == '+' or text[idx+d] == '*':
		f = True
	return text[:idx+d] if f else text[:idx+d+1]


if __name__ == '__main__':
	file = open('result.txt', 'w+')
	output = crack_captcha_cnn()

	tr = 0

	saver = tf.train.Saver()
	with tf.Session() as sess:
		saver.restore(sess, tf.train.latest_checkpoint('./models/'))

		predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
		for i in range(5000):
			idx = str('%04d' % i)
			img_name = dir_name + idx + '.jpg'
			new = denoise(img_name)
			NaiveRemoveNoise(new)
			new.save('clean.jpg')
			real, image = get_captcha_text_and_image(i, 'clean.jpg')
			image = convert_to_gray(image)
			captcha_image = image.flatten() / 255

			text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})

			text = text_list[0].tolist()
			vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)

			j = 0
			for n in text:
				vector[j * CHAR_SET_LEN + n] = 1
				j += 1

			predict_text = vec_to_text(vector)
			deal_text = deal(predict_text)

			res = 0
			try:
				res = eval(deal_text)
			except Exception as e:
				res = 0

			txt = deal_text+'='+str(res)
			if txt == real:
				tr += 1

			print('Real: {}   Predict: {}       {}    {}'.format(real, txt, tr, tr/(i+1)))
			file.write(idx + ',' + txt + '\n')


		file.close()



		