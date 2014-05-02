# Python 3.x
# Triangle Generator -- Triangle.py

import argparse
from random import sample, getrandbits as rbit, seed # random as rand (for setting up weighted probabilities?)
def argue(): # build arguments and their parser (help is cookbook section 13.3-p541)
	parser=argparse.ArgumentParser(description='Generate triangles')
	parser.add_argument(	# -(a)rray (H)eight
		# UNIMPLEMENTED
		'-ah',
		dest='aHeight',
		metavar='Array Height',
		type=int,
		action='store',
		help='Define the grid\'s height, in cells')
	parser.add_argument(	# -(a)rray (W)idth
		# UNIMPLEMENTED
		'-aw',
		dest='aWidth',
		metavar='Array Width',
		type=int,
		action='store',
		help='Define the grid\'s width, in cells')
	parser.add_argument(	# -(c)ell size
		'-cs',
		dest='cellSize',
		metavar='Cell Size',
		type=int,
		action='store',
		default=10,
		help='Sets the edge length of a cell, in pixels. The default value is 10.')
	parser.add_argument(	# -lookup (d)isabling - UNIMPLEMENTED
		'-d',
		dest='disable',
		action='store',
		choices={'left','up','both','internal','all'},	# this could be more elegant
		help='Disable adjacency checking for specific directions. If unspecified, default behavior is to prevent adjacent color duplication.')
	parser.add_argument(	# -svg (d)ocument (h)eight
		'-dh',
		dest='dHeight',
		metavar='Document Height',
		action='store',
		type=int,
		default=100,
		help='Sets the height of the SVG document. The default value is 100.')
	parser.add_argument(	# -svg (d)ocument (w)idth
		'-dw',
		dest='dWidth',
		metavar='Document Width',
		action='store',
		type=int,
		default=100,
		help='Sets the width of the SVG document. The default value is 100.')
	parser.add_argument(	# -(f)ile (n)ame
		'-fn',
		dest='fileName',
		metavar='File Name',
		action='store',
		help='Sets the file name. Default name is triangle_(random number).svg. File is saved to either your home directory or the directory from which this was ran.')
	parser.add_argument(	# -o(r)ientation
		'-r',
		dest='orientation',
		metavar='oRientation',
		action='store',
		choices={'ul','ur'},
		help='Accepts ul and ur as arguments. Sets cell division to always be either \\ or /, respectively. Tthe default action is to randomly apply orientation.')
	# parser.add_argument() # -(p)ath: palette file location (if !=none, run palette interp function)
	# parser.add_argument() # -(svgz): action='store_true' : causes file to be converted to an svgz on close.
	parser.add_argument(	# -(s)eed
		'-s',
		dest='seed',
		metavar=' Seed Value',
		action='store',
		help='Sets the seed value. The default action is to have the system determine the seed.')
	# parser.add_argument() # -(w)eighted: action='store_true' : turns on weighted layout if called.
	global argv				# set the parser as a global item
	argv=parser.parse_args()# make the parser
class color: # holds color functions
	def purge(posX,posY,slot):	# removes color of defined triangle from color.active
		try: color.active.remove(tile.array[posX][posY][slot])	# attempts to remove values not in color.master
		except KeyError: pass
	def reset(): color.active=set(color.master) # initializes color.active by copying color.master as a set
	def setup():				# initializes color.master
		color.master=set({})	# build empty set (set doesn't support duplicates)
		print(	# not a """ string because those preserve whitespace. Split into separate lines anyway because of readability
			'Please input at least four colors in standard\n'
			'3 or 6 character HEX format (excluding #).\n'
			'When you are complete, please enter 0.')
		while True:							# start the input loop
			i=input('?>> ')						# input string
			if i==str(0) or i=='':				# if input is 0 or blank...
				if len(color.master)>=4: break	# 	if master has at least 4 items, exit loop
				else: print('At least four colors are needed.')	# 	else, alert too few colors
			else: color.master.add(i)			# else, add the color to the master
		color.master=tuple(color.master)	# store color.master as a tuple
		color.reset()						# initialise color.active
def docSpec(): # opens file
	if argv.fileName==None:	return open('triangle_%s.svg'%rbit(5),'w')
	else: return open(argv.fileName+'.svg','w')
class tile:	# holds tile, lookup, and array generation functions
	def assign(posX,posY,slot): # assigns a color to a tile then purges it from color.active
		tile.array[posX][posY][slot]=sample(color.active,1)[0]	# [0] because sample returns a list. Why not 'choice' instead? Choice doesn't like non-indexable items (sets)
		color.purge(posX,posY,slot)
	def setup(): # initializes the array variables
		# SET WIDTH
		try:
			if argv.aWidth==None: argv.aWidth=int(input('Enter array width:\n?>> '))	# if argv.aWidth is None, enter a value
			if argv.aWidth<=1:
				quit('SizeError: array Width is less than 1')
		except ValueError:
			quit('ValueError: Invalid entry for array width.')
		# SET HEIGHT
		try:
			if argv.aHeight==None: argv.aHeight=int(input('Enter array height:\n?>> '))
			if argv.aHeight<=1:
				quit('SizeError: array height is less than 1')
		except ValueError:
			quit('ValueError: Invalid entry for array height')
		# SET-UP ARRAY
		if argv.orientation=='ul':								# if argv.orientation=='ul'... set array with ULLR orientation
		 	tile.array=[[[0,None,None] for x in range(argv.aHeight)] for x in range(argv.aWidth)]
		elif argv.orientation=='ur':							# if argv.orientation=='ur'... set array with URLL orientation
			tile.array=[[[1,None,None] for x in range(argv.aHeight)] for x in range(argv.aWidth)]
		else:													# else... set array with normal orientation
			if argv.seed!=None: seed(argv.seed)					# if argv.seed specified, reset seed
			tile.array=[[[rbit(1),None,None] for x in range(argv.aHeight)] for x in range(argv.aWidth)]
	def ullr(posX,posY): # lookup rules r=ULLR
		left=posX-1
		up=posY-1
		if posX==0 and posY!=0: 		# if against the wall... (also assigns for r0-0,0)
			tile.assign(0,posY,2)			# 	set and purge lower
			color.purge(0,up,2)				# 	look up and purge uLower
			tile.assign(0,posY,1)			# 	set and purge Upper
		elif posX!=0 and posY==0: 			# elif against the ceiling...
			tile.assign(posX,0,1)			# 	set and purge Upper
			if tile.array[left][0][0]==0:	# 	if left's orientation is ULLR...
				color.purge(left,0,1)		# 		look left and purge lUpperlL
			else:color.purge(left,0,2)		# 	else look left and purge lLower
			tile.assign(posX,0,2)			# 	set and purge lower
		else:								# else neither against wall or ceiling...
			color.purge(posX,up,2)			# 	look up and purge uLower
			tile.assign(posX,posY,1)		# 	set and purge upper
			if tile.array[left][posY][0]==0:# 	if left's orientation is ULLR...
				color.purge(left,posY,1)	# 		look left and purge lUpper
			else: color.purge(left,posY,2)	#	else look left and purge lLower
			tile.assign(posX,posY,2)		# 	set and purge lower
	def urll(posX,posY): # lookup rules r=URLL
		left=posX-1
		up=posY-1
		tile.assign(posX,posY,2)			# set and purge lower
		if posX==0 and posY!=0:				# if against the wall... (also assigns for r1-0,0)
			color.purge(0,up,2)				# 	look up and purge uLower
			tile.assign(0,posY,1)			# 	set and purge upper
		elif posX!=0 and posY==0:			# elif against the ceiling...
			if tile.array[left][posY][0]==0:# 	if left's orientation is ULLR...
				color.purge(left,posY,1)	# 		look left and purge lUpper
			else: color.purge(left,posY,2)	# 	else look left and purge lLower
			tile.assign(posX,posY,1)		# 	set and purge upper
		else: 								# else against neither wall or ceiling...
			color.purge(posX,up,2)			# 	look up and purge uLower
			if tile.array[left][posY][0]==0:# 	if left's orientation is ULLR...
				color.purge(left,posY,1)	# 		look left and purge lUpper
			else: color.purge(left,posY,2)	# 	else look left and purge lLower
			tile.assign(posX,posY,1)		# 	set and purge upper
def run(): # actually builds and writes the array
	polyPath=(													# set the polygon write template
		'\n\t<g>\n\t\t'+										# 	open group tag
		'<polygon points="%s,%s %s,%s %s,%s" fill="#%s"/> '*2+	# 	set up two polygon tags with format slots
		'\n\t</g>')												# 	close group tag
	file.write(				# build SVG tag, comment the color list
		'<svg '+				# 	open SVG tag
		'width="%s" '			#		sets width, with format slot
		'height="%s"\n\t'		#		sets height, with format slot
		%(argv.dWidth, argv.dHeight)+# 	applies format
		'xmlns="http://www.w3.org/2000/svg">\n'# writes out the xmlns and ends the svg tag
		'<!--\n'+				# 	opens a comment tag
		'%s\n'*len(color.master)# 	build a new line for each color, with format slots
			%color.master+		# 		fill the format slots
		'-->\n')				# 	close the comment tag, write line to document
	if argv.seed!=None: seed(argv.seed)	# if argv.seed specified, reset seed
	for posX in range(argv.aWidth):
		multX=argv.cellSize*posX			# set offset multiplier X
		for posY in range(argv.aHeight):
			multY=argv.cellSize*posY		# set offset multiplier Y
			color.reset()
			if tile.array[posX][posY][0]==0:				# if orientation is ullr...
				tile.ullr(posX,posY)							# sets tile
				file.write(polyPath%(							# write to document...
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
				file.write(polyPath%(							# write to document...
					multX,multY,								# 	URLL-U xy1
					argv.cellSize+multX,multY,					# 	URLL-U xy2
					multX,argv.cellSize+multY,					# 	URLL-U xy3
					tile.array[posX][posY][1],					# 	URLL-U fill
					argv.cellSize+multX,multY,					# 	URLL-L xy1
					argv.cellSize+multX,argv.cellSize+multY,	# 	URLL-L xy2
					multX,argv.cellSize+multY,					# 	URLL-L xy3
					tile.array[posX][posY][2]))					# 	URLL-L fill
	file.write('</svg>'); file.close() # close the svg tag and then close the document
# --RUN ON STARTUP BELOW HERE--
argue()				# accept/parse any arguments, makes the argv object global and fills it
tile.setup()		# set up all dimensional variables, build array
color.setup()		# build color lists
file=docSpec()		# open a file for writing
run()				# start the builder
# TO DO LIST:
#	Move to SVG symbols, see if it runs faster or makes smaller files
# 	Build and implement cell scaling arguments and argument priority overrides
# 	Build and implement array offset positioning (don't start at 0,0 for instance, to allow for bleeds)
#	Implement document size argv
#	Clean-up choices for and implement lookup disabling
# 	Build and implement -s(c)ale, which would override any cell size flags and force the grid to scale to the document size. Ignored if docwidth and height aren't specified. 3 modes Off (default), Square, which scales to the largest square -aw and -ah will fit, then centers the array, and Aspect, which scales -to aw and -ah independently
#	Write palette parser
#	Build and implement Palette path argv
#	Add a -svgz argv to make it a .svgz
#	Validate color input items hexPat=re.compile('((\d|[a-f]){3}){,2}',re.I)
#	could make this whole thing tileable by adding right wall and floor lookup events