import random
from cmu_graphics import *
from gamePlatform import *
from obstacles import *

class Map:
    def __init__(self):
        self.canvas = Canvas(18000,400) #generate a long canvas -> can change the length of canvas to make game longer or shorter
        self.numberObstacles = 40
        self.numberPlatforms = 20
        self.obstacleInterval = self.canvas.canvasWidth//self.numberObstacles
        self.platformInterval = self.canvas.canvasWidth//self.numberPlatforms
        self.obstacleList = []
        self.platformList = []
        self.createMap()

    def createMap(self): #generates a map with obstacles and platforms -> can include parameter for level difficulty
        for index in range(self.numberObstacles):
            obstacleXMin = index*self.obstacleInterval 
            obstacleXMax = obstacleXMin + self.obstacleInterval
            obstacleXCoord = random.randint(obstacleXMin, obstacleXMax)
            self.createObstacle(obstacleXCoord)
        for index in range(self.numberPlatforms):
            platformXMin = index*self.platformInterval 
            platformXMax = platformXMin + self.platformInterval
            platformXCoord = random.randint(platformXMin, platformXMax)
            self.createPlatform(platformXCoord)
        
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
        


