from PIL import Image
from image import ImageCaptcha

text = '1234'
image = ImageCaptcha()
captcha = image.generate(text)
img = Image.open(captcha)

img.show()