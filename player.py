from cmu_graphics import *
from terrain import *
from gamePlatform import *
from obstacles import *

class Player:
    def __init__(self, map):
        self.height = 50
        self.width = 50
        self.x = 50
        self.y = map.terrainList[0].yCoord
        self.map = map
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 1
        self.isJumping = False

    def updatePosition(self):
        ifLanded, _ = self.checkIfLanded()
        if not ifLanded or self.isJumping: #if jumping or jumping off, update position
            self.x += self.vx
            self.y += self.vy
            self.vx += self.ax
            self.vy += self.ay      
        ifLanded, heightLanded = self.checkIfLanded() #check if landed after updating position
        if ifLanded:
            self.vy = 0
            self.isJumping = False
            # terrainHeight = self.map.findTerrainHeight(self.x)
            # platformHeight = self.map.findPlatformHeight(self.x)
            self.y = heightLanded
            

    def checkIfLanded(self):
        terrainHeight = self.map.findTerrainHeight(self.x) 
        platformHeight = self.map.findPlatformHeight(self.x)
        if platformHeight != None and  (platformHeight-Tile.height <= self.y <= platformHeight): #check for landing on platforms
            return True, platformHeight - Tile.height
        if self.y >= terrainHeight:
            #print('landed')
            return True, terrainHeight
        # for platform in self.map.platformList:
        #     if self.y == platform.yCoord+platform.getHeightPixel(platform.height, Tile.height):
        #         return True
        # for obstacle in self.map.obstacleList:
        #     if self.y == obstacle.obstacle.yCoord+obstacle.obstacle.height:
        #         return True
        return False, 0
    
    def drawPlayer(self):
        #print(self.y)
        drawRect(self.x, self.y-self.height, self.width, self.height, fill = 'yellow', border='black')
    