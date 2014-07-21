#!/usr/bin/python
# many dependencies are all brought in with this import...
from photoboothlib import *
from string import split

#=============================================================================
# ==================================  MAIN  ==================================
#=============================================================================

# lists used below...
printed = []
existing = []

# change directory to shared directory root of photo booth files...
#os.chdir('/volumes/PHOTOBOOTH')
os.chdir('/home/r14793/photobooth/')
# add filenames to existing list and sort...
#for i in os.listdir('for-display'):
#	print i,
#	if os.path.isfile('for-display/'+i): existing.append(i)
existing = os.listdir('for-display')
existing.sort()
print repr(existing)
print
filename = split(existing[-1], '_')[0]
print 'filename:', filename

while (1):

	# watch for new file in for-display
	new = False
	while not(new):
		tmp = os.listdir('for-display')
		tmp.sort()
		newest = tmp[-1]
		if newest not in existing:
			new = True # so we fall out of while loop...
			existing.append(newest)
		else:
			time.sleep(2)

	start = time.time()

	# grab the actual single strip filename, which may have a color suffix...
	tmp = os.listdir('for-phone')
	tmp.sort()
	filename = tmp[-1]
	outputfilename = split(filename, '_')[0]+'_print'
	if '-' not in filename: outputfilename = outputfilename + '.jpg'
	else: outputfilename = outputfilename + '-' + split(filename, '-')[1]
	print newest, filename, outputfilename
	
	print '\r\nCreating double print strip...'
	imPrint = Image.open('for-phone/'+filename)
	imDouble = Image.new('RGB', (4000, 6000), 'white')
	# generate double strip for printing...
	imDouble.paste( imPrint, (0, 0, 2000, 6000) )
	imDouble.paste( imPrint, (2000, 0, 4000, 6000) )
	draw = ImageDraw.Draw(imDouble)
	draw.line( (2000, 0, 2000, 6000), fill='rgb(0,0,0)', width=2)
	del draw
	imDouble.save('for-print/'+outputfilename, 'JPEG', quality=90)

	print '\r\nProcessing done: ', time.time()-start

	# send print job here...

	# then save to printed list...
	printed.append(filename)
	
	# print elapsed time to console...
	print '\r\nTotal cycle time: ', time.time()-start



