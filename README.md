<h1 align="center"> Crack Captcha </h1>

[![Travis CI](https://travis-ci.org/Save404/captcha.svg?branch=master)](https://travis-ci.org/Save404/captcha)
[![license](https://img.shields.io/github/license/Save404/captcha.svg)](https://github.com/Save404/captcha/blob/master/LICENSE)

## 依赖环境  
Python 3.6

### 使用的Python库 
科学计算：numpy   
图像处理：matplotlib, Pillow  
机器学习：tensorflow  

## 安装

### 1.下载到本地  
- 点击右上方绿色按钮Download ZIP。  
- 在终端输入如下命令 **(推荐)**
```bash
git clone git@github.com:Save404/captcha.git
```

### 2.安装依赖包
```bash
cd captcha
pip install -r requirements.txt
```

## 训练
- [task1](https://github.com/Save404/captcha/tree/master/task1) ------ [四则运算验证码]

- [task2](https://github.com/Save404/captcha/tree/master/task2) ------ [英文+数字---5字符]

- [task3](https://github.com/Save404/captcha/tree/master/task3) ------ [英文+数字---4字符(干扰)]
```bash
cd [task1|task2|task3]
python train.py
```
训练完成后模型保存在当前目录的```models```文件夹中

## 识别
将待识别的验证码文件夹存放在对应的目录```(task1|task2|task3)```下，并重命名为```test```

#### 单张测试  
修改clean.py中img变量为验证码名(形如'test/0000.jpg')
```bash
./run.sh
```

#### 识别输出  
```bash
python output.py
```
输出结果保存在当前文件夹下```result.txt```中

## 文件说明
- ```data```: 验证码字体
- ```clean.py```: 去噪  
- ```gen_cap.py```: 生成验证码数据集
- ```get_cap.py```: 读取待识别的验证码
- ```image.py```: 验证码生成模块
- ```output.py```: 识别并输出识别结果至output.txt
- ```recognize.py```: 识别模块
- ```run.sh```: 用于单张识别测试
- ```train.py```: 训练模块，使用卷积神经网络CNN算法

## 算法说明
本项目主要使用卷积神经网络CNN算法进行验证码识别；  
预处理包括灰度图转化、二值化、去噪点，在三层卷积层下进行训练。
