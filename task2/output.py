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

if __name__ == '__main__':
	file = open('train/output.txt', 'w+')
	output = crack_captcha_cnn()

	saver = tf.train.Saver()
	with tf.Session() as sess:
		saver.restore(sess, tf.train.latest_checkpoint('./models/'))

		predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
		for i in range(10000):
			idx = str('%04d' % i)
			img_name = 'train/' + idx + '.jpg'
			new = denoise(img_name)
			NaiveRemoveNoise(new)
			new.save('clean.jpg')
			real, image = get_captcha_text_and_image(i, 'clean.jpg')
			image = convert_to_gray(image)
			captcha_image = image.flatten() / 255

			text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})

			text = text_list[0].tolist()
			vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)

			i = 0
			for n in text:
				vector[i * CHAR_SET_LEN + n] = 1
				i += 1

			predict_text = vec_to_text(vector) 
			print('Real: {}   Predict: {}'.format(real, predict_text))
			file.write(idx + ',' + predict_text.upper() + '\n')

		file.close()



		