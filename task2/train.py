#-*- coding: utf-8 -*-

import numpy as np 
import tensorflow as tf 
from gen_cap import gen_captcha_text_and_image
from gen_cap import chars
from get_cap import get_captcha_text_and_image

text, image = get_captcha_text_and_image(0, 'train/0000.jpg')

#text, image = gen_captcha_text_and_image()
print("Image channel: ", image.shape)

IMAGE_HEIGHT = 60
IMAGE_WIDTH = 200
MAX_CAPTCHA = len(text)
print("Length: ", MAX_CAPTCHA)

char_set = ['_']
for i in chars:
	char_set.append(i)
CHAR_SET_LEN = len(char_set)

# 图像转为灰度图像
def convert_to_gray(img):
	if len(img.shape) > 2:
		gray = np.mean(img, -1)
		return gray
	else:
		return img

# 文本转向量
def text_to_vec(text):
	text_len = len(text)
	if text_len > MAX_CAPTCHA:
		raise ValueError('Wrong length!')

	vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
	def char_to_pos(c):
		if c == '_':
			k = 62
			return k
		k = ord(c) - ord('0')
		if k > 9:
			k = ord(c) - ord('A') + 10
			if  k > 35:
				k = ord(c) - ord('a') + 36
				if k > 61:
					raise ValueError('No map char!')
		return k

	for i, c in enumerate(text):
		idx = i * CHAR_SET_LEN + char_to_pos(c)
		vector[idx] = 1

	return vector

# 向量转文本
def vec_to_text(vec):
	char_pos = vec.nonzero()[0]
	text = []
	for i, c in enumerate(char_pos):
		char_idx = c % CHAR_SET_LEN
		if char_idx < 10:
			char_code = char_idx + ord('0')
		elif char_idx < 36:
			char_code = char_idx - 10 + ord('A')
		elif char_idx < 62:
			char_code = char_idx - 36 + ord('a')
		elif char_idx == 62:
			char_code = ord('_')
		else:
			raise ValueError('Index Error!')
		text.append(chr(char_code))
	return ''.join(text)

# 生成一批captcha作为样本
def gen_next_batch(batch_size=128):
	batch_x = np.zeros([batch_size, IMAGE_HEIGHT * IMAGE_WIDTH])
	batch_y = np.zeros([batch_size, MAX_CAPTCHA * CHAR_SET_LEN])

	def wrap_gen_captcha_text_and_image():
		while True:
			text, image = gen_captcha_text_and_image()
			if image.shape == (IMAGE_HEIGHT, IMAGE_WIDTH, 3):
				return text, image

	for i in range(batch_size):
		text, image = wrap_gen_captcha_text_and_image()
		image = convert_to_gray(image)

		batch_x[i, :] = image.flatten() / 255
		batch_y[i, :] = text_to_vec(text)

	return batch_x, batch_y

#########################################################################
X = tf.placeholder(tf.float32, [None, IMAGE_HEIGHT * IMAGE_WIDTH])
Y = tf.placeholder(tf.float32, [None, MAX_CAPTCHA * CHAR_SET_LEN])
keep_prob = tf.placeholder(tf.float32)

# 定义卷积神经网络cnn
def crack_captcha_cnn(w_alpha=0.01, b_alpha=0.1):
	x = tf.reshape(X, shape=[-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])
	print(x)

	# 3个卷积层
	w_c1 = tf.Variable(w_alpha * tf.random_normal([3, 3, 1, 32]))
	b_c1 = tf.Variable(b_alpha * tf.random_normal([32]))
	conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, w_c1, strides=[1, 1, 1, 1], padding='SAME'), b_c1))
	conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
	conv1 = tf.nn.dropout(conv1, keep_prob)
	print(conv1)

	w_c2 = tf.Variable(w_alpha * tf.random_normal([3, 3, 32, 64]))
	b_c2 = tf.Variable(b_alpha * tf.random_normal([64]))
	conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, w_c2, strides=[1, 1, 1, 1], padding='SAME'), b_c2))
	conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
	conv2 = tf.nn.dropout(conv2, keep_prob)
	print(conv2)

	w_c3 = tf.Variable(w_alpha * tf.random_normal([3, 3, 64, 64]))
	b_c3 = tf.Variable(b_alpha * tf.random_normal([64]))
	conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, w_c3, strides=[1, 1, 1, 1], padding='SAME'), b_c3))
	conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
	conv3 = tf.nn.dropout(conv3, keep_prob)
	print(conv3)

	# 全连接层
	w_d = tf.Variable(w_alpha * tf.random_normal([8 * 25 * 64, 1024]))
	b_d = tf.Variable(b_alpha * tf.random_normal([1024]))
	dense = tf.reshape(conv3, [-1, w_d.get_shape().as_list()[0]])
	dense = tf.nn.relu(tf.add(tf.matmul(dense, w_d), b_d))
	dense = tf.nn.dropout(dense, keep_prob)

	w_out = tf.Variable(w_alpha * tf.random_normal([1024, MAX_CAPTCHA * CHAR_SET_LEN]))
	b_out = tf.Variable(b_alpha * tf.random_normal([MAX_CAPTCHA * CHAR_SET_LEN]))
	out = tf.add(tf.matmul(dense, w_out), b_out)

	return out

# 训练
def train_crack_captcha_cnn():
	output = crack_captcha_cnn()

	loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=Y))
	optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

	predict = tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN])
	max_idx_p = tf.argmax(predict, 2)
	l = tf.reshape(Y, [-1, MAX_CAPTCHA, CHAR_SET_LEN])
	max_idx_l = tf.argmax(l, 2)

	correct_pred = tf.equal(max_idx_p, max_idx_l)
	accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

	saver = tf.train.Saver()
	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())

		step = 0
		while True:
			batch_x, batch_y = gen_next_batch(64)
			_, loss_ = sess.run([optimizer, loss], feed_dict={X: batch_x, Y: batch_y, keep_prob: 0.75})
			print(step, loss_)

			# 每100步计算一次准确度
			if step % 100 == 0:
				batch_x_test, batch_y_test = gen_next_batch(100)
				acc = sess.run(accuracy, feed_dict={X: batch_x_test, Y: batch_y_test, keep_prob: 1.})
				print(step, acc)
				# 如果准确度够大了, 保存模型, 完成训练
				if acc > 0.99:
					saver.save(sess, "./models/crack_captcha.model", global_step=step)
					print('Training completed and the model is saved!')
					break

			step += 1

if __name__ == '__main__':
	train_crack_captcha_cnn()






























