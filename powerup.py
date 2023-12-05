from cmu_graphics import *

from imageHandling import *
import random

class PowerUp:
    width = 50
    height = 50
    image = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/boost.png')
    def __init__(self, map = None, xCoord = None, yCoord = None, width = None, height = None):
        self.map = map
        if xCoord == None: raise ValueError('xCoord not specified')
        else: self.xCoord = xCoord
        if yCoord == None: raise ValueError('yCoord not specified')
        else: self.yCoord = yCoord
        if width == None: self.width = 1
        else: self.width = width
        if height == None: self.height = 1
        else: self.height = height

    def drawPowerUp(self):
        #print(self.xCoord, self.yCoord, self.width, self.height)
        drawImage(self.image, self.xCoord, self.yCoord-self.getHeightPixel(self.height, PowerUp.height), 
                  width = self.getWidthPixel(self.width, PowerUp.width), 
                  height = self.getHeightPixel(self.height, PowerUp.height))

    def updateXCoord(self, step):
        self.xCoord += step

    @staticmethod
    def getWidthPixel(numBlocks, blockWidth):
        return numBlocks*blockWidth
    
    @staticmethod
    def getHeightPixel(numBlocks, blockHeight):
        return numBlocks*blockHeight
    