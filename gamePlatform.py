from cmu_graphics import *
import random

class GamePlatform:
    def __init__(self, map, xCoord):
        self.map = map
        self.xCoord = xCoord
        self.yCoord = self.map.canvas.canvasHeight - random.randint(100, 150) #random height between 100-150
        self.platform = self.createPlatform()
    
    def createPlatform(self):
        platform = []
        numTiles = random.randint(1,5) #random length of platform between 1-5 tiles
        for i in range(numTiles):
            xCoord = self.xCoord + i*Tile.width
            yCoord = self.yCoord
            platform.append(Tile(xCoord, yCoord))
        return platform
    
    def drawPlatform(self):
        for tile in self.platform:
            tile.draw()

    def updateXCoord(self, step):
        for tile in self.platform:
            tile.xCoord += step

class Tile:
    width = 50
    height = 20
    def __init__(self, xCoord, yCoord):
        self.width = Tile.width
        self.height = Tile.height
        self.xCoord = xCoord
        self.yCoord = yCoord

    def draw(self):
        drawRect(self.xCoord, self.yCoord, self.width, self.height)