import random
from cmu_graphics import *
from gamePlatform import *
from obstacles import *
from terrain import *

class Map:
    def __init__(self, canvas = None):
        #print(canvas[0], canvas[1])
        self.canvas = Canvas(canvas[0], canvas[1]) #generate a long canvas -> can change the length of canvas to make game longer or shorter
        self.terrainList = []
        self.obstacleList = []
        self.platformList = []
        self.createMap()

    def createMap(self): #generates a map with obstacles and platforms -> can include parameter for level difficulty
        self.createTerrain(start=True)
        self.createObstacle(start=True)
        self.createPlatform(start=True)
        
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
            yCoord = self.findTerrainHeight(xCoord) - random.randint(100,150)
            obstacle = GamePlatform(map = self, xCoord = xCoord, yCoord = yCoord)
            self.platformList.append(obstacle)

    def createObstacle(self, start=False):
        minDist = 100
        if start == True:
            for i in range(3):
                nearestObstacleIndex = self.findNearestObstacle(self.canvas.canvasWidth)
                #print(nearestObstacleIndex)
                if nearestObstacleIndex == None:
                    xMin = i*self.canvas.canvasWidth//3
                    xMax = xMin + self.canvas.canvasWidth//3
                    xCoord = random.randint(xMin, xMax)
                    yCoord = self.findTerrainHeight(0)
                else:
                    nearestObstacle = self.obstacleList[nearestObstacleIndex]
                    xCoord = nearestObstacle.obstacle.xCoord + nearestObstacle.obstacle.width + random.randint(minDist, minDist+100)
                    yCoord = self.findTerrainHeight(xCoord)
                obstacle = Obstacle(map = self, xCoord = xCoord, yCoord = yCoord)
                self.obstacleList.append(obstacle)
                #print(self.obstacleList)
            #create obstacles for the starting map
        else:
            #create obstacles to add onto the map -> on the border of the canvas

            #ensures that obstacle generated is not too close
            nearestObstacleIndex = self.findNearestObstacle(self.canvas.canvasWidth)
            #print(nearestObstacleIndex)
            nearestObstacle = self.obstacleList[nearestObstacleIndex]
            nearestTerrainIndex = self.findNearestTerrain(self.canvas.canvasWidth)
            #print(nearestTerrainIndex)
            nearestTerrainBefore = self.terrainList[nearestTerrainIndex-1]
            distFromNearestObstacle = self.canvas.canvasWidth - nearestObstacle.obstacle.xCoord - nearestObstacle.obstacle.width
            distFromNearestTerrain = self.canvas.canvasWidth - nearestTerrainBefore.xCoord - nearestTerrainBefore.getWidthPixel(nearestTerrainBefore.width, Floor.width)
            print(distFromNearestObstacle, distFromNearestTerrain)
            distFromNearest = min(distFromNearestObstacle, distFromNearestTerrain)
            if distFromNearest < minDist:
                xCoord = self.canvas.canvasWidth + minDist - distFromNearest
            else:
                xCoord = self.canvas.canvasWidth
            yCoord = self.findTerrainHeight(xCoord)
            if yCoord == None: #terrain has not been geenrated
                return
            print(f'xcoord:{xCoord} ycoord:{yCoord}')
            obstacle = Obstacle(map = self, xCoord = xCoord, yCoord = yCoord)
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
        return None

    def findNearestObstacle(self, xCoord):
        if len(self.obstacleList) == 0:
            return None
        shortestDist = 100000
        nearestIndex = 0
        for obstacle in self.obstacleList:
            distance = xCoord - obstacle.obstacle.xCoord - obstacle.obstacle.width
            if distance < shortestDist:
                shortestDist = distance
                nearestIndex = self.obstacleList.index(obstacle)
        return nearestIndex
    
    def findNearestTerrain(self, xCoord):
        terrains = self.terrainList
        for terrainIndex in range(len(terrains)):
            terrain = terrains[terrainIndex]
            if terrain.xCoord <= xCoord <= terrain.xCoord + terrain.getWidthPixel(terrain.width, Floor.width):
                return terrainIndex

class Canvas: 
    def __init__(self, canvasWidth, canvasHeight):
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        


