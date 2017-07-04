import string

def makeAlphabet(numTrees):
	letterSet = []
	for ii in range(numTrees):
		letterSet.append(string.ascii_lowercase[ii])
	return letterSet