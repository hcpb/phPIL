#!/usr/bin/python
# many dependencies are all brought in with this import...
from photoboothlib import *


#=============================================================================
# ==================================  MAIN  ==================================
#=============================================================================

# list of already printed files...
printed = []

# change directory to shared directory root of photo booth files...

while (1):

	# watch for new file in for-display
	#   something here...
	# then grab same numbered file in for-phone 
	#   something more here... 
	#   strip all but "filename" of newest session...

	start = time.time()
	
	imPrint = Image.open('for-phone/'+filename+'_phone.jpg')
	imDouble = Image.new('RGB', (4000, 6000), 'white')
	# generate double strip for printing...
	imDouble.paste( imPrint, (0, 0, 2000, 6000) )
	imDouble.paste( imPrint, (2000, 0, 4000, 6000) )
	draw = ImageDraw.Draw(imDouble)
	draw.line( (2000, 0, 2000, 6000), fill='rgb(0,0,0)', width=2)
	del draw
	imDouble.save('for-print/'+filename+'_print.jpg', 'JPEG', quality=90)

	print '\r\nProcessing done: ', time.time()-start

	# send print job here...

	# then save to printed list...
	printed.append(filename)
	
	# print elapsed time to console...
	print '\r\nTotal cycle time: ', time.time()-start



