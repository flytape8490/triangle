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
	def setup():
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
class lookup:	# holds the lookup rules
	def ullr(posX,posY):					# ORIENTATION 0 - ULLR
		if posX==0 and posY!=0: 				# if against the wall...
			tile.assign(0,posY,2) 				# 	set and purge lower
			color.purge(0,posY-1,2)				# 	look up and purge lower
			tile.assign(0,posY,1)				# 	set and purge upper
		elif posX!=0 and posY==0: 				# elif against the ceiling...
			tile.assign(posX,0,1)				# 	set and purge upper
			if tile.array[posX-1][0][0]==0:		# 	if left's orientation is ULLR...
				color.purge(posX-1,0,1)			# 		look left and purge upper
			else:color.purge(posX-1,0,2)		# 	else look left and purge lower
			tile.assign(posX,0,2)				# 	set and purge lower
		else:									# else...
			color.purge(posX,posY-1,2)			# 	look up and purge lower
			tile.assign(posX,posY,1)			# 	set and purge upper
			if tile.array[posX-1][posY][0]==0:	# 	if left's orientation is ULLR...
				color.purge(posX-1,posY,1)		# 		look left and purge upper
			else: color.purge(posX-1,posY,2)	#	else look left and purge lower
			tile.assign(posX,posY,2)			# 	set and purge lower			
	def urll(posX,posY):					# ORIENTATION 1 - URLL
		tile.assign(posX,posY,2)				# set and purge lower
		if posX==0 and posY!=0:					# if against the wall...
			color.purge(0,posY-1,2)				# 	look up and purge lower
			tile.assign(0,posY,1)				# 	set and purge lower
		elif posX!=0 and posY==0:				# elif against the ceiling...
			if tile.array[posX-1][posY][0]==0:	# 	if left's orientation is ULLR...
				color.purge(posX-1,posY,1)		# 		look left and purge upper
			else: color.purge(posX-1,posY,2)	# 	else look left and purge lower
			tile.assign(posX,posY,1)			# 	set and purge upper
		else: 									# else...
			color.purge(posX,posY-1,2)			# 	look up and purge lower
			if tile.array[posX-1][posY][0]==0:	# 	if left's orientation is ULLR...
				color.purge(posX-1,posY,1)		# 		look left and purge upper
			else: color.purge(posX-1,posY,2)	# 	else look left and purge lower
			tile.assign(posX,posY,1)			# 	set and purge upper
class tile:
	def assign(posX,posY,slot): # assigns a color to a tile then purges it from color.active
		tile.array[posX][posY][slot]=choice(color.active)
		color.purge(posX,posY,slot)
	def setup(width,height):
		tile.array=[]
		# if argv.orient==0
		# 	tile.array=[[[0,None,None] for x in range(height)] for x in range(width)]
		# elif argv.orient==1
		# 	tile.array=[[[1,None,None] for x in range(height)] for x in range(width)]
		# elif argv.orient==2 OR argv.orient==None
		tile.array=[[[rbit(1),None,None] for x in range(height)] for x in range(width)]
def run():
	# INITIALIZE VARIABLES
	color.setup()		# build color list
	file=docSpec()		# set file to the name returned by docSpec
	file.write(					# write to document a comment
		'<!--\n'+					# opens a comment
		'%s\n'*len(color.list)		# build a new line for each color
		%color.list+				# fill each line with each color
		'-->\n'						# close the comment
		'<svg>')					# open SVG and write to document
	width=int(input("Enter grid width:\n?>> ")) # set array width to input
	height=input("Enter grid height:\n?>> ")	# accept array height input
	if height=='':height=width					# if height is empty set array height to width
	else:height=int(height)						# else store input as integer
	tile.setup(width,height)					# build empty array
	polyPath=(		# define the polygon write template
		'\n\t<g>\n\t\t'+
		'<polygon points="%s,%s %s,%s %s,%s" fill="#%s"/> '*2+
		'\n\t</g>')
	# RUN
	for posX in range(width):	# build and write out the array
		multX=10*posX			# set offset multiplier
		for posY in range(height):
			multY=10*posY
			color.reset() # COULD BUILD AN XLINK FOR (ULLR-(U|L)|URLL-(U|L) TO SHORTEN THE AMOUNT %s TO 3 PER ITER
			if tile.array[posX][posY][0]==0:
				lookup.ullr(posX,posY)			# fills array
				file.write(polyPath%(			# write to document
					multX,multY,				# 	ULLR-U xy1
					10+multX,multY,				# 	ULLR-U xy2
					10+multX,10+multY,			# 	ULLR-U xy3
					tile.array[posX][posY][1],	# 	ULLR-U fill
					multX,multY,				# 	ULLR-L xy1
					10+multX,10+multY,			# 	ULLR-L xy2
					multX,10+multY,				# 	ULLR-L xy3
					tile.array[posX][posY][2]))	# 	ULLR-L fill
			else:
				lookup.urll(posX,posY)			# fills array
				file.write(polyPath%(			# write to document
					multX,multY,				# 	URLL-U xy1
					10+multX,multY,				# 	URLL-U xy2 
					multX,10+multY,				# 	URLL-U xy3
					tile.array[posX][posY][1],	# 	URLL-U fill
					10+multX,multY,				# 	URLL-L xy1
					10+multX,10+multY,			# 	URLL-L xy2
					multX,10+multY,				# 	URLL-L xy3
					tile.array[posX][posY][2]))	# 	URLL-L fill
	file.write('</svg>')	# write to document svg element closing
	file.close()			# close document
run()
