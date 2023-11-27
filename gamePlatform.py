from cmu_graphics import *
import random

class GamePlatform:
    def __init__(self, map = None, xCoord = None, yCoord = None, width = None, height = None):
        self.map = map
        if xCoord == None: raise ValueError('xCoord not specified')
        else: self.xCoord = xCoord
        if yCoord == None: raise ValueError('yCoord not specified')
        else: self.yCoord = yCoord
        if width == None: self.width = random.randint(1,5)
        else: self.width = width
        if height == None: self.height = 1
        else: self.height = height
    
    def drawPlatform(self):
        for rowIndex in range(self.height):
            for colIndex in range(self.width):
                xCoord = self.xCoord + self.getWidthPixel(colIndex, Tile.width)
                yCoord = self.yCoord + self.getHeightPixel(rowIndex, Tile.height)
                tile = Tile(xCoord, yCoord)
                tile.draw()

    def updateXCoord(self, step):
        self.xCoord += step

    @staticmethod
    def getWidthPixel(numBlocks, blockWidth):
        return numBlocks*blockWidth
    
    @staticmethod
    def getHeightPixel(numBlocks, blockHeight):
        return numBlocks*blockHeight
    
class Tile:
    width = 50
    height = 20
    def __init__(self, xCoord, yCoord):
        self.width = Tile.width
        self.height = Tile.height
        self.xCoord = xCoord
        self.yCoord = yCoord

    def draw(self):
        drawRect(self.xCoord, self.yCoord - self.height, self.width, self.height)