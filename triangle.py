# Python 3.x
# Triangle Generator - Triangle.py

from random import sample, getrandbits as rbit, seed #random as rand (for setting up weighted probabilities?)
import argparse
class color: # holds color functions
	def purge(posX,posY,slot):	# removes color of defined triangle from color.active
		try: color.active.remove(tile.array[posX][posY][slot])	# attempts to remove values not in color.master
		except KeyError: pass
	def reset():				# (re)initializes color.active
		color.active=set(color.master)
	def setup():				# initializes color.master
		color.master=set({})
		print(
			"Please input at least four colors in standard\n"
			"3 or 6 character HEX format (excluding #).\n"
			"When you are complete, please enter 0.")
		while True:
			i=str(input("?> "))
			if i==str(0) or i=='':
				if len(color.master)>3: break	# if more than 3 colors present, stop input
				else: print("At least four colors are needed.")	# else, alert and force continuation
			else:
				color.master.add(i)
		color.master=tuple(color.master) # store as a tuple
		color.reset()	# initialise color.active
def docSpec(): # opens file
	return open('triangle.svg','w')
class tile:	# holds tile and array functions
	def assign(posX,posY,slot): # assigns a color to a tile then purges it from color.active
		tile.array[posX][posY][slot]=sample(color.active,1)[0]	# [0] because sample returns a list. Why not 'choice' instead? Choice doesn't like non-indexable items
		color.purge(posX,posY,slot)
	def setup(): # initializes the tile variables and array
		if argv.aWidth!=None: tile.aWidth=argv.aWidth			# if argv.aWidth specified, set aWidth
		else:tile.aWidth=int(input("Enter grid width:\n?>> "))	# else set aWidth to input
		if argv.aHeight!=None: tile.aHeight=argv.aHeight		# if argv.aHeight specified, set aHeight
		else:tile.aHeight=int(input("Enter grid height:\n?>> "))# else, set aHeight to input
		# SET-UP ARRAY
		if argv.orientation=='ul':								# if argv.orientation=='ul'... set array with ULLR orientation
		 	tile.array=[[[0,None,None] for x in range(tile.aHeight)] for x in range(tile.aWidth)]
		elif argv.orientation=='ur':							# if argv.orientation=='ur'... set array with URLL orientation
			tile.array=[[[1,None,None] for x in range(tile.aHeight)] for x in range(tile.aWidth)]
		else:													# else... set array with normal orientation
			tile.array=[[[rbit(1),None,None] for x in range(tile.aHeight)] for x in range(tile.aWidth)]
	def ullr(posX,posY):					# LOOKUP RULES - ULLR
		upper=1
		lower=2
		left=posX-1
		up=posY-1
		if posX==0 and posY!=0: 				# if against the wall...
			tile.assign(0,posY,lower)			# 	set and purge lower
			color.purge(0,up,lower)				# 	look up and purge uLower
			tile.assign(0,posY,upper)			# 	set and purge upper
		elif posX!=0 and posY==0: 				# elif against the ceiling...
			tile.assign(posX,0,upper)			# 	set and purge upper
			if tile.array[left][0][0]==0:		# 	if left's orientation is ULLR...
				color.purge(left,0,upper)		# 		look left and purge lUpper
			else:color.purge(left,0,lower)		# 	else look left and purge lLower
			tile.assign(posX,0,lower)			# 	set and purge lower
		else:									# else neither against wall or ceiling...
			color.purge(posX,up,lower)			# 	look up and purge uLower
			tile.assign(posX,posY,upper)		# 	set and purge upper
			if tile.array[left][posY][0]==0:	# 	if left's orientation is ULLR...
				color.purge(left,posY,upper)	# 		look left and purge lUpper
			else: color.purge(left,posY,lower)	#	else look left and purge lLower
			tile.assign(posX,posY,2)			# 	set and purge lower
	def urll(posX,posY):					# LOOKUP RULES - URLL
		upper=1
		lower=2
		left=posX-1
		up=posY-1
		tile.assign(posX,posY,lower)			# set and purge lower
		if posX==0 and posY!=0:					# if against the wall...
			color.purge(0,up,lower)				# 	look up and purge uLower
			tile.assign(0,posY,upper)			# 	set and purge upper
		elif posX!=0 and posY==0:				# elif against the ceiling...
			if tile.array[left][posY][0]==0:	# 	if left's orientation is ULLR...
				color.purge(left,posY,upper)	# 		look left and purge lUpper
			else: color.purge(left,posY,lower)	# 	else look left and purge lLower
			tile.assign(posX,posY,upper)		# 	set and purge upper
		else: 									# else against neither wall or ceiling...
			color.purge(posX,up,lower)			# 	look up and purge uLower
			if tile.array[left][posY][0]==0:	# 	if left's orientation is ULLR...
				color.purge(left,posY,upper)	# 		look left and purge lUpper
			else: color.purge(left,posY,lower)	# 	else look left and purge lLower
			tile.assign(posX,posY,upper)		# 	set and purge upper
def run():
	for posX in range(tile.aWidth):
		multX=argv.cellSize*posX				# set offset multiplier X
		for posY in range(tile.aHeight):
			multY=argv.cellSize*posY			# set offset multiplier Y
			color.reset()
			if tile.array[posX][posY][0]==0:				# if Orientation is ullr...
				tile.ullr(posX,posY)							# sets tile
				file.write(polyPath%(							# write to document
					multX,multY,								# 	ULLR-U xy1
					argv.cellSize+multX,multY,					# 	ULLR-U xy2
					argv.cellSize+multX,argv.cellSize+multY,	# 	ULLR-U xy3
					tile.array[posX][posY][1],					# 	ULLR-U fill
					multX,multY,								# 	ULLR-L xy1
					argv.cellSize+multX,argv.cellSize+multY,	# 	ULLR-L xy2
					multX,argv.cellSize+multY,					# 	ULLR-L xy3
					tile.array[posX][posY][2]))					# 	ULLR-L fill
			else:											# else orientation is urll...
				tile.urll(posX,posY)							# sets tile
				file.write(polyPath%(							# write to document
					multX,multY,								# 	URLL-U xy1
					argv.cellSize+multX,multY,					# 	URLL-U xy2
					multX,argv.cellSize+multY,					# 	URLL-U xy3
					tile.array[posX][posY][1],					# 	URLL-U fill
					argv.cellSize+multX,multY,					# 	URLL-L xy1
					argv.cellSize+multX,argv.cellSize+multY,	# 	URLL-L xy2
					multX,argv.cellSize+multY,					# 	URLL-L xy3
					tile.array[posX][posY][2]))					# 	URLL-L fill
	file.write('</svg>'); file.close() # close the tag and then close the document

# RUN IMMEDIATELY

# INITIALIZE ARGUMENTS (help is cookbook section 13.3-p541)
parser=argparse.ArgumentParser(description='Generate triangles')
parser.add_argument(	# -(OR)ientation
	'-or',
	dest='orientation',
	metavar='ORientation',
	action='store',
	choices={'ul','ur'},
	help='Sets cell division to always be either \\ or /. If unspecified, the default action is to randomly apply orientation.')
parser.add_argument(	# -(A)rray (H)eight
	# UNIMPLEMENTED
	'-ah',
	dest='aHeight',
	metavar='Array Height',
	type=int,
	action='store',
	help='Define the grid\'s height, in cells')
parser.add_argument(	# -(A)rray (W)idth
	# UNIMPLEMENTED
	'-aw',
	dest='aWidth',
	metavar='Array Width',
	type=int,
	action='store',
	help='Define the grid\'s width, in cells')
parser.add_argument(	# -(C)ell size
	'-cs',
	dest='cellSize',
	metavar='Cell Size',
	type=int,
	action='store',
	default=10,
	help='Sets the edge length of a cell, in pixels. The default value is 10.')
parser.add_argument(	# -(S)eed
	'-s',
	dest='seed',
	action='store',
	help='Sets the seed value. If omitted, the seed is set by the system randomly. This can accept strings.'
	)
parser.add_argument(	# -lookup (D)isabling - UNIMPLEMENTED
	'-d',
	dest='disable',
	action='store',
	choices={'left','up','both','internal','all'},
	help='Disable adjacency checking for specific directions. If unspecified, default behavior is to prevent adjacent color duplication.')
# parser.add_argument()	# -(F)ile (N)ame: default file name is triangle.svg
# parser.add_argument() # -(P)ath: palette file location (if !=none, run palette interp function)
# parser.add_argument() # -(W)eighted: action='store_true' : turns on weighted layout if called.
argv=parser.parse_args()
# INITIALIZE SYSTEM
if argv.seed!=None:seed(argv.seed)	# if argv.seed specified, set seed
file=docSpec()						# set file to the name returned by docSpec
color.setup()						# build color list
tile.setup()						# build empty array
file.write(							# write a comment to the document and open the SVG tag
	'<!--\n'+						# 	opens a comment
	'%s\n'*len(color.master)		# 	build a new line for each color
	%color.master+					# 	fill each line with each color
	'-->\n'							# 	close the comment
	'<svg>')						# 	open SVG and write to document
polyPath=(							# set the polygon write template
	'\n\t<g>\n\t\t'+				# 	open object group
									# 	set the polygon string and duplicate it
	'<polygon points="%s,%s %s,%s %s,%s" fill="#%s"/> '*2+
	'\n\t</g>')						# 	close object group
run()

# TO DO LIST:
#	Build and implement file naming argv
#	Wrap width and height manual inputs in TRY functions to catch non-integer/lessthan1 inputs
#	Implement lookup disabling
#	Validate color input items
#	Figure out best where to reset the random state for when seed is specified
#	Build proper SVG structure
#	Move to SVG symbols
#	Build and implement document size argv
#	if two args can't both be active together, "if argv.a!=None and argv.b!=None:print("Fatal Error: Cannot have A/B both called"); end"
#	Write palette parser
#	Build and implement Palette path argv
#	File compression? Multithreading?