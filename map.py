import random
from cmu_graphics import *
from gamePlatform import *
from obstacles import *

class Map:
    def __init__(self):
        self.canvas = Canvas(6000,400)
        self.numberObstacles = 20
        self.numberPlatforms = 5
        self.obstacleInterval = self.canvas.canvasWidth//self.numberObstacles
        self.platformInterval = self.canvas.canvasWidth//self.numberPlatforms
        self.obstacleList = []
        self.platformList = []
        self.createMap()

    def createMap(self): #can include level later on
        for index in range(self.numberObstacles):
            self.createObstacle(index*self.obstacleInterval)
        for index in range(self.numberPlatforms):
            self.createPlatform(index*self.platformInterval)

    # def createStart(self):
    #     for i in range(3): # hard coded for now
    #         x = i*(self.canvas.canvasWidth//3)
    #         obstacle = self.createObstacle(x)
        
    def createObstacle(self, xCoord):
        obstacle = Obstacle(self, xCoord)
        self.obstacleList.append(obstacle)

    def createPlatform(self, xCoord):
        platform = GamePlatform(self, xCoord)
        self.platformList.append(platform)

class Canvas:
    def __init__(self, canvasWidth, canvasHeight):
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        


