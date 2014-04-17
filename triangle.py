#Python 3x
from random import choice, getrandbits as rbit
#import xml	-----not sure if would help with writing the SVG
#import argument library when we get that set up
	#Arguments would be arrayWidth -w, !arrayHeight -h (-h is also 
	#help?), squareWidth -W, #squareHeight -H, seed -s, force
	#orientation(0-2)[0,1,!random] -o, disable lookups(0-4)
	#[left, up, same cell, both adj., all 3, normal] -l, output
	#path -O, color count -c |color choices -C (cant have both),
	#path to palette -p ,maybe also have an option to specify a
	#document and array size, with the option to have always square
	#tiles so the document, bleeds a bit or to have it scaled a bit?
	#That'd be a complicated preference to set up, but might be
	#beneficial in the long term to learn
class tile:
	def assign(posX,posY,slot): #assigns a color to a tile then purges it from active
		tile.array[posX][posY][slot]=choice(color.active)
		color.purge(posX,posY,slot)
class color:
	def setup():#put a thing that removes duplicates. put a thing in if a number isn't 6 hex characters (might need RE)
		l=[]
		print("Please input your colors in 6-character HEX format. \nWhen you are complete, please enter 0.")
		while True:
			i=str(input("?> "))
			if i==str(0) or i=='':break
			else:l.append(i)
		color.list=tuple(l)
		del i,l
	def reset():
		color.active=list(color.list)
	def purge(posX,posY,slot): #removes color of defined triangle from active list, use math when calling
		try: color.active.remove(tile.array[posX][posY][slot])
		except ValueError: pass
class lookup:	#holds the lookup rules
	#left=True	#used for argument rule augmentations, might not need depending on how i eventually set up the arguments
	#up=True	#used for argument rule augmentations, might not need depending on how i eventually set up the arguments
	#same=True	#used for argument rule augmentations, might not need depending on how i eventually set up the arguments
				#the arguments *could* be:  disable lookups left -l, disable lookup up -u, disable lookup internal -i
	def ullr(posX,posY):#ORIENTATION 0
		if posX==0 and posY!=0: #if against the wall...
			tile.assign(0,posY,2) #set and purge lower - no need for lookup
			color.purge(0,posY-1,2) #purge lookUP
			tile.assign(0,posY,1) #set and purge upper
		elif posX!=0 and posY==0: #elif against the ceiling...
			tile.assign(posX,0,1)#set and purge upper - no need for lookup
			if tile.array[posX-1][0][0]==0: color.purge(posX-1,0,1)#if left==r0, purge left1
			else: color.purge(posX-1,0,2)#else purge left2
			tile.assign(posX,0,2)#set and purge lower
		else:
			color.purge(posX,posY-1,2)#purge lookUP
			tile.assign(posX,posY,1)#set and purge upper
			if tile.array[posX-1][posY][0]==0: color.purge(posX-1,posY,1)#if left==r0, purge left1
			else: color.purge(posX-1,posY,2)#else purge left2
			tile.assign(posX,posY,2)#set and purge lower			
	def urll(posX,posY):
		tile.assign(posX,posY,2) #set and purge lower, no need to check - never bordering
		if posX==0 and posY!=0: #if against the wall...
			color.purge(0,posY-1,2)#purge lookUP lower
			tile.assign(0,posY,1) #set and purge upper
		elif posX!=0 and posY==0:#if against the ceiling
			if tile.array[posX-1][posY][0]==0:color.purge(posX-1,posY,1) #if left==r0, purge left 1
			else: color.purge(posX-1,posY,2)#else purge left2
			tile.assign(posX,posY,1)#set upper
		else: 
			color.purge(posX,posY-1,2)#lookUp
			if tile.array[posX-1][posY][0]==0:color.purge(posX-1,posY,1) #if left==r0, purge left 1
			else: color.purge(posX-1,posY,2)#else purge left2
			tile.assign(posX,posY,1)#set upper
def run():
	# INITIALIZE
	# setup color list as per arguments
	# if no color arguments, accept input
	color.setup()#!!!!!!!!!!!!!!!!!!!!! put color setup inside a try. RAISE an exception if len(color.list) is <=3. Delete color.list, print("Please enter more than four colors.") and re-call color.setup()
	# setup document info as per arguments
	# setup lookup rules as per arguments (maybe?)
	# generate an array based on orientation arguments
	# if argv width=something: width=something
	#else:
	width=int(input("Enter width:\n?>> "))#REPLACE with arg logic
	height=input("Enter height:\n?>> ")#REPLACE with arg logic
	if height=='':height=width
	else:height=int(height)
	file=open('triangle_%s.html'%rbit(5),'w') #REPLACE with previous commented line once argvs 
	print("Please wait while we write your file.")
	#if argv orientation==0: tile.array=[[[0,0,0] for x in range(height)] for x in range(width)]
	#elif argv orientation==1: tile.array=[[[1,0,0] for x in range(height)] for x in range(width)]
	#else: orientation set random:
	print("Initialising array")
	tile.array=[[[rbit(1),0,0] for x in range(height)] for x in range(width)] #generates tile.array if argv orientation=random
	#RUN
	#set origin
	color.reset()
	tile.assign(0,0,1) #set and purge upper color
	tile.assign(0,0,2) #set and purge lower color
	#start rest of the array
	for posX in range(width):
		print("Selecting squares: %s%s complete"%(int(posX/width*100),'%'))
		for posY in range(height):
			color.reset()
			if tile.array[posX][posY][0]==0: lookup.ullr(posX,posY)
			else: lookup.urll(posX,posY)
	writer(width,height,file)
def writer(width,height,file):	#writes the SVG document docWidth and docHeight will eventually be replaced by grabs from the
	#note that the SVG document 0,0 is at the upper left
	#set path to (triangle.svg|(argvpath)triangle.svg|(arg_path+filename))
	#file=open(r'%s' % path,'w')	once path gets set up
	for i in color.list:file.write('<li>%s</li>\n'%(i))
	file.write('<svg>\n')
	for posY in range(height):
		for posX in range(width):
#			file.write('\n\t<g>')
			if tile.array[posX][posY][0]:#if URLL
				file.write('\t\t<polygon points="%s,%s %s,%s %s,%s" fill="%s"/>'%(10*posX,10*posY,10+(10*posX),10*posY,10*posX,10+(10*posY),tile.array[posX][posY][1]))
				file.write('<polygon points="%s,%s %s,%s %s,%s" fill="%s"/>\n'%(10+(10*posX),10*posY,10+(10*posX),10+(10*posY),10*posX,10+(10*posY),tile.array[posX][posY][2]))
			else: #if ULLR
				file.write('\t\t<polygon points="%s,%s %s,%s %s,%s" fill="%s"/>'%(10*posX,10*posY,10+(10*posX),10*posY,10+(10*posX),10+(10*posY),tile.array[posX][posY][1]))
				file.write('<polygon points="%s,%s %s,%s %s,%s" fill="%s"/>\n'%(10*posX,10*posY,10+(10*posX),10+(10*posY),10*posX,10+(10*posY),tile.array[posX][posY][2]))
#			file.write('\n\t</g>')
	#write svg header with dimensions
	#could i group two items together?
	#<polygon points="x,y x2,y2 x3,y3" style="fill:COLOR;" />
	#could also use xlink - define boundaries but not the fills of a shape
	#<defs>
	#<g id="(lU|lL|rU|rL)"> #one lU lL are ullr's upper and lower triangles, respectively. rU and rL are urll's upper and lower triangles, respectively
	#	<path points="x1,y1 x2,y2 x3,y3" stroke="none" />
	#</g>
	#</defs>
	#<g id="array">
	#	<use id="x,y,(U|L)" xlink:href="#(lU|lL|rU|rL)" x="(xPos UL point)" y="(yPos UL point)" fill="#(fill)" />
	#</g>
	#add a function that makes large files into .svgz?
	file.write('</svg>')
	file.close()
	print("Done!")
run()