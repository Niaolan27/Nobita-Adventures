from cmu_graphics import *
from imageHandling import *
import random

class Square:
    width = 50
    height = 50
    image = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/square.png')
    def __init__(self, xCoord, yCoord):
        self.image = Square.image
        self.width = Square.width
        self.height = Square.height
        self.xCoord = xCoord
        self.yCoord = yCoord

    def draw(self):
        drawImage(self.image, self.xCoord, self.yCoord-self.height, width = self.width, height = self.height)
        #drawRect(self.xCoord, self.yCoord - self.height, self.width, self.height, fill = 'red', border='black')

class Fire:
    width = 50
    height = 10
    image = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/fire.png')
    def __init__(self, xCoord, yCoord):
        self.image = Fire.image
        self.width = Fire.width
        self.height = Fire.height
        self.xCoord = xCoord
        self.yCoord = yCoord

    def draw(self):
        drawImage(self.image, self.xCoord, self.yCoord-self.height, width = self.width, height = self.height)
        #drawPolygon(self.xCoord, self.yCoord, self.xCoord+self.width//2, self.yCoord-self.height, self.xCoord+self.width, self.yCoord, fill = 'blue', border = 'black') #triangle

class Glue:
    width = 50
    height = 10
    image = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/glue.png')
    def __init__(self, xCoord, yCoord):
        self.image = Glue.image
        self.width = Glue.width
        self.height = Glue.height
        self.xCoord = xCoord
        self.yCoord = yCoord

    def draw(self):
        drawImage(self.image, self.xCoord, self.yCoord-self.height, width = self.width, height = self.height)
        #drawPolygon(self.xCoord, self.yCoord, self.xCoord+self.width//2, self.yCoord-self.height, self.xCoord+self.width, self.yCoord, fill = 'blue', border = 'black') #triangle

class Obstacle: #defined by x Coord and obstacle type
    obstacleProb = [0.5, 0.2, 0.3]
    obstacleType = [Square, Fire, Glue]
    def __init__(self, map = None, xCoord = 0, yCoord = 0):
        self.map = map
        obstacle = random.choices(Obstacle.obstacleType, weights = Obstacle.obstacleProb)[0]
        self.obstacle = obstacle(xCoord, yCoord)
        
    
    def drawObstacle(self):
        #print(self.obstacle)
        self.obstacle.draw()
    
    def updateXCoord(self, step):
        self.obstacle.xCoord += step