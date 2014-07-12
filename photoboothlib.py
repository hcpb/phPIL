#!/usr/bin/python
import threading
import time
import piggyphoto
import os, sys
import shutil
import pygame
from string import split,join
from pygame.locals import *
import Image, ImageDraw

# list with raw image suffixes, used for appending to files as they are created
suffix = [ 'a', 'b', 'c', 'd' ]


# *** for PIL instead of graphicsmagick... ***
imDisplay = Image.new('RGBA', (1280, 720), 'white')
imPrint = Image.new('RGBA', (2000, 6000), 'white')
dispbox = [ (124, 12, 628, 348), (124, 373, 628, 709), 
		(652, 12, 1156, 348), (652, 373, 1156, 709) ]
printbox= [ (120, 996, 1876, 2160), (120, 2248, 1876, 3412), 
		(120, 3500, 1876, 4664), (120, 4752, 1876, 5916) ]
# ********************************************



# execute a shell command, printing it to the console for debugging purposes...
def shellcmd(command):
	print ' =>', command
	os.system(command)

# new filename generation function: returns next sequential filename
def new_filename(storename='lastphoto', increment=True):
	last = eval(open(storename, 'r').read())
	filename = 'DSC' + (4-len(str(last)))*'0' + str(last)
	if increment: last=last+1
	open(storename, 'w').write(str(last))
	return filename


# delete the temporary files created during creation of composites...
def cleanup_temp_files(filename):
	# remove temp files...
	shellcmd('rm *output.jpg done.jpg '+filename+'*done')

# filename function: returns next sequential filename (as a string)
def new_filename(storename='lastphoto', increment=True):
	last = eval(open(storename, 'r').read())
	filename = 'DSC' + (4-len(str(last)))*'0' + str(last)
	if increment: last=last+1
	open(storename, 'w').write(str(last))
	return filename


def grab_image2(filename, i, usecamera=True):
	# Only capture image if it's one of the four... 
	if i in range(4): 
		# grab from camera or make a copy of the dummy images (for testing...)
		if usecamera:
			# create PTP connection to camera...
			C = piggyphoto.camera() 
			C.capture_image(filename+'_'+suffix[i] + '.jpg')
		else: shellcmd('cp images/DSCdummy'+str(i+1)+'.jpg '+filename+'_'+suffix[i] + '.jpg')


# add each new image to the dipslay composite...
def composite_add_display(fname, i):
	tmp = Image.open(fname)
	imDisplay.paste(tmp.resize( (504, 336), Image.ANTIALIAS), dispbox[i])

# add each new image to the print composite...
def composite_add_print(fname, i):
	tmp = Image.open(fname)
	imPrint.paste(tmp.resize( (1756, 1164), Image.ANTIALIAS), printbox[i])
	

# move files into local subdirectories and SAMBA share at path
def move_files(filename, path='/media/PHOTOBOOTH/', copy=True):
      if copy: cmd='cp '
      else: cmd='mv '
      try:
	print
	print 'filename = ', filename
	print cmd+'raw images...'
	shellcmd(cmd+filename+'_[a-d].jpg '+path+'raw-images')
	print cmd+'dislay images...'
        shellcmd(cmd+filename+'_display.jpg '+path+'for-display')
	print cmd+'print image...'
        shellcmd(cmd+filename+'_print.jpg '+path+'for-print')
	print cmd+'phone image...'
        shellcmd(cmd+filename+'_phone.jpg '+path+'for-phone')
      except:
	print 'PROBLEMS!!'


#size = width, height = 960, 540
#camerasize = camw, camh =  810,540
size = width, height = 1230, 692
camerasize = camw, camh =  1037,692
cameraloc = (width-camw)/2, 0
black = (0,0,0)
white = (255,255,255)

def waitforkey(key, quitable = True):
	userkey = False
	while not(userkey):
		time.sleep(1)
		for event in pygame.event.get():
			#print repr(event)
			if event.type == QUIT: sys.exit()
			elif event.type == KEYDOWN: 
				#print 'keydown...'
				if event.key in key: return event.key
				if quitable and event.key == K_q: sys.exit()
	pygame.event.clear()

def fillscreen(screen, color):
	screen.fill(color)
	pygame.display.flip()

def displayimage(screen, filename, size, location=(0,0)):
		image = pygame.image.load(filename)
		imagerect = image.get_rect()
		image = pygame.transform.scale(image, size)
		screen.blit(image, location)
		pygame.display.flip()

def flashtext(duration, rate, screen, text, size, location=None):
	bgwhite = pygame.Surface(screen.get_size())
	bgblack = pygame.Surface(screen.get_size())
	bgwhite = bgwhite.convert()
	bgblack = bgblack.convert()
	bgwhite.fill(white)
	bgblack.fill(black)
	
	fontname = pygame.font.match_font('freeserif')
	font = pygame.font.Font(fontname, 128)
	textw = font.render(text, 1, white)
	textb = font.render(text, 1, black)
	textwpos = textw.get_rect()
	textbpos = textb.get_rect()
	if location==None:
		textwpos.centerx = textbpos.centerx = bgwhite.get_rect().centerx	
		textwpos.centery = textbpos.centery = bgwhite.get_rect().centery
	else:
		w,h = location
		textwpos.centerx = textbpos.centerx = w
		textwpos.centery = textbpos.centery = h
	bgwhite.blit(textb, textbpos)
	bgblack.blit(textw, textbpos)

	start = time.time()
	while (time.time()-start < duration):
		screen.blit(bgblack, (0,0))
		pygame.display.flip()
		time.sleep(rate/2.)
		screen.blit(bgwhite, (0,0))
		pygame.display.flip()
		time.sleep(rate/2.)


def showtext(screen, text, size, location=None):
	bgwhite = pygame.Surface(screen.get_size())
	bgwhite = bgwhite.convert()
	bgwhite.fill(black)#white)
	
	fontname = pygame.font.match_font('freeserif')
	font = pygame.font.Font(fontname, size)
	textb = font.render(text, 1, white)#black)

	textbpos = textb.get_rect()
	if location==None:
		textbpos.centerx = bgwhite.get_rect().centerx	
		textbpos.centery = bgwhite.get_rect().centery
	else:
		w,h = location
		textbpos.centerx = w	
		textbpos.centery = h
	bgwhite.blit(textb, textbpos)

	screen.blit(bgwhite, (0,0))
	pygame.display.flip()



