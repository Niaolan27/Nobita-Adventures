from cmu_graphics import *
import random

class Square:
    width = 50
    height = 50
    def __init__(self, xCoord, yCoord):
        self.width = Square.width
        self.height = Square.height
        self.xCoord = xCoord
        self.yCoord = yCoord

    def draw(self):
        drawRect(self.xCoord, self.yCoord - self.height, self.width, self.height)

class Spike:
    width = 50
    height = 50
    def __init__(self, xCoord, yCoord):
        self.width = Square.width
        self.height = Square.height
        self.xCoord = xCoord
        self.yCoord = yCoord

    def draw(self):
        drawPolygon(self.xCoord, self.yCoord, self.xCoord+self.width//2, self.yCoord-self.height, self.xCoord+self.width, self.yCoord) #triangle

class Obstacle: #defined by x Coord and obstacle type
    obstacleProb = [0.8, 0.1, 0.1]
    obstacleType = [None, Square, Spike]
    def __init__(self, map = None, xCoord = 0, yCoord = 0):
        self.map = map
        obstacle = random.choices(Obstacle.obstacleType, weights = Obstacle.obstacleProb)[0]
        if obstacle == None: 
            self.obstacle = None
        else: self.obstacle = obstacle(xCoord, yCoord)
        
    
    def drawObstacle(self):
        #print(self.obstacle)
        self.obstacle.draw()
    
    def updateXCoord(self, step):
        self.obstacle.xCoord += step

