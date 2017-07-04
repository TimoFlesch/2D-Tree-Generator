import turtle
import numpy as np
from PIL import Image, ImageEnhance

def whiteToAlpha(img):
	""" renders white background of image transparent
	 found under http://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent """
	img   = img.convert("RGBA")
	datas =       img.getdata()

	newData = []
	for item in datas:
		if item[0] > 250 and item[1] > 250 and item[2] > 250: # i.e. pixel is 'white' [changed, thresh was 100]
			newData.append((255,255,255,0)) # adds zero opacity
		else:
			newData.append(item)
	img.putdata(newData)
	return img