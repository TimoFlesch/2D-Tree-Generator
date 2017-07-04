"""
main generator script
Timo Flesch, 2017
"""


import os
import turtle
import numpy as np
import string
from PIL import Image, ImageEnhance


# define some parameters for generation of multiple trees
numTrees         = 10


class TreeGen():
	def __init__(self,
		treeColourBase       = tuple((66./255,33./255,2./255)),
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
			pen.pencolor(tuple(map(float,np.abs(np.add(self.treeColourBase,
				np.random.uniform(-self.stemColourVari,self.stemColourVari))))))
			# set width (proportional to length of branch)
			pen.width(max(0,branchLength/self.stemWidthFactor))
			# draw :)
			pen.forward(branchLength)

		# ... or a branch which might have leaves
		else:
			# change colour slightly (3d effect)
			pen.pencolor(tuple(map(float,np.abs(np.add(self.treeColourBase,
				np.random.uniform(-self.branchColourVari,self.branchColourVari))))))
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
					self.leafCoords.append([int((.5*canvas.canvwidth+pen.xcor())/self.scaleFactor),
					int((.5*canvas.canvheight-pen.ycor())/self.scaleFactor)]) # centre translated



		pen.pencolor(self.treeColourBase) # back to default

		# CONTINUE with children:
		# either left branch,...
		if  np.random.uniform() <= self.probaLeftBranch:
			pen.setheading(thisHeading+self.branchAngleBase+
				np.random.uniform(-self.branchAngleRange,self.branchAngleRange))
			self.branches(max(0,branchLength-self.branchShrinkage+
				int(np.random.uniform(-self.branchShrinkageRange,
					self.branchShrinkageRange))),pen,iter+1,canvas)


		# ...right branch,...
		if np.random.uniform() <= self.probaRightBranch:
			pen.setheading(thisHeading-self.branchAngleBase+
				np.random.uniform(-self.branchAngleRange,self.branchAngleRange))
			self.branches(max(0,branchLength-self.branchShrinkage+
				int(np.random.uniform(-self.branchShrinkageRange,
					self.branchShrinkageRange))),pen,iter+1,canvas)

		# ...or just go straight
		if iter < self.numStem or np.random.uniform() <= self.probaStraightBranch:
			pen.setheading(thisHeading+
				np.random.uniform(-self.branchAngleRange,self.branchAngleRange))
			self.branches(max(0,branchLength-self.branchShrinkage+
				int(np.random.uniform(-self.branchShrinkageRange,
					self.branchShrinkageRange))),pen,iter+1,canvas)


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

			
			return treeIMG

