from cmu_graphics import *
import random

class Terrain:
    #what is the terrain made of?
    #lets try a simple case of flat terrain
    def __init__(self, map):
        self.map = map
        self.terrainList = []
        self.terrainCount = 20
        self.terrainInterval = self.map.canvas.canvasWidth//self.terrainCount
        self.createTerrain()
    
    def createTerrain(self):
        #let's say i split the canvas into three parts to make three sections of terrain
        for index in range(self.terrainCount):
            height = random.choices([50, 100], weights = [0.5, 0.5])[0]
            xCoord = index*self.terrainInterval
            yCoord = self.map.canvas.canvasHeight - height
            terrain = Floor(xCoord, yCoord, self.terrainInterval, height) #xCoord, yCoord, length, height
            # if i specify length and height, i can make the terrain scale accordingly -> generate more interesting terrains
            self.terrainList.append(terrain)
        
    
    def findYCoord(self, xCoord):
        for terrain in self.terrainList:
            if terrain.xCoord <= xCoord <= terrain.xCoord + terrain.length:
                return terrain.yCoord
        return None
    def drawTerrain(self):
        for terrain in self.terrainList:
            #print(terrain.yCoord)
            terrain.draw()

    def updateXCoord(self, step):
        for terrain in self.terrainList:
            terrain.xCoord += step

class Floor: #floor is a building block of terrain
    def __init__(self, xCoord, yCoord, length, height):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.length = length
        self.height = height

    def draw(self):
        drawRect(self.xCoord, self.yCoord, self.length, self.height, fill = 'green')