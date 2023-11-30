from cmu_graphics import *
from imageHandling import *
import random


class Terrain:
    #what is the terrain made of?
    #lets try a simple case of flat terrain
    minDistFromObstacle = 100
    def __init__(self, map = None, xCoord = None, yCoord = None, width = 0, height = 0):
        self.map = map
        if width == 0: self.width = random.randint(1,12) #width is number of blocks wide
        else: self.width = width 

        if self.obstacleTooClose(xCoord) or self.platformTooClose(xCoord):
            #print('obstacle too close')
            self.height = self.map.terrainList[-1].height
        else:
            if height == 0: self.height = random.randint(1,3) #height specified at 2 blocks  
            else: self.height = height

        self.xCoord = xCoord 

        self.yCoord = self.map.canvas.canvasHeight - self.getHeightPixel(self.height, Floor.height) #yCoord is dependent on height of terrain

    def obstacleTooClose(self, xCoord):
        minDistFromObstacle = 100
        
        #print(nearestObstacleIndex, len(self.map.obstacleList))
        if len(self.map.obstacleList) != 0: #non empty
            nearestObstacle = self.map.obstacleList[-1] #most recent obstacle
            distFromObstacle = xCoord-nearestObstacle.obstacle.xCoord-nearestObstacle.obstacle.width
            if distFromObstacle < minDistFromObstacle:
                return True
            else: return False
        return False
    
    def platformTooClose(self, xCoord):
        minDistFromPlatform = 100
        
        #print(nearestObstacleIndex, len(self.map.obstacleList))
        if len(self.map.platformList) != 0: #non empty
            nearestPlatform = self.map.platformList[-1] #most recent platform
            distFromPlatform = xCoord-nearestPlatform.xCoord-nearestPlatform.width
            if distFromPlatform < minDistFromPlatform:
                return True
            else: return False
        return False

    @staticmethod
    def getWidthPixel(numBlocks, blockWidth):
        return numBlocks*blockWidth

    @staticmethod
    def getHeightPixel(numBlocks, blockHeight):
        return numBlocks*blockHeight
    
    def drawTerrain(self):
        for rowIndex in range(self.height):
            for colIndex in range(self.width):
                xCoord = self.xCoord + self.getWidthPixel(colIndex, Floor.width)
                yCoord = self.yCoord + self.getHeightPixel(rowIndex, Floor.height)
                tile = Floor(xCoord, yCoord)
                tile.draw()

    def findYCoord(self, xCoord):
        for terrain in self.terrainList:
            if terrain.xCoord <= xCoord <= terrain.xCoord + terrain.length:
                return terrain.yCoord
        return None

    def updateXCoord(self, step):
        self.xCoord += step

class Floor: #floor is a building block of terrain
    width = 50
    height = 50
    fill = 'green'
    image = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/floor.png')
    def __init__(self, xCoord, yCoord):
        self.image = Floor.image
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.width = Floor.width
        self.height = Floor.height
        #self.fill = Floor.fill

    def draw(self):
        drawImage(self.image, self.xCoord, self.yCoord, width = self.width, height = self.height)
        #drawRect(self.xCoord, self.yCoord, self.width, self.height, fill = self.fill, border='black')