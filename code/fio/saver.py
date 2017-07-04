import os
import numpy as np
from PIL import Image, ImageEnhance


def saveTree(treeIMG,tName):
	treeIMG.save(os.path.join("Trees",tInstance+".png"),"PNG")
	return