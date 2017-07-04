import turtle


def makeCanvas(canvHeight,canvWidth):
	"""
	auxiliar function to create canvas
	"""
	canvas = turtle.Screen()
	canvas.setup(width  =  canvWidth,
				 height = canvHeight)
	canvas.screensize(canvwidth  =  canvWidth,
					  canvheight = canvHeight)

	canvas.colormode(1.)	
	#canvas.tracer(False)      # no turtle animation
	return canvas


def makePen(canvas,myTree):
	"""
	auxiliar function to create pen instance
	"""
	pen = turtle.Turtle()
	pen.ht()                                 # make invisible
	pen.speed('fastest')                     # turbo turtle
	#pen.shapesize(0)                         # dunno
	
	pen.up()                                 # lift pen
	pen.left(90)                             # turn by 90deg
	pen.sety((-1/5.)*canvas.screensize()[1]) # move down
	pen.pencolor(myTree.treeColourBase)      # colour of my tree
	pen.width(myTree.stemLength*.2)			 # set initial branch width
	pen.down()                               # put pen on paper

	return pen 