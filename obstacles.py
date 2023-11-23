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
        #print(self.xCoord, self.yCoord)
        drawRect(self.xCoord, self.yCoord - self.height, self.width, self.height, fill = 'red', border='black')

class Spike:
    width = 50
    height = 50
    def __init__(self, xCoord, yCoord):
        self.width = Square.width
        self.height = Square.height
        self.xCoord = xCoord
        self.yCoord = yCoord

    def draw(self):
        drawPolygon(self.xCoord, self.yCoord, self.xCoord+self.width//2, self.yCoord-self.height, self.xCoord+self.width, self.yCoord, fill = 'blue', border = 'black') #triangle

class Obstacle: #defined by x Coord and obstacle type
    obstacleProb = [0.5, 0.5]
    obstacleType = [Square, Spike]
    def __init__(self, map = None, xCoord = 0, yCoord = 0):
        self.map = map
        obstacle = random.choices(Obstacle.obstacleType, weights = Obstacle.obstacleProb)[0]
        self.obstacle = obstacle(xCoord, yCoord)
        
    
    def drawObstacle(self):
        #print(self.obstacle)
        self.obstacle.draw()
    
    def updateXCoord(self, step):
        self.obstacle.xCoord += step

