from cmu_graphics import *
import random

class Square:
    width = 50
    height = 50
    def __init__(self, xCoord, yCoord):
        self.width = Square.width
        self.height = Square.height
        self.xCoord = xCoord
        self.yCoord = yCoord - self.height

    def draw(self):
        drawRect(self.xCoord, self.yCoord, self.width, self.height)

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
    obstacleDict = {0: Square,
                    1: Spike} #include a bunch of obstacle types here
    obstacleProbWeights = {0: 0.8,
                           1: 0.2} #probability of generating each obstacle -> can vary based on difficulty 
    def __init__(self, map, xCoord, yCoord):
        self.xCoord = xCoord
        self.yCoord = yCoord #yCoord of the terrain surface
        #self.yCoord = map.canvas.canvasHeight - 50 #top left corner of a square -> might have to redefine for each shape
        self.map = map
        self.generateShape(self.xCoord, self.yCoord)
    
    def generateShape(self, xCoord, yCoord): #Monte Carlo implementation
        obstacleListIndex = list(Obstacle.obstacleDict.keys())
        obstacleProbability = list(Obstacle.obstacleProbWeights.values())
        shapeIndex = random.choices(obstacleListIndex, weights = obstacleProbability)[0] #to get a random shape
        self.shape = Obstacle.obstacleDict[shapeIndex](xCoord, yCoord)
    
    def drawObstacle(self):
        self.shape.draw()
    
    def updateXCoord(self, step):
        self.shape.xCoord += step

