from cmu_graphics import *
from terrain import *
from gamePlatform import *
from obstacles import *

class Player:
    height = 50
    width = 50
    def __init__(self, map):
        self.height = Player.height
        self.width = Player.width
        self.x = 50
        self.y = map.terrainList[0].yCoord
        self.map = map
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 2
        self.isJumping = False

    def updatePosition(self):
        #take a step and check if it is legal?
        self.x += self.vx
        self.y += self.vy
        self.vy += self.ay
        self.vx += self.ax

        #check if it is legal aka did it land or collide
        ifLanded, heightLanded = self.checkIfLanded()
        if ifLanded:
            #undo move
            self.x -= self.vx
            self.y = heightLanded
            self.vx -= self.ax
            #reset velocity
            self.vy = 0
            self.isJumping = False
        #elif not ifLanded or self.isJumping: #if jumping or jumping off, update position
        else:
            #check if player collides from below
            ifFromBelow, heightCollided = self.checkFromBelow()
            if ifFromBelow:
                #undo move
                self.x -= self.vx
                self.y = heightCollided
                self.vy = 0
                self.vy += self.ay
                self.vx -= self.ax
            else:
                pass

        

    def checkIfLanded(self): #return True/False for landing, and height of landing
        terrainHeight = self.map.findTerrainHeight(self.x) 
        platformHeight = self.map.findPlatformHeight(self.x)
        if platformHeight != None: #there is a platform
            platformTopEdge = platformHeight - Tile.height
            platformBottomEdge = platformHeight
            if (platformTopEdge <= self.y <= platformBottomEdge): #landing on platform from above 
                return True, platformHeight - Tile.height
        if self.y >= terrainHeight: #landing on terrain from above
            return True, terrainHeight
        return False, 0
    
    def checkFromBelow(self): #return True/False for colliding from below, and height of collision
        platformHeight = self.map.findPlatformHeight(self.x)
        if platformHeight != None: #there is a platform
            platformTopEdge = platformHeight - Tile.height
            platformBottomEdge = platformHeight
            if (platformTopEdge <= self.y - self.height <= platformBottomEdge): #colliding into the platform from below
                return True, platformHeight + self.height
        return False, 0
    
    def drawPlayer(self):
        #print(self.y)
        drawRect(self.x, self.y-self.height, self.width, self.height, fill = 'yellow', border='black')
    