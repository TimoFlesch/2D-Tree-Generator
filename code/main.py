"""
TreeGen
 A generator for fairly naturalistic tree images
 
 (c) Timo Flesch, 2017
 timo [dot] flesch [at] gmail [dot] com

"""
# external
import os
import turtle
import numpy as np
import string
from PIL import Image, ImageEnhance

# custom
from auxiliar        import imtransform
from fio.saver       import saveTree
from arbor.arbor     import TreeGen
from vincent.painter import *



def main():
	"""
	main function, wrapper for canvas setup, tree generation and figure export
	"""

	numTrees = 2 # number of consecutively generated tree images

	# 1. CANVAS SETUP
	canvHeight = 610
	canvWidth  = 610
	
	canvas = makeCanvas(canvHeight,canvWidth)

	# 2. TREE INSTANTIATION
	myTree = TreeGen()

	# 3. PEN SETUP
	pen = makePen(canvas,myTree)


	# 4. TEE GENERATOR LOOP
	for ii in range(numTrees):

		# instantiate tree with custom settings
		myTree = TreeGen(branchAngleBase     =   25, 
						  branchAngleRange    =   15,
						  numIters            =   12,
						  probaRightBranch    =   .9,
						  probaLeftBranch     =   .9,
						  probaStraightBranch =   .8,
						  leafSize            =   10,
						  leafSizeVariance    =    0,
						  leafNum             =    8,
						  probaLeaf           =   .1)


		# first, generate some branches
		myTree.branches(myTree.stemLength,pen,0,canvas)

		# then, convert into vector graphics [eps]
		pen.getscreen().getcanvas().postscript(file = os.path.join("../tmp","nudistTree.eps"))
		# clear canvas
		pen.clear()
		# load images of generated tree and a leaf
		branchIMG = Image.open(os.path.join("../tmp","nudistTree.eps"))
		leafIMG   =   Image.open(os.path.join("../Leaves","leaf4.png"))
		# enhance images, add transparent background
		# convert type
		branchIMG = branchIMG.convert("RGBA")
		leafIMG   =   leafIMG.convert("RGBA")
		# make sure that background is transparent
		branchIMG =   imtransform.whiteToAlpha(branchIMG)
		leafIMG   =     imtransform.whiteToAlpha(leafIMG)
		# create empty transparent background image (to put bg leaves on)
		treeIMG = Image.new("RGBA",branchIMG.size,(255,255,255,0))

		# add leaves (or not, depending on leaf proba)
		treeIMG   = myTree.leaves(treeIMG,branchIMG,leafIMG)

		saveTree(treeIMG,'myTree_' + str(ii))
	# close canvas
	canvas.bye()
	print("all trees generated")


if __name__ == '__main__':
	main()
