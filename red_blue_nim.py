import sys

#we do a little rounding
POSINF = 999999
NEGINF = -999999

#this class represents each possible gamestate
class statenode:

	def __init__(self, reds, blues, gamemode, nodetype, move):
		#set starting variables woohoo
		self.children = []
		self.parent = None
		self.nodetype = nodetype
		self.move = move
		self.reds = reds
		self.blues = blues
		self.gamemode = gamemode

		#make sure children are the correct type (this is for the next two if statements)
		if nodetype == "max":
			childtype = "min"
		elif nodetype == "min":
			childtype = "max"

		#as long as the node isn't terminal, give it children that represent
		#the state following each possible action. they'll also do this, so 
		#it should recursively create the entire tree. yippee!
		if (gamemode == "standard" and self.terminal() == False):
			if reds > 1:
				self.children.append(statenode(reds-2,blues,gamemode,childtype,"redtwo"))
			if blues > 1:
				self.children.append(statenode(reds,blues-2,gamemode,childtype,"bluetwo"))
			self.children.append(statenode(reds-1,blues,gamemode,childtype,"redone"))
			self.children.append(statenode(reds,blues-1,gamemode,childtype,"blueone"))
		#slightly different for misere
		if (gamemode == "misere" and self.terminal() == False):
			self.children.append(statenode(reds,blues-1,gamemode,childtype,"blueone"))
			self.children.append(statenode(reds-1,blues,gamemode,childtype,"redone"))
			if blues > 1:
				self.children.append(statenode(reds,blues-2,gamemode,childtype,"bluetwo"))
			if reds > 1:
				self.children.append(statenode(reds-2,blues,gamemode,childtype,"redtwo"))

	#is the node terminal? or does it have children
	def terminal(self):
		if (self.reds == 0 or self.blues == 0):
			return True
		else:
			return False

	#calculates the utility of TERMINAL nodes. does NOT work on nonterminal nodes.
	#(higher utility = better situation for the computer.)
	#this is not the true utility of a node with children, that is decided by
	#the actual minmax search.
	def utility(self):

		utemp = 2*self.reds + 3*self.blues
		#print(self.reds,self.blues,utemp,utemp*-1,self.nodetype)
		if self.gamemode == "standard":
			if self.nodetype == "max":
				return utemp
			elif self.nodetype == "min":
				utemp *= -1
				return utemp
		elif self.gamemode == "misere":
			if self.nodetype == "max":
				utemp *= -1
				return utemp
			elif self.nodetype == "min":
				return utemp

	#getters

	def getmove(self):
		return self.move

	def getchildren(self):
		return self.children

	def getnodetype(self):
		return self.nodetype

	def getgamemode(self):
		return self.gamemode

	#printers! solely for debugging. print either an individual node or
	#a sloppy visualization of the entire tree.

	def printnode(self):
		print(self.getmove(),self.reds,self.blues,self.utility(),str(self.nodetype))

	def printtree(self):
		print("<><><><><><><><><><><><><PRINTING TREE><><><><><><><><><><><><>") #graphic design is my passion
		self.printnode()
		print("-")
		for child in self.children:
			child.printnode()
		print("-")
		for child in self.children:
			for a in child.getchildren():
				a.printnode()
		print("-")
		for child in self.children:
			for a in child.getchildren():
				for b in a.getchildren():
					b.printnode()


	#tha big one. begins the minmax search
	def alphabetadecision(node):
		v = MaxValue(node, NEGINF, POSINF)
		for child in node.children:
			if MinValue(child, NEGINF, POSINF) == v:
				#print("FOUND IT " + str(v) + " vs " + str(MinValue(child, NEGINF, POSINF)) + " " + child.getnodetype() + " " + child.getgamemode() + " " + str(child.terminal()))
				return child.getmove()
			#else:
				#print("WHERE IS IT " + str(v) + " vs " + str(MinValue(child, NEGINF, POSINF)) + " " + child.getnodetype() + " " + child.getgamemode() + " " + str(child.terminal()))




	#the classic maxvalue and minvalue functions from minmax search.
def MaxValue(node, alpha, beta):
	#node.printnode()
	#if depth == maxdepth:
	#	return node.utility()
	if node.terminal() == True:
		#print("node terminal, utility returned(" + str(node.utility()) + ")")
		return node.utility()
	#print("maxxing")

	v = NEGINF
	#print("{")
	for child in node.getchildren():
		v = max(v, MinValue(child,alpha,beta))
		if v >= beta:
			#print("} (returned v>=beta) (" + str(v) + " >= " + str(beta) + ")")
			return v
		alpha = max(alpha,v)
	#print("} (returned v<beta) (" + str(v) + " < " + str(beta) + ")")
	return v
#143
def MinValue(node, alpha, beta):
	#node.printnode()
	#if depth == maxdepth:
	#	return node.utility()
	if node.terminal() == True:
		#print("node terminal, utility returned (" + str(node.utility()) + ")")
		return node.utility()
	#print("minning")

	v = POSINF
	#print("{")
	for child in node.getchildren():
		v = min(v, MaxValue(child,alpha,beta))
		if v <= alpha:
			#print("} (returned v<=alpha) (" + str(v) + " <= " + str(alpha) + ")")
			return v
		beta = min(beta,v)
	#print("} (returned v>alpha(" + str(v) + " > " + str(alpha) + ")")
	return v




if __name__ == '__main__':
	#if there aren't enough arguments, exit program
	if(len(sys.argv)<3):
		print("Insufficient Arguments")
		sys.exit()

	#get command line input
	red = int(sys.argv[1])
	blue = int(sys.argv[2])
	version = "standard"
	first = "computer"
	if(len(sys.argv)>3):
		version = sys.argv[3]
		if(len(sys.argv)>4):
			first = sys.argv[4]
			if(len(sys.argv)>5):
				depth = int(sys.argv[5])

	#allow  whatever spelling of misere the user uses. except misery. dont put that
	if(version in ("misere", "Misere", "misère", "Misère")):
		version = "misere"
	else:
		version = "standard"

	if first != "human" and first != "computer":
		first = "computer"


	if red<0 or blue<0:
		print("Expected positive values")
		exit()

	#this is a sloppy way to do this but, if human mode is on, give the human
	#an "extra turn", kind of
	if(first == "human"):
		print("\n[PLAYER TURN]")
		#get player move
		loopchoice = 1
		while loopchoice == 1:
			print(str(red) + " red left. " + str(blue) + " blue left.")
			print()
			print("1) Take 1 red marble\n2) Take 2 red marbles\n3) Take 1 blue marble\n4) Take 2 blue marbles")
		

			try:
				choice = int(input())
			except:
				choice = 0
			match choice:
				case 1:
					red -= 1
					loopchoice = 0
				case 2:
					if (red > 1):
						red -= 2
						loopchoice = 0
					else:
						print("Not enough marbles.")
				case 3:
					blue -= 1
					loopchoice = 0
				case 4:
					if (blue > 1):
						blue -= 2
						loopchoice = 0
					else:
						print("Not enough marbles.")
				case _:
					print("Input must be 1,2,3, or 4")
		if (red == 0 or blue == 0):
			print(str(red) + " red left. " + str(blue) + " blue left.\n")
			if(version == "misere"):
				print("You win!\n+" + str(2*red+3*blue) + " points.")
				exit()
			else:
				print("You lose!\n-" + str(2*red+3*blue) + " points.")
				exit()
	while(1):
		print("\n[COMPUTER TURN]")
		thenode = statenode(red, blue, version, "max", None)
		#run that beautiful algorithm
		move = thenode.alphabetadecision()
		print(str(red) + " red left. " + str(blue) + " blue left.\n")
		#let the computer actually take marbles, and narrate it.
		if move == "redtwo":
			print(">The Computer takes two red marbles.")
			red -= 2
		if move == "bluetwo":
			print(">The Computer takes two blue marbles.")
			blue -= 2
		if move == "redone":
			print(">The Computer takes one red marble.")
			red -= 1
		if move == "blueone":
			print(">The Computer takes one blue marble.")
			blue -= 1
		#let the computer lose if it loses
		if (red == 0 or blue == 0):
			print(str(red) + " red left. " + str(blue) + " blue left.\n")
			if(version == "misere"):
				print("Computer wins!\n+" + str(2*red+3*blue) + " points.")
				exit()
			else:
				print("Computer loses!\n-" + str(2*red+3*blue) + " points.")
				exit()



		print("\n[PLAYER TURN]")
		#get player input
		loopchoice = 1
		while loopchoice == 1:
			print(str(red) + " red left. " + str(blue) + " blue left.")
			print()
			print("1) Take 1 red marble\n2) Take 2 red marbles\n3) Take 1 blue marble\n4) Take 2 blue marbles")
		

			try:
				choice = int(input())
			except:
				choice = 0
			match choice:
				case 1:
					red -= 1
					loopchoice = 0
				case 2:
					if (red > 1):
						red -= 2
						loopchoice = 0
					else:
						print("Not enough marbles.")
				case 3:
					blue -= 1
					loopchoice = 0
				case 4:
					if (blue > 1):
						blue -= 2
						loopchoice = 0
					else:
						print("Not enough marbles.")
				case _:
					print("Input must be 1,2,3, or 4")
		#handle player loss
		if (red == 0 or blue == 0):
			print(str(red) + " red left. " + str(blue) + " blue left.\n")
			if(version == "misere"):
				print("You win!\n+" + str(2*red+3*blue) + " points.")
				exit()
			else:
				print("You lose!\n-" + str(2*red+3*blue) + " points.")
				exit()