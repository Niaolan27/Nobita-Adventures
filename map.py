import random
from cmu_graphics import *
from gamePlatform import *
from obstacles import *
from terrain import *

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
        #creates terrain
        self.terrain = Terrain(self) #the entire terrain is abstracted from the map
        #creates obstacles
        for index in range(self.numberObstacles):
            obstacleXMin = index*self.obstacleInterval 
            obstacleXMax = obstacleXMin + self.obstacleInterval
            obstacleXCoord = random.randint(obstacleXMin, obstacleXMax)
            #check through the terrain and check what is the yCoord of the terrain at that xCoord
            obstacleYCoord = self.terrain.findYCoord(obstacleXCoord) #yCoord of the surface of the terrain
            if obstacleYCoord == None: raise ValueError('No Y Coordinate found for terrain')
            self.createObstacle(obstacleXCoord, obstacleYCoord)
        #creates platforms
        for index in range(self.numberPlatforms):
            platformXMin = index*self.platformInterval 
            platformXMax = platformXMin + self.platformInterval
            platformXCoord = random.randint(platformXMin, platformXMax)
            platformYCoord = self.terrain.findYCoord(platformXCoord) #yCoord of the surface of the terrain
            self.createPlatform(platformXCoord, platformYCoord)
        
    def createObstacle(self, xCoord, yCoord):
        obstacle = Obstacle(self, xCoord, yCoord)
        self.obstacleList.append(obstacle)

    def createPlatform(self, xCoord, yCoord):
        platform = GamePlatform(self, xCoord, yCoord) #yCoord of the surface of the terrain
        self.platformList.append(platform)

class Canvas: 
    def __init__(self, canvasWidth, canvasHeight):
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        


