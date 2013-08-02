#Filename: gameFunctions.py
#Author: Ryan Blakely
#Last Modified By: Ryan Blakely
#Last Modified: July 31st, 2013
#Description: Functions required for the ZombieMiner.py game


import pygame
from pygame.locals import *

from gameConstants import *

#initialize pygame
pygame.init()
#dirty fix to allow loading of images before main display kicks in
pygame.display.set_mode((1,1), pygame.NOFRAME)

#Generic load image function - loads an image from a file and sets its colorkey if given
#imgFile (str) - the filename for the image
#transColor (color) - the color wished to be transparent
#returns - the image (pygame Surface)
def loadImage(imgFile,transColor=None):
    #load image from file
    img = pygame.image.load(imgFile)
    
    #if there is a transparency color set, set the colorkey so that color is transparent
    if(transColor):
        #img=img.convert() #transparency fix for some images - converts it so it doesnt have a per-pixel alpha. not currently used
        img.set_colorkey(transColor, RLEACCEL)
    
    return img

#Creates an image from text - handles multi-line text since pygame doesnt natively support it
#text (str) - text to convert to an image
#font (pygame Font) - Font to be used in the image
#color (Color) - color of text
#lineDlim (str) - line delimiter for the text if its multi-line
#lineCenter (bool) - flag to determine whether or not to center multi-line text
#returns - the text as an image (pygame Surface)
def textImage(text,font,color,lineDlim=None,lineCenter=False):
    if(lineDlim): #if there is a line delimter...
        lines = str(text).split(lineDlim) # split up the line
        imgWid=0 #the final images width
        lineImgs=list() #create a list to store the line images
        for line in lines: #loop through each line in the text
            lineImgs.append(font.render(line, 1, color)) #render its image (using bit transparency) and add it to the img list
            
            #determine if this line is the largest so far, if so, store its size 
            if font.size(line)[X] > imgWid:
                imgWid=font.size(line)[X]
        
        #create a surface to hold the master image, fill the surface and set its colorkey to the transparent color
        txtImg=pygame.Surface((imgWid,len(lines)*font.get_linesize()),pygame.SRCALPHA)
        
        for i in range(0,len(lineImgs)): #loop through each line img and draw it to the master img
            #center the text if it required
            drawX=0
            if lineCenter: drawX=(imgWid/2)-(lineImgs[i].get_size()[X]/2)
            
            txtImg.blit(lineImgs[i],(drawX,i*font.get_linesize()))
        
    else: #otherwise, if its not a multi-liner...
        #render it with bit transparency
        txtImg=font.render(text, 1, color)
        
    return txtImg

#Checks a given position value from a UI element to determine if it needs any special UI alignments in regards to its container
#pos (tuple) - the position to check for special UI flags
#bigSize (tuple) - the size of the container of the UI element
#smallSize (tuple) - the size of the UI element
#returns - either the original position if no UI alignment changes needed to occur, or the fixed positions for UI alignment
def specialPos(pos,bigSize,smallSize):
    #if the x position is meant to be "centered", center it
    if (pos[X]==ALIGN_CENTER):
        newPos = (bigSize[X]/2.0 - smallSize[X]/2.0,pos[Y]) #force float divison
    else:
        newPos = pos
    
    #if the y pos is meant to be "centered", center it
    if (pos[Y]==ALIGN_CENTER):
        newPos = (newPos[X],bigSize[Y]/2.0 - smallSize[Y]/2.0) #force float divison

    #elseif the y pos is meant to be "bottomed", put it at the bottom of the container
    elif (pos[Y]==ALIGN_BOTTOM):
        newPos = (newPos[X],bigSize[Y]-smallSize[Y])
        
    return newPos;

#Generic pixel-by-pixel RGB brightener (or shader) for a Surface
#img (Surface) - the image to change the rgb values of
#factor (float) - factor (0.1=10%,2=200%) to modify the rgb by
#returns - N/A, modifies img directly
def changeBrightness(img,factor):
    for y in range(img.get_height()):
        for x in range(img.get_width()):
            pixel = img.get_at((x,y))
            if (pixel!=img.get_colorkey()):
                rgb=[int(factor * pixel.r),int(factor * pixel.g),int(factor * pixel.b)]
                
                #make sure chosen rgb values are valid
                for clr in range(0,len(rgb)):
                    if rgb[clr] > MAX_RGB:
                        rgb[clr]=MAX_RGB
                    elif rgb[clr]<MIN_RGB:
                        rgb[clr]=MIN_RGB
                
                img.set_at((x,y),(rgb[0],rgb[1],rgb[2]))

#Given a time in seconds, converts it into minutes and seconds
#time (int) - time in seconds
#returns - tuple (minutes,seconds)
def humanTime(time):
    minutes= str(time/1000/60)
    seconds=str((time/1000) % 60)
    
    return (minutes,seconds)