import random
from cmu_graphics import *


class Map:
    def __init__(self):
        self.canvas = Canvas(600,400)
        self.obstacleList = []
    
    def createStart(self):
        for i in range(3): # hard coded for now
            x = i*(self.canvas.canvasWidth//3)
            obstacle = self.createObstacle(x)
        
    def createObstacle(self, xCoordinate):
        obstacle = Obstacle(xCoordinate)
        self.obstacleList.append(obstacle)
    
    def drawObstacle(self, obstacle, canvas):
        obstacle.drawObstacle(canvas)

class Canvas:
    def __init__(self, canvasWidth, canvasHeight):
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        
class Obstacle: #defined by x coordinate and obstacle type
    obstacleList = [] #include a bunch of obstacle types here
    def __init__(self, xCoordinate):
        #do some random function and return one of the obstacles
        self.xCoordinate = xCoordinate
        self.shape = Square()
    
    def drawObstacle(self, canvas):
        self.shape.draw(self.xCoordinate, canvas)

class Square:
    def __init__(self):
        self.width = 50
        self.height = 50
    def draw(self, xCoordinate, canvas):
        drawRect(xCoordinate, canvas.canvasHeight - self.height, self.width, self.height)