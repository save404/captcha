#-*- coding: utf-8 -*-

import numpy as np 
import tensorflow as tf 
from PIL import Image
from gen_cap import gen_captcha_text_and_image
from get_cap import get_captcha_text_and_image
from train import MAX_CAPTCHA
from train import CHAR_SET_LEN
from train import X
from train import keep_prob
from train import convert_to_gray
from train import vec_to_text
from train import crack_captcha_cnn
from clean import denoise

index = 35

def crack_captcha(captcha_image):
	output = crack_captcha_cnn()

	saver = tf.train.Saver()
	with tf.Session() as sess:
		saver.restore(sess, tf.train.latest_checkpoint('./models/'))

		predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
		text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})

		text = text_list[0].tolist()
		vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)

		i = 0
		for n in text:
			vector[i * CHAR_SET_LEN + n] = 1
			i += 1

		return vec_to_text(vector) 

if __name__ == '__main__':
	#text, image = gen_captcha_text_and_image()
	text, image = get_captcha_text_and_image(index, 'clean2.jpg')
	image = convert_to_gray(image)
	
	image = image.flatten() / 255

	predict_text = crack_captcha(image)
	print('Real: {}   Predict: {}'.format(text, predict_text))
	
