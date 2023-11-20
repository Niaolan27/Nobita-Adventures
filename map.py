import random
from cmu_graphics import *
from gamePlatform import *
from obstacles import *

class Map:
    def __init__(self):
        self.canvas = Canvas(6000,400) #generate a long canvas -> can change the length of canvas to make game longer or shorter
        self.numberObstacles = 20
        self.numberPlatforms = 10
        self.obstacleInterval = self.canvas.canvasWidth//self.numberObstacles
        self.platformInterval = self.canvas.canvasWidth//self.numberPlatforms
        self.obstacleList = []
        self.platformList = []
        self.createMap()

    def createMap(self): #generates a map with obstacles and platforms -> can include parameter for level difficulty
        for index in range(self.numberObstacles):
            self.createObstacle(index*self.obstacleInterval)
        for index in range(self.numberPlatforms):
            self.createPlatform(index*self.platformInterval)
        
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
        


