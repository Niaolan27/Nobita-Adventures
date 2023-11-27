import random
from cmu_graphics import *
from gamePlatform import *
from obstacles import *
from terrain import *
from player import *

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
            if self.checkLegalPlatform(platform):
                self.platformList.append(platform)
            #create obstacles for the starting map
        else:
            #create obstacles to add onto the map -> on the border of the canvas
            xCoord = self.canvas.canvasWidth #at the border of the canvas
            yCoord = self.findTerrainHeight(xCoord) - random.randint(100,150)
            platform = GamePlatform(map = self, xCoord = xCoord, yCoord = yCoord)
            if self.checkLegalPlatform(platform):
                self.platformList.append(platform)

    def createObstacle(self, start=False):
        if start == True:
            for i in range(3):
                xMin = i*self.canvas.canvasWidth//3
                xMax = xMin + self.canvas.canvasWidth//3
                xCoord = random.randint(xMin, xMax)
                yCoord = self.findTerrainHeight(xCoord)
                obstacle = Obstacle(map = self, xCoord = xCoord, yCoord = yCoord)
                if self.checkLegalObstacle(obstacle):
                    self.obstacleList.append(obstacle)
                #print(self.obstacleList)
            #create obstacles for the starting map
        else:
            #create obstacles to add onto the map -> on the border of the canvas
            xCoord = self.canvas.canvasWidth
            yCoord = self.findTerrainHeight(xCoord)
            obstacle = Obstacle(map = self, xCoord = xCoord, yCoord = yCoord)
            if self.checkLegalObstacle(obstacle):
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

    def removeObstacles(self):
        if self.obstacleList == []: return #non empty 
        firstObstacle = self.obstacleList[0]
        if firstObstacle.obstacle.xCoord + firstObstacle.obstacle.width <= -50:
            self.obstacleList.pop(0)
        #print(len(self.obstacleList))
        return

    def removePlatforms(self):
        if self.platformList == []: return #non empty
        firstPlatform = self.platformList[0]
        if firstPlatform.xCoord + firstPlatform.getWidthPixel(firstPlatform.width, Tile.width) <= -50: #add some buffer
            self.platformList.pop(0)
        #print(len(self.platformList))
        return

    def removeTerrains(self):
        if self.terrainList == []: return #non empty
        firstTerrain = self.terrainList[0]
        if firstTerrain.xCoord + firstTerrain.getWidthPixel(firstTerrain.width, Floor.width) <= -50:
            self.terrainList.pop(0)
        return

    def findTerrainHeight(self, xCoord):
        for terrain in self.terrainList:
            if terrain.xCoord <= xCoord <= terrain.xCoord + terrain.getWidthPixel(terrain.width, Floor.width):
                return terrain.yCoord
        return None
    
    # def findPlatformHeight(self, xCoord):
    #     for platform in self.platformList:
    #         #check if the back of player is on the platform
    #         if platform.xCoord <= xCoord <= platform.xCoord + platform.getWidthPixel(platform.width, Tile.width):
    #             return platform.yCoord
    #         #check if the front of player is on the platform
    #         elif platform.xCoord <= xCoord + Player.width <= platform.xCoord + platform.getWidthPixel(platform.width, Tile.width):
    #             return platform.yCoord
    #     return None
    
    def checkLegalObstacle(self, obstacle): #check if a piece legal
        minDistFromObstacle = 100
        minDistFromTerrain = 100
        #check if it is far enough from other obstacles
        otherObstacles = self.obstacleList
        for otherObstacle in otherObstacles:
            #other obstacles will definitely be before this 
            #print('checking obstacle distance')
            if obstacle.obstacle.xCoord - otherObstacle.obstacle.xCoord - otherObstacle.obstacle.width < minDistFromObstacle:
                return False
    
        #check if it is far enough from terrain 
        nearestTerrainIndex = self.findNearestTerrain(obstacle.obstacle.xCoord)

        #check terrain before
        try:
            #print('checking terrain before')
            terrainBefore = self.terrainList[nearestTerrainIndex-1]
            distanceFromBefore = obstacle.obstacle.xCoord - terrainBefore.xCoord - terrainBefore.getWidthPixel(terrainBefore.width, Floor.width)
            if distanceFromBefore < minDistFromTerrain:
                return False
        except IndexError:
            pass
        return True
    
    def checkLegalPlatform(self, platform): #check if a piece legal
        minDistFromPlatform = 100
        minDistFromTerrain = 100
        #check if it is far enough from other obstacles
        otherPlatforms = self.platformList
        for otherPlatform in otherPlatforms:
            #other obstacles will definitely be before this 
            #print('checking obstacle distance')

            if platform.xCoord - otherPlatform.xCoord - otherPlatform.getWidthPixel(otherPlatform.width, Tile.width) < minDistFromPlatform:
                return False
            
        nearestTerrainIndex = self.findNearestTerrain(platform.xCoord)

        #check terrain before
        try:
            #print('checking terrain before')
            terrainBefore = self.terrainList[nearestTerrainIndex-1]
            distanceFromBefore = platform.xCoord - terrainBefore.xCoord - terrainBefore.getWidthPixel(terrainBefore.width, Floor.width)
            if distanceFromBefore < minDistFromTerrain:
                return False
        except IndexError:
            pass
        return True
    
    def findNearestTerrain(self,xCoord):
        terrains = self.terrainList
        for terrainIndex in range(len(terrains)):
            if terrains[terrainIndex].xCoord <= xCoord <= terrains[terrainIndex].xCoord + terrains[terrainIndex].getWidthPixel(terrains[terrainIndex].width, Floor.width):
                nearestTerrainIndex = terrainIndex
        return nearestTerrainIndex
        #check distance from terrain before this terrain
        
    def findNearestObstacle(self,xCoord):
        obstacles = self.obstacleList
        shortestDistance = 100000
        nearestIndex = 0
        for obstacleIndex in range(len(obstacles)):
            obstacle = obstacles[obstacleIndex]
            distance = xCoord - obstacle.obstacle.xCoord - obstacle.obstacle.width
            if distance < shortestDistance:
                shortestDistance = distance
                nearestIndex = obstacleIndex
        return nearestIndex
    
    def findNextObstacle(self, xCoord):
        obstacles = self.obstacleList
        for obstacleIndex in range(len(obstacles)):
            obstacle = obstacles[obstacleIndex]
            if obstacle.obstacle.xCoord >= xCoord:
                return obstacle

    def findNextPlatform(self, xCoord):
        platforms = self.platformList
        for platformIndex in range(len(platforms)):
            platform = platforms[platformIndex]
            if platform.xCoord >= xCoord:
                return platform


class Canvas: 
    def __init__(self, canvasWidth, canvasHeight):
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight