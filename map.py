import random
from cmu_graphics import *
from gamePlatform import *
from obstacles import *
from terrain import *

class Map:
    def __init__(self):
        self.canvas = Canvas(600,400) #generate a long canvas -> can change the length of canvas to make game longer or shorter
        self.terrainList = []
        self.obstacleList = []
        self.platformList = []
        self.createMap()

    def createMap(self): #generates a map with obstacles and platforms -> can include parameter for level difficulty
        self.createTerrain(start=True)
        self.createObstacle(start=True)
        self.createPlatform(start=True)

        # #creates obstacles
        # for index in range(self.numberObstacles):
        #     obstacleXMin = index*self.obstacleInterval 
        #     obstacleXMax = obstacleXMin + self.obstacleInterval
        #     obstacleXCoord = random.randint(obstacleXMin, obstacleXMax)
        #     #check through the terrain and check what is the yCoord of the terrain at that xCoord
        #     obstacleYCoord = self.terrain.findYCoord(obstacleXCoord) #yCoord of the surface of the terrain
        #     if obstacleYCoord == None: raise ValueError('No Y Coordinate found for terrain')
        #     self.createObstacle(obstacleXCoord, obstacleYCoord)
        # #creates platforms
        # for index in range(self.numberPlatforms):
        #     platformXMin = index*self.platformInterval 
        #     platformXMax = platformXMin + self.platformInterval
        #     platformXCoord = random.randint(platformXMin, platformXMax)
        #     platformYCoord = self.terrain.findYCoord(platformXCoord) #yCoord of the surface of the terrain
        #     self.createPlatform(platformXCoord, platformYCoord)
        
    def createPlatform(self, start=False):
        if start == True:
            xMin = 0
            xMax = self.canvas.canvasWidth
            xCoord = random.randint(xMin, xMax)
            yCoord = self.findTerrainHeight(xCoord) - random.randint(100,150)
            platform = GamePlatform(map = self, xCoord = xCoord, yCoord = yCoord)
            self.platformList.append(platform)
            #create obstacles for the starting map
        else:
            #create obstacles to add onto the map -> on the border of the canvas
            xCoord = self.canvas.canvasWidth #at the border of the canvas
            yCoord = self.findTerrainHeight(xCoord)
            obstacle = GamePlatform(map = self, xCoord = xCoord, yCoord = yCoord)
            self.platformList.append(obstacle)

    def createObstacle(self, start=False):
        if start == True:
            for i in range(3):
                xMin = i*self.canvas.canvasWidth//3
                xMax = xMin + self.canvas.canvasWidth//3
                xCoord = random.randint(xMin, xMax)
                yCoord = self.findTerrainHeight(xCoord)
                obstacle = Obstacle(map = self, xCoord = xCoord, yCoord = yCoord)
                if obstacle.obstacle == None: 
                    #print('No obstacles')
                    continue
                else:
                    self.obstacleList.append(obstacle)
                #print(self.obstacleList)
            #create obstacles for the starting map
        else:
            #create obstacles to add onto the map -> on the border of the canvas
            xCoord = self.canvas.canvasWidth
            yCoord = self.findTerrainHeight(xCoord)
            obstacle = Obstacle(map = self, xCoord = xCoord, yCoord = yCoord)
            if obstacle.obstacle == None: 
                pass
            else:
                self.obstacleList.append(obstacle)
    
    def createTerrain(self, start=False):
        if start == True:
            #create a starting terrain
            numBlocks = self.canvas.canvasWidth//Floor.width
            terrain = Terrain(map = self, width = numBlocks, xCoord = 0) #returns a terrain object
        else:
            #create a terrain to add onto the map
            terrain = Terrain(map = self, xCoord = self.canvas.canvasWidth)
        self.terrainList.append(terrain)

    def findTerrainHeight(self, xCoord):
        for terrain in self.terrainList:
            if terrain.xCoord <= xCoord <= terrain.xCoord + terrain.getWidthPixel(terrain.width, Floor.width):
                return terrain.yCoord
        raise ValueError('No Y Coordinate found for terrain')

class Canvas: 
    def __init__(self, canvasWidth, canvasHeight):
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        


