import pygame
import os.path
import time
import picamera


# playback stuff
imageBasename = "usbdrv/img"
playNum = 1
done = False
msPlaybackDelay = 1
nextPlaybackMS = 1
maxImageCount = 400

# recording
msRecordingDelay = 4000
nextRecordMS = 1
recNum = 1

#delete all files in the directory
imgFile = "%s%03d.jpg" % (imageBasename,playNum)
num = 1
while os.path.isfile(imgFile):
	os.remove(imgFile)
	num = num+1
	imgFile = "%s%03d.jpg" % (imageBasename,playNum)
	
	
pygame.init()
screen = pygame.display.set_mode((0,0))
pygame.mouse.set_visible(0)


with picamera.PiCamera() as camera:
	camera.resolution = (320,240)	#TFT 913
	while not done:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				done = True
				
		# record an image
		if pygame.time.get_ticks() > nextRecordMS:
			nextRecordMS = pygame.time.get_ticks() + msRecordingDelay
			recFile = "%s%03d.jpg" % (imageBasename,recNum)
			camera.capture(recFile)
			recNum = recNum + 1
			if recNum > maxImageCount:	#make into a circular buffer
				recNum = 1			
			
		# will display the next image
		# check a timer here and then load the file appropriately
		if pygame.time.get_ticks() > nextPlaybackMS:
			nextPlaybackMS = pygame.time.get_ticks() + msPlaybackDelay
			imgFile = "%s%03d.jpg" % (imageBasename,playNum)
			if os.path.isfile(imgFile) == False:
				playNum = 1
				imgFile = "%s%03d.jpg" % (imageBasename,playNum)
			
			if os.path.isfile(imgFile):
				im = pygame.image.load(imgFile)
				playNum = playNum + 1
				screen.fill((0,0,0))
				screen.blit(im,(0,0))			
				pygame.display.update()
	




