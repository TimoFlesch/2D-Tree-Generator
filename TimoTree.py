"""
TimoTrees
 A generator for fairly naturalistic tree images
 in Collaboration with Ronald Dekker

 (c) Timo Flesch, 2017
 timo [dot] flesch [at] gmail [dot] com

"""
# import svgwrite

import os
import turtle
import numpy as np
import string
from PIL import Image, ImageEnhance


# define some parameters for generation of multiple trees
numTrees         = 10


class TimoTree():
	def __init__(self,
		treeColourBase       = tuple(np.divide((66.,33.,2.),255)),
		branchColourVari     =                    .08,
		stemColourVari       =                    .05,
		stemLength           =                     60,
		numStem              =                      3,
		stemWidthFactor      =                      6,
		branchAngleBase      =                      40,
		branchAngleRange     =                      25,
		branchShrinkage      =                      6,
		branchShrinkageRange =                      4,
		branchMin            =                    0.2,
		branchWidthFactor    =                      8,
		numIters             =                     20,
		leafSize             =                     10,
		leafSizeVariance     =                      0,
		leafNum              =                      8,
		leafFractionBehind   =                    .85,
		leafMinBrightness    =                    .55,
		leafMaxBrightness    =                    1.6,
		fruitSize            =                     [],
		fruitNum             =                      0,
		probaStraightBranch  =                    0.8,
		probaLeftBranch      =                    0.9,
		probaRightBranch     =                    0.9,
		probaLeaf            =                   0.1,
		probaFruit           =                      0,
		scaleFactor          =              (1/.722)):
		"""
		 tree initialiser
		"""

		# MISC
		self.scaleFactor         =         scaleFactor


		# TREE PARAMETERS
		self.branchAngleBase     =     branchAngleBase # angle child edge to parent edge
		self.branchAngleRange    =    branchAngleRange # range of possible angles
		self.treeColourBase      =      treeColourBase # colour of tree
		self.branchColourVari    =    branchColourVari # variability in colour of branches
		self.stemColourVari      =    stemColourVari # variability in colour of stem

		# stem: branches withouth leaves
		self.stemLength          =          stemLength # length of stem
		self.stemWidthFactor     =     stemWidthFactor # proportional width of stem
		self.numStem             =             numStem # number of iterations without leaves

		# branch params
		self.branchShrinkage     =     branchShrinkage # reduction in branch-size on each iteration
		self.branchShrinkageRange = branchShrinkageRange # range of rnd noise
		self.branchWidthFactor   =   branchWidthFactor # proportional width of potentially leafy branch

		# recursion anchors
		self.branchMin           =           branchMin # minimum branch length
		self.numIters            =            numIters # maximum number of iterations

		# leaf params
		self.leafSize            =            leafSize # size of leaf image
		self.leafSizeVariance    =    leafSizeVariance # variance in leaf size
		self.leafNum             =             leafNum # max Num of leaves per branch
		self.leafFractionBehind  =  leafFractionBehind # percentage of leaves that go behind tree
		self.leafMinBrightness   =  leafMinBrightness  # minimal brightness of leaves
		self.leafMaxBrightness   =  leafMaxBrightness  # maximal brightness of leaves

		self.leafCoords          =                  [] # container for leaf coordinates

		# fruit params
		self.fruitSize           =           fruitSize # avg size of fruit
		self.fruitNum            =            fruitNum # Num of fruits per branch

		# growth probabilities
		self.probaStraightBranch = probaStraightBranch # proceed with straight line
		self.probaLeftBranch     =     probaLeftBranch # branch to the left
		self.probaRightBranch    =    probaRightBranch # branch to the right
		self.probaFruit          =          probaFruit # probability of fruit growth
		self.probaLeaf           =           probaLeaf # probability of leaf growth


	def branches(self,branchLength,pen,iter,canvas):
		"""
		 this function grows a tree
		"""

		thisHeading = pen.heading() # current heading
		# recursion anchor:
		if((branchLength<self.branchMin) or (int(iter) == int(self.numIters))):
			return
		# DRAW...

		# ... either a stem,...
		if iter < self.numStem:
			# change colour slightly
			pen.pencolor(tuple(np.abs(np.add(self.treeColourBase,np.random.uniform(-self.stemColourVari,self.stemColourVari)))))
			# set width (proportional to length of branch)
			pen.width(max(0,branchLength/self.stemWidthFactor))
			# draw :)
			pen.forward(branchLength)

		# ... or a branch which might have leaves
		else:
			# change colour slightly (3d effect)
			pen.pencolor(tuple(np.abs(np.add(self.treeColourBase,np.random.uniform(-self.branchColourVari,self.branchColourVari)))))
			# set width (proportional to length of branch)
			pen.width(max(0,branchLength/self.branchWidthFactor))
			# draw in steps, save potential leaf coordinates
			thisBranchLength = 0

			for drawStep in np.repeat(branchLength/self.leafNum,self.leafNum):
				pen.forward(drawStep)
				thisBranchLength += drawStep

				# add leaf coords in probabilistic fashion
				if np.random.uniform() < self.probaLeaf:
					# add coords to my list
					self.leafCoords.append([int((.5*canvas.canvwidth+pen.xcor())/self.scaleFactor),int((.5*canvas.canvheight-pen.ycor())/self.scaleFactor)]) # centre translated



		pen.pencolor(self.treeColourBase) # back to default

		# CONTINUE with children:
		# either left branch,...
		if  np.random.uniform() <= self.probaLeftBranch:
			pen.setheading(thisHeading+self.branchAngleBase+np.random.uniform(-self.branchAngleRange,self.branchAngleRange))
			self.branches(max(0,branchLength-self.branchShrinkage+int(np.random.uniform(-self.branchShrinkageRange,self.branchShrinkageRange))),pen,iter+1,canvas)


		# ...right branch,...
		if np.random.uniform() <= self.probaRightBranch:
			pen.setheading(thisHeading-self.branchAngleBase+np.random.uniform(-self.branchAngleRange,self.branchAngleRange))
			self.branches(max(0,branchLength-self.branchShrinkage+int(np.random.uniform(-self.branchShrinkageRange,self.branchShrinkageRange))),pen,iter+1,canvas)

		# ...or just go straight
		if iter < self.numStem or np.random.uniform() <= self.probaStraightBranch:
			pen.setheading(thisHeading+np.random.uniform(-self.branchAngleRange,self.branchAngleRange))
			self.branches(max(0,branchLength-self.branchShrinkage+int(np.random.uniform(-self.branchShrinkageRange,self.branchShrinkageRange))),pen,iter+1,canvas)


		# once drawn, move pen back to start (to ensure correct branching)
		pen.setheading(thisHeading)
		pen.up()
		if iter < self.numStem:
			pen.backward(branchLength)
		else:
			pen.backward(thisBranchLength)
		pen.down()

	def leaves(self,treeIMG, branchIMG,leafIMG):
		"""
		adds some fresh leaves to my beautiful tree :)
		"""

		if self.probaLeaf == 0:
			treeIMG.paste(branchIMG,None,branchIMG)
			# showTree(treeIMG)
			return treeIMG
		else:
			# scale leaf image
			sizeNoise = np.random.uniform(-self.leafSizeVariance,self.leafSizeVariance)
			newSize = self.leafSize+sizeNoise,self.leafSize+sizeNoise
			leafIMG.thumbnail(newSize,Image.ANTIALIAS)
			# shuffle the leaf indices
			np.random.shuffle(self.leafCoords)
			leavesBehind = self.leafCoords[0:int(self.leafFractionBehind*len(self.leafCoords))]
			leavesFront = self.leafCoords[int(self.leafFractionBehind*len(self.leafCoords)):len(self.leafCoords)]

			# draw leaves that go behind tree on background
			for coordPair in leavesBehind:
				# self -explanatory
				coordPair[0] = int(coordPair[0]-leafIMG.width*.5)
				coordPair[1] = int(coordPair[1]+leafIMG.height*.5)
				thisLeaf = leafIMG.rotate(np.random.uniform(0,359))
				# leaves that go behind might be slightly darker:
				thisLeaf = ImageEnhance.Brightness(thisLeaf).enhance(np.random.uniform(self.leafMinBrightness,1))
				treeIMG.paste(thisLeaf, tuple(coordPair), thisLeaf)
			# paste tree on top
			treeIMG.paste(branchIMG,None,branchIMG)
			# draw leaves that are in front of tree
			for coordPair in leavesFront:
				# self-explanatory
				coordPair[0] = int(coordPair[0]-leafIMG.width*.5)
				coordPair[1] = int(coordPair[1]+leafIMG.height*.5)
				thisLeaf = leafIMG.rotate(np.random.uniform(0,359))
				# leaves that go in front might be slightly brighter:
				thisLeaf = ImageEnhance.Brightness(thisLeaf).enhance(np.random.uniform(1,self.leafMaxBrightness))
				treeIMG.paste(thisLeaf, tuple(coordPair), thisLeaf)

			# showTree(treeIMG)
			return treeIMG


def makeAlphabet(numTrees):
	letterSet = []
	for ii in range(numTrees):
		letterSet.append(string.ascii_lowercase[ii])
	return letterSet

def saveTree(treeIMG,bLevel,lLevel,tInstance):
	treeIMG.save(os.path.join("Trees","B"+str(bLevel)+"L"+str(lLevel)+"_"+tInstance+".png"),"PNG")
	return

def showTree(treeIMG):
	treeIMG.show()
	return


def whiteToAlpha(img):
	# renders white background of image transparent
	# found under http://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent
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


def main():
	"""
	main function, wrapper for canvas setup, tree generation and figure export
	"""

	# 1. CANVAS SETUP
	canvHeight = 610
	canvWidth  = 610
	canvas = turtle.Screen()
	canvas.setup(width  =  canvWidth,
				 height = canvHeight)
	canvas.screensize(canvwidth  =  canvWidth,
					  canvheight = canvHeight)

	canvas.colormode(1)						 # set colour mode

	# 2. TREE INSTANTIATION
	myTree = TimoTree()


	# 3. PEN SETUP
	pen = turtle.Turtle()
	pen.ht()                                 # make invisible
	pen.speed('fastest')                     # turbo turtle
	pen.shapesize(0)                         # dunno
	pen.tracer(0,0)                          # no turtle animation
	pen.up()                                 # lift pen
	pen.left(90)                             # turn by 90deg
	pen.sety((-1/5.)*canvas.screensize()[1]) # move down
	pen.pencolor(myTree.treeColourBase)      # colour of my tree
	pen.width(myTree.stemLength*.2)			 # set initial branch width
	pen.down()                               # put pen on paper


	letterSet = makeAlphabet(numTrees)

	for ii in range(numTrees):
		myTree = TimoTree(branchAngleBase     =   40,
						  branchAngleRange    =   25,
						  numIters            =   30,
						  probaRightBranch    =   .9,
						  probaLeftBranch     =   .9,
						  probaStraightBranch =   .8,
						  leafSize            =   10,
						  leafSizeVariance    =    0,
						  leafNum             =    8,
						  probaLeaf           =   .1)

		# 4. TREE GENERATION
		# first, generate some branches
		myTree.branches(myTree.stemLength,pen,0,canvas)

		# then, convert into vector graphics [eps]
		pen.getscreen().getcanvas().postscript(file = os.path.join("tmp","nudistTree.eps"))
		# clear canvas
		pen.clear()
		# load images
		branchIMG = Image.open(os.path.join("tmp","nudistTree.eps"))
		leafIMG   =   Image.open(os.path.join("Leaves","leaf4.png"))
		# enhance images, add transparent background
		# convert type
		branchIMG = branchIMG.convert("RGBA")
		leafIMG   =   leafIMG.convert("RGBA")
		# make sure that background is transparent
		branchIMG =   whiteToAlpha(branchIMG)
		leafIMG   =     whiteToAlpha(leafIMG)
		# create empty transparent background image (to put bg leaves on)
		treeIMG = Image.new("RGBA",branchIMG.size,(255,255,255,0))

		# add leaves (or not, depending on leaf proba)
		treeIMG   = myTree.leaves(treeIMG,branchIMG,leafIMG)

		saveTree(treeIMG,bLevel+1,lLevel+1,letterSet[ii])
	# close canvas
	canvas.bye()
	print "all trees generated"

# if "run XZ.py", call main
if __name__ == '__main__':
	main()
