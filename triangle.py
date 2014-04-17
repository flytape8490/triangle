# Python 3.x
# Triangle Generator
# import argument library when we get that set up...
	# Arguments would be arrayWidth -w, !arrayHeight -h (-h is also 
	# help?), squareWidth -W, #squareHeight -H, seed -s, force
	# orientation(0-2)[0, 1, normal] -o, disable lookups(0-4)
	# [left, up, both, internl only, off completely, normal] -l, output
	# path -O, color choices -C (cant have both),
	# path to palette -p, maybe also have an option to specify a
	# document and array size, with the option to have always square
	# tiles so the document, bleeds a bit or to have it scaled a bit?
	# That'd be a complicated preference to set up, but might be
	# beneficial in the long term to learn
#import cairo http://cairographics.org/pycairo/   could be useful for making JPG or something... maybe...
from random import choice, getrandbits as rbit #, seed
class color:
	def purge(posX,posY,slot): # removes color of defined triangle from color.active
		try: color.active.remove(tile.array[posX][posY][slot])	# catches attempts to remove values not in color.list
		except ValueError: pass
	def reset():	# resets active color group to the master
		color.active=list(color.list)
	def setup():	# initializes color
		color.list=[]
		print("Please input at least four colors in standard\n3 or 6 character HEX format (excluding #).\nWhen you are complete, please enter 0.")
		while True:
			i=str(input("?> "))
			if i==str(0) or i=='':
				if len(set(color.list))>3:break	# check if >3 colors are present after stripping duplicates with set, could replace with a try/assert block? this uses fewer lines though...
				else:print("At least four colors are needed.")
			else:color.list.append(i)
		color.list=tuple(set(color.list)) # convert list to a set to strip out duplicates, then store as a tuple to speed up access ever so slightly
		color.reset()	# initialise color.active
def docSpec():
	# add argv-related conditionals that control file specifications
	return open('triangle_%s.svg'%rbit(8),'w')

class tile:	# holds things relating to the cells and array layout
	def assign(posX,posY,slot): # assigns a color to a tile then purges it from color.active
		tile.array[posX][posY][slot]=choice(color.active)
		color.purge(posX,posY,slot)
	def setup():	# initializes the array
		# need to input catches for invalid entries and items not greater than 0
		# BUILD VARIABLES
		tile.aWidth=int(input("Enter grid width:\n?>> "))	# set array width to input
		tile.aHeight=input("Enter grid height:\n?>> ")		# input array height input
		if tile.aHeight=='':								# if array height is blank...
			tile.aHeight=tile.aWidth						# 	set array height to array width
		else:												# else...
			tile.aHeight=int(tile.aHeight)					# 	set array height to integer
		tile.size=int(input("What is the size of the square, in pixels?\n?>> "))	# set the size of the square
		# BUILD ARRAY
		# if argv.orient==0
		# 	tile.array=[[[0,None,None] for x in range(tile.aHeight)] for x in range(tile.aWidth)]
		# elif argv.orient==1
		# 	tile.array=[[[1,None,None] for x in range(tile.aHeight)] for x in range(tile.aWidth)]
		# elif argv.orient==2 OR argv.orient==None
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
	file.write(					# write to document a comment
		'<!--\n'+					# opens a comment
		'%s\n'*len(color.list)		# build a new line for each color
		%color.list+				# fill each line with each color
		'-->\n'						# close the comment
		'<svg>')					# open SVG and write to document
	tile.setup()					# build empty array
	polyPath=(		# define the polygon write template
		'\n\t<g>\n\t\t'+
		'<polygon points="%s,%s %s,%s %s,%s" fill="#%s"/> '*2+
		'\n\t</g>')
	# RUN
	for posX in range(tile.aWidth):	# build and write out the array
		multX=tile.size*posX			# set offset multiplier
		for posY in range(tile.aHeight):
			multY=tile.size*posY
			color.reset() # COULD BUILD AN XLINK FOR (ULLR-(U|L)|URLL-(U|L) TO SHORTEN THE AMOUNT %s TO 3 PER ITER
			if tile.array[posX][posY][0]==0:
				tile.ullr(posX,posY)			# fills array
				file.write(polyPath%(			# write to document
					multX,multY,				# 	ULLR-U xy1
					tile.size+multX,multY,			# 	ULLR-U xy2
					tile.size+multX,tile.size+multY,	# 	ULLR-U xy3
					tile.array[posX][posY][1],	# 	ULLR-U fill
					multX,multY,				# 	ULLR-L xy1
					tile.size+multX,tile.size+multY,	# 	ULLR-L xy2
					multX,tile.size+multY,			# 	ULLR-L xy3
					tile.array[posX][posY][2]))	# 	ULLR-L fill
			else:
				tile.urll(posX,posY)			# fills array
				file.write(polyPath%(			# write to document
					multX,multY,				# 	URLL-U xy1
					tile.size+multX,multY,			# 	URLL-U xy2 
					multX,tile.size+multY,			# 	URLL-U xy3
					tile.array[posX][posY][1],	# 	URLL-U fill
					tile.size+multX,multY,			# 	URLL-L xy1
					tile.size+multX,tile.size+multY,	# 	URLL-L xy2
					multX,tile.size+multY,			# 	URLL-L xy3
					tile.array[posX][posY][2]))	# 	URLL-L fill
	file.write('</svg>')	# write to document svg element closing
	file.close()			# close document
run()
