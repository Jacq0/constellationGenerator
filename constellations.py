from tkinter import *
import random
import math as m

#As seen on: https://github.com/Jacq0/constellationGenerator

#variables for program
starsize = 3
minStars = 256
maxStars = 1024

windowWidth = 1280
windowHeight = 1024

#arrays to store x and y values of the stars (both will be identical in size!)
starPosX = []
starPosY = []

#generate our window and canvas with tkinter
window = Tk()
window.title("Constellation Generator")
canvas = Canvas(window, width=windowWidth, height=windowHeight, border=0, highlightthickness=0, bg="black")
canvas.pack()

stars = [] #list of stars

#basis for a star class, we can use this to create star objects instead of just drawing dots, might be slower but much more dynamic! (TODO)
class Star():
    #constructor
    def __init__(self, x, y, connections):
        self.x = x
        self.y = y
        self.connections = connections #this list isn't used atm, but is here for graphing further down the line

    #getters
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getConnected(self):
        return self.connections
    
    #setters
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def setConnections(self, connections):
        self.connections = connections

    #this is just findClosest but for this object
    def closestNeighbour(self):
        closest = 10000000
        for star in stars:
            x1 = star.getX()
            y1 = star.getY()
            dist = m.sqrt(pow((x1-self.x),2)+pow((y1-self.y),2))
            if(dist > 1 and dist < closest):
                closest = dist
                closeStar = star
        return closeStar #return our closest neighbour!

    #could have bundled this with closest, but can do that later
    def secClosestNeighbour(self):
        closest = 10000000
        secClosest = 100000001
        for star in stars:
            x1 = star.getX()
            y1 = star.getY()
            dist = m.sqrt(pow((x1-self.x),2)+pow((y1-self.y),2))
            if(dist > 1 and dist < closest):
                closest = dist
        
        for star in stars:
            x1 = star.getX()
            y1 = star.getY()
            dist = m.sqrt(pow((x1-self.x),2)+pow((y1-self.y),2))
            if(dist > closest and dist < secClosest):
                secClosest = dist
                secCloseStar = star
        
        return secCloseStar #return our 2nd closest neighbour!

    def farthestNeighbour(self):
        farthest = 0
        for star in stars:
            x1 = star.getX()
            y1 = star.getY()
            dist = m.sqrt(pow((x1-self.x),2)+pow((y1-self.y),2))
            if(dist > farthest):
                farthest = dist
                farStar = star
        return farStar #return our farthest neighbour!
    
    #this function is buggy at best, especially with lower star counts, but does give a nice output 
    def fiveNearest(self):
        c1 = 100000000
        c2 = 10000000
        c3 = 1000000
        c4 = 100000
        c5 = 10000
        for star in stars:
            x1 = star.getX()
            y1 = star.getY()
            dist = m.sqrt(pow((x1-self.x),2)+pow((y1-self.y),2))
            if(dist > 1 and dist < c1):
                c1 = dist
                c1Star = star
            elif(dist > c1 and dist < c2):
                c2 = dist
                c2Star = star
            elif(dist > c2 and dist < c3):
                c3 = dist
                c3Star = star
            elif(dist > c3 and dist < c4):
                c4 = dist
                c4Star = star
            elif(dist > c4 and dist < c5):
                c5 = dist
                c5Star = star
        return c1Star,c2Star,c3Star,c4Star,c5Star #return the top 5 closest!
        

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

#this is now the legacy generate function!
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

def generate2():
    for i in range(0,random.randrange(minStars,maxStars+1)):
        starX = random.randrange(0,windowWidth+1)
        starY = random.randrange(0,windowHeight+1)
        stars.append(Star(starX, starY, []))

    #connect a random number of the top 5 nearest neighbours!
    for i in range(0, len(stars)):
        x = stars[i].getX()
        y = stars[i].getY()
        for j in range(0,random.randrange(1,len(stars[0].fiveNearest())+1)): #this generates a lovely web pattern! when not using random range!
            star = stars[i].fiveNearest()[j]
            x1 = star.getX()
            y1 = star.getY()
            drawLine(x,y, x1, y1) #connect the nearest

    for i in range(0, len(stars)):
        x = stars[i].getX()
        y = stars[i].getY()
        drawCircle(x,y,starsize)


def generate3():
    for i in range(0,random.randrange(minStars,maxStars+1)):
        starX = random.randrange(0,windowWidth+1)
        starY = random.randrange(0,windowHeight+1)
        stars.append(Star(starX, starY, []))

    #connect a random number of the top 5 nearest neighbours!
    for i in range(0, len(stars)):
        x = stars[i].getX()
        y = stars[i].getY()
        star = stars[i].closestNeighbour()
        #star = stars[i].farthestNeighbour()
        x1 = star.getX()
        y1 = star.getY()
        drawLine(x,y, x1, y1) #connect the nearest
        star = stars[i].secClosestNeighbour()
        x1 = star.getX()
        y1 = star.getY()
        drawLine(x,y, x1, y1) #connect the nearest

    for i in range(0, len(stars)):
        x = stars[i].getX()
        y = stars[i].getY()
        drawCircle(x,y,starsize)

#generate() #output looks nice, but its not realistic, keeping it for now!
#generate2() #this output is a lot more messy but creates a nice web effect
generate3()

#this was just a test for the 5 nearest function!
#for i in range(0,len(stars[0].fiveNearest())):
#    star = stars[0].fiveNearest()[i]
#    x = star.getX()
#    y = star.getY()
#    print(x,y)

#main loop to keep the window open!
window.mainloop()