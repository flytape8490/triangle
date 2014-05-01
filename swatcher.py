def ase(swatchFile):
	# the 11th character is the count of the expected number of blocks [file[0][11]), which start
	# with C001 or 0001. You're looking for items starting with 0001 and ending with C002.
	# more info here http://www.selapa.net/swatches/colors/fileformats.php#adobe_ase
	pass


def identify(path):
	swatchFile=open(path).readlines()
	if swatchFile[0][:4]=='ASEF':ase(swatchFile)	# If signature is ASEF, Adobe Swatch Exchange
	else:print('Swatch file type is not recognised.')