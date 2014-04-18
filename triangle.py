# Python 3.x
# Triangle Generator - Triangle.py

from random import sample, getrandbits as rbit # seed, random as rand (for setting up weighted probabilities?)
import argparse
class color:
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
def docSpec():
	# add argv-related conditionals that control file specifications
	return open('triangle_%s.svg'%rbit(8),'w')

	
class tile:	# holds things relating to the cells and array layout
	def assign(posX,posY,slot): # assigns a color to a tile then purges it from color.active
		tile.array[posX][posY][slot]=sample(color.active,1)[0]	# [0] because sample returns a list. Why not 'choice' instead? Choice doesn't like non-indexable items
		color.purge(posX,posY,slot)
	def setup():	# initializes the array
		# need to input catches for invalid entries and items not greater than 0
		# BUILD VARIABLES
		tile.aWidth=int(input("Enter grid width:\n?>> "))	# set array width to input
		tile.aHeight=input("Enter grid height:\n?>> ")			# input array height input
		if tile.aHeight=='':									# if array height is blank...
			tile.aHeight=tile.aWidth							# 	set array height to array width
		else:													# else...
			tile.aHeight=int(tile.aHeight)						# 	set array height to integer
		# BUILD ARRAY
		if argv.orientation=='allUL':	# if argument states 'Make all ULLR', define array type
		 	tile.array=[[[0,None,None] for x in range(tile.aHeight)] for x in range(tile.aWidth)]
		elif argv.orientation=='allUR':	# if argument states 'Make all URLL", define array type
			tile.array=[[[1,None,None] for x in range(tile.aHeight)] for x in range(tile.aWidth)]
		else:
			tile.array=[[[rbit(1),None,None] for x in range(tile.aHeight)] for x in range(tile.aWidth)]
	def ullr(posX,posY):					# ORIENTATION 0 - ULLR
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
	def urll(posX,posY):					# ORIENTATION 1 - URLL
		upper=1
		lower=2
		left=left
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
	# INITIALIZE SYSTEM
	color.setup()		# build color list
	file=docSpec()		# set file to the name returned by docSpec
	file.write(				# write to document a comment
		'<!--\n'+				# opens a comment
		'%s\n'*len(color.master)	# build a new line for each color
		%color.master+			# fill each line with each color
		'-->\n'					# close the comment
		'<svg>')				# open SVG and write to document
	tile.setup()		# build empty array
	polyPath=(			# set the polygon write template
		'\n\t<g>\n\t\t'+	# open the group
		'<polygon points="%s,%s %s,%s %s,%s" fill="#%s"/> '*2+		# set the polygon string and duplicate it
		'\n\t</g>')			# close the group
	# RUN
	for posX in range(tile.aWidth):
		multX=argv.cellSize*posX				# set offset multiplier X
		for posY in range(tile.aHeight):
			multY=argv.cellSize*posY			# set offset multiplier Y
			color.reset()
			if tile.array[posX][posY][0]==0:		# if Orientation is ullr...
				tile.ullr(posX,posY)					# sets tile
				file.write(polyPath%(					# write to document
					multX,multY,						# 	ULLR-U xy1
					argv.cellSize+multX,multY,				# 	ULLR-U xy2
					argv.cellSize+multX,argv.cellSize+multY,	# 	ULLR-U xy3
					tile.array[posX][posY][1],			# 	ULLR-U fill
					multX,multY,						# 	ULLR-L xy1
					argv.cellSize+multX,argv.cellSize+multY,	# 	ULLR-L xy2
					multX,argv.cellSize+multY,				# 	ULLR-L xy3
					tile.array[posX][posY][2]))			# 	ULLR-L fill
			else:									# else orientation is urll...
				tile.urll(posX,posY)					# sets tile
				file.write(polyPath%(					# write to document
					multX,multY,						# 	URLL-U xy1
					argv.cellSize+multX,multY,				# 	URLL-U xy2 
					multX,argv.cellSize+multY,				# 	URLL-U xy3
					tile.array[posX][posY][1],			# 	URLL-U fill
					argv.cellSize+multX,multY,				# 	URLL-L xy1
					argv.cellSize+multX,argv.cellSize+multY,	# 	URLL-L xy2
					multX,argv.cellSize+multY,				# 	URLL-L xy3
					tile.array[posX][posY][2]))			# 	URLL-L fill
	file.write('</svg>'); file.close() # close the tag and then close the document

# initialize arguments   # arg help is section 13.3-p541 of the cookbook
	# Arguments would be arrayWidth -w, arrayHeight -h (-h is also 
	# help?), squareWidth -W, #squareHeight -H, seed -s, force
	# orientation(0-2)[0, 1, normal] -o, disable lookups(0-4)
	# [left, up, both, internl only, off completely, normal] -l, output
	# path -O, color choices -C (cant have both),
	# path to palette -p, maybe also have an option to specify a
	# document and array size, with the option to have always square
	# tiles so the document, bleeds a bit or to have it scaled a bit?
	# That'd be a complicated preference to set up, but might be
	# beneficial in the long term to learn
parser=argparse.ArgumentParser(description='Generate triangles')
# parser.add_argument(	# arg name
# 	'-list','-of','--flags',
#	dest='argv.varname',
#	action='how the info is stored'
# 	choices={'set','of','default','options'},
#	default='what is returned if argument isn't sepecified or invalid choice',
#	help='what is displayed when -h,--help is called')
parser.add_argument(	# orientation
	'-or','--orientation',
	dest='orientation',
	action='store',
	choices={'allUL','allUR','normal'},
	default='normal',
	help='Sets cell division to always be \\, /, or randomly selected.')
parser.add_argument(	# array height
	'-ah','--arrayHeight',
	dest='aHeight',
	action='store',
	default=None,
	help='Define the grid\'s height in cells')
parser.add_argument(	# array width
	'-aw','--arrayWidth',
	dest='aWidth',
	action='store',
	default=None,
	help='Define the grid\'s width in cells')
parser.add_argument(	# square size
	'-s','--size',
	dest='cellSize',
	action='store',
	default=10,
	help='Sets the edge length of the cell. Default is 10.')
	
argv=parser.parse_args()
run()
	# In order:
	# color setup
	# sets and opens file returned by docSpec()
	# writes out the file's opening info and comments out the color list
	# initializes array and its related variables, such as height and size
	# sests polypath
	# runs the generator
	# writes and closes the file