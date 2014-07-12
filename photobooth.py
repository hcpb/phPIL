 #!/usr/bin/python
# many dependencies are all brought in with this import...
from photoboothlib import *

#=============================================================================
# ========================= COMMAND LINE ARGUMENTS ===========================
#=============================================================================
if 'help' in sys.argv or '-h' in sys.argv or '--help' in sys.argv:
	print """
NAME: 
	photobooth.py  -  a photo booth python script

OPTIONS:
	-h,--help,help	print help
	nousecamera	use dummy photos instead of camera (default: USB connected camera)
	nomove		do not move images after processing (default: move)
	lastphoto=xxxx	begin sequence with the provided 4-digit (>=1000) number 
	noincrement	do not increment the image sequence number (default: increment)
	doubleprint	generate the double print (adds time, default: no doubleprint)
	sepia		do composites in sepia tone
	bw		do composites in black and white

DESCRIPTION:
	This python script implements a photo booth where a sequence of four images is 
	taken by a USB-connected camera and processed into various composite images.

	Requires: libgphoto2, python-pygame, piggyphoto (python binding for libgphoto2)
	and graphicsmagick.

"""
	sys.exit()

# use camera or dummy source images...
if 'nousecamera' in sys.argv:
	camera_arg=False
else:
	camera_arg=True

if 'doubleprint' in sys.argv:
	doubleprint=True
else:
	doubleprint=False

# use sepia tone...
tone = ''
if 'sepia' in sys.argv and not('bw' in sys.argv):
	tone = '-sepia'
if 'bw' in sys.argv and not('sepia' in sys.argv):
	tone='-bw'

# move the files when done? Assume true...
move=True
if 'nomove' in sys.argv:
	print 'Not moving files...'
	move=False

# set lastphoto via command line... 
lastphoto=False
for i in sys.argv:
	if 'lastphoto' in i:
		lastphoto = True
		temp = split(i, '=')[1]
		break
if not(lastphoto):
	# this should be rolled into the filename function but for now it's here...
	last = eval(open('lastphoto', 'r').read())
	print 'Change current photo number '+str(last)+'?'
	temp = raw_input( 'Enter valid new number or nothing to keep: ')
if temp not in ['']: 
	last = eval(temp) 
	open('lastphoto', 'w').write(str(last))

# increment output photo index? default is true...
increment=True
if 'noincrement' in sys.argv:
	increment = False
#=============================================================================
# ===================== DONE COMMAND LINE ARGUMENTS ==========================
#=============================================================================



#=============================================================================
# ==================================  MAIN  ==================================
#=============================================================================

# verify command line args...
print 'nousecamera:', repr(camera_arg)
print 'nomove:', repr(move)
print 'lastphoto:', last
print 'increment:', repr(increment)
print 'doubleprint:', repr(doubleprint)

pygame.init()
screen = pygame.display.set_mode(size)
#toggle_fullscreen()

while (1):
	showtext(screen, "Push a button to start", 100)

	key = waitforkey([K_g, K_r, K_y])
	if key == K_y: tone='-sepia'
	if key == K_r: tone='-bw'
	if key == K_g: tone =''

	fillscreen(screen, black)

	# keep track of the starting time for some statistics...
	start = time.time()
	
	# get a new filename and print it to the console...
	filename= new_filename(increment=increment)
	print '\r\nnew filename:', filename

	# grab the sequence of images from the camera (or, if specified, dummy images)...
	for i in range(4):
		showtext(screen, 'Image: '+str(i+1), 100)
		time.sleep(0.5)
		print 
		print 'Grabbing image: ', i+1
		fillscreen(screen, black)
		grab_image2(filename, i, camera_arg)

		# display image just taken
		displayimage(screen, filename+'_'+suffix[i]+'.jpg', camerasize, cameraloc)

		# two threads for compositing images...
		fname = filename+'_'+suffix[i] + '.jpg'
		t_ = []
		t_.append( threading.Thread(target=composite_add_display, args=(fname, i)) )
		t_.append( threading.Thread(target=composite_add_print,	args=(fname, i)) )
		for i in t_: i.start()
		while ( t_[0].isAlive() or t_[1].isAlive() ):
			time.sleep(0.05)
		print time.time()-start


	showtext(screen, 'Processing...', 100)
	# add emblems to composites...
	tmp = Image.open('images/overlay-disp.png').resize( (233, 233), Image.ANTIALIAS )
	print tmp.size, tmp.mode
	imDisplay.paste( tmp, (522, 243, 755, 476), mask=tmp )
	# save display composite...
	imDisplay.save(filename+'_display.jpg', 'JPEG', quality=98)

	# throw up completed display image while finishing up print images...
	displayimage(screen, filename+'_display.jpg', size)

	# save single print composite...
	tmp = Image.open('images/overlay-phone.png').resize( (1500, 941), Image.ANTIALIAS )
	print tmp.size, tmp.mode
	imPrint.paste( tmp, (250, 50, 1750, 991), mask=tmp )
	imPrint.save(filename+'_phone.jpg', 'JPEG', quality=90)
	imDouble = Image.new('RGB', (4000, 6000), 'white')
	# generate double strip for printing...
	imDouble.paste( imPrint, (0, 0, 2000, 6000) )
	imDouble.paste( imPrint, (2000, 0, 4000, 6000) )
	draw = ImageDraw.Draw(imDouble)
	draw.line( (2000, 0, 2000, 6000), fill='rgb(0,0,0)', width=2)
	del draw
	imDouble.save(filename+'_print.jpg', 'JPEG', quality=90)

	print '\r\nProcessing done: ', time.time()-start

#	time.sleep(8)

	# clean up the temporary files generated during compositing...
	cleanup_temp_files(filename)

	# print elapsed time to console...
	print '\r\nTotal cycle time: ', time.time()-start



