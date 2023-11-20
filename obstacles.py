from cmu_graphics import *


class Obstacle: #defined by x Coord and obstacle type
    obstacleList = [] #include a bunch of obstacle types here
    def __init__(self, map, xCoord):
        #do some random function and return one of the obstacles
        self.xCoord = xCoord
        self.yCoord = map.canvas.canvasHeight - 50
        self.map = map
        self.shape = Square(self.xCoord, self.yCoord)
    
    def drawObstacle(self):
        self.shape.draw()
    
    def updateXCoord(self, step):
        self.shape.xCoord += step

class Square:
    width = 50
    height = 50
    def __init__(self, xCoord, yCoord):
        self.width = Square.width
        self.height = Square.height
        self.xCoord = xCoord
        self.yCoord = yCoord

    def draw(self):
        drawRect(self.xCoord, self.yCoord, self.width, self.height)