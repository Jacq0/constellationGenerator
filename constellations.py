from tkinter import *
import random
import math as m

#As seen on: https://github.com/Jacq0/constellationGenerator

#variables for program
starsize = 3
minStars = 256
maxStars = 1024

windowWidth = 1024
windowHeight = 1024

#arrays to store x and y values of the stars (both will be identical in size!)
starPosX = []
starPosY = []

#generate our window and canvas with tkinter
window = Tk()
window.title("Constellation Generator")
canvas = Canvas(window, width=windowWidth, height=windowHeight, border=0, highlightthickness=0, bg="black")
canvas.pack()

#basis for a star class, we can use this to create star objects instead of just drawing dots, might be slower but much more dynamic! (TODO)
class Star():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y

    #this is just findClosest but for this object
    def closestNeighbour(self):
        print("Placeholder")


#simple method for drawing circles, does all the maths for us!
def drawCircle(x,y,r):
    #calcuate with offsets
    x0 = x-r
    y0 = y-r
    x1 = x+r
    y1 = y+r
    return canvas.create_oval(x0,y0,x1,y1, fill="#ff8") #now we can draw stars!

def findClosest(x0,y0): #find the closest star to this point!
    closest = 10000000 #really big base number!
    for i in range(0, len(starPosX)):
        x1 = starPosX[i] 
        y1 = starPosY[i]
        dist = m.sqrt(pow((x1-x0),2)+pow((y1-y0),2))
        if(dist > 1 and dist < closest):
            closest = dist
            coordX = x1
            coordY = y1
    return closest, coordX, coordY

#draw the line
def drawLine(x0,y0, x1,y1):
    return canvas.create_line(x0, y0, x1, y1, fill="#777", dash=(5,2))

#this is a bit slow and innefficient, I will iron those issues out in the future!
def generate():
    #randomly generate star coordinates
    for i in range(0,random.randrange(minStars,maxStars+1)):
        starX = random.randrange(0,windowWidth+1)
        starY = random.randrange(0,windowHeight+1)
        starPosX.append(starX)
        starPosY.append(starY)

    #connect stars (will occasionally double up lines!)
    for i in range(0, len(starPosX)):
        x = starPosX[i]
        y = starPosY[i]
        drawLine(x,y, findClosest(x,y)[1], findClosest(x,y)[2])

    #to draw over the lines (not efficient, but easiest way!)
    for i in range(0, len(starPosX)):
        x = starPosX[i]
        y = starPosY[i]
        drawCircle(x,y,starsize)

generate() #output looks nice, but its not realistic, keeping it for now!
#main loop to keep the window open!
window.mainloop()