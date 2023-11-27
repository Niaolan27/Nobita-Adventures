from cmu_graphics import *
from terrain import *
from gamePlatform import *
from obstacles import *

class Player:
    height = 50
    width = 50
    speed = 10
    def __init__(self, map):
        self.height = Player.height
        self.width = Player.width
        self.x = 50
        self.y = map.terrainList[0].yCoord
        self.map = map
        self.vx = Player.speed
        self.vy = 0
        self.ax = 0
        self.ay = 2
        self.isJumping = False
        self.isDoubleJumping = False

    # def updatePosition(self):
    #     #take a step and check if it is legal?
    #     self.x += self.vx
    #     self.y += self.vy
    #     self.vy += self.ay
    #     self.vx += self.ax

    #     #check if it is legal aka did it land or collide
    #     ifLanded, heightLanded = self.checkIfLanded()
    #     if ifLanded:
    #         #undo move
    #         self.x -= self.vx
    #         self.y = heightLanded
    #         self.vx -= self.ax
    #         #reset velocity
    #         self.vy = 0
    #         self.isJumping = False
    #     #elif not ifLanded or self.isJumping: #if jumping or jumping off, update position
    #     else:
    #         #check if player collides from below
    #         ifFromBelow, heightCollided = self.checkFromBelow()
    #         if ifFromBelow:
    #             #undo move
    #             self.x -= self.vx
    #             self.y = heightCollided
    #             self.vy = 0
    #             self.vy += self.ay
    #             self.vx -= self.ax
    #         else:
    #             pass
    #     return

    def updatePosition(self):
        #print(self.y, self.vy)
        #self.x += self.vx
        self.y += self.vy
        self.vy += self.ay

        #check if it is legal aka did it land or collide
        ifLandedOnTerrain, heightLanded = self.checkIfLandedOnTerrain()
        ifCollidedWithPlatform, collidedPlatform, platformCollisionDirection = self.checkIfCollidedWithPlatform()
        ifCollidedWithObstacle, collidedObstacle, obstacleCollisionDirection = self.checkIfCollidedWithObstacle()
        #ifCollidedWithTerrain, collidedTerrain = self.checkIfCollideWithTerrain()
        if ifLandedOnTerrain:
            #undo move
            #self.x -= self.vx
            self.y = heightLanded
            self.vx = Player.speed
            self.ax = 0
            #reset velocity
            self.vy = 0
            self.isJumping = False
            self.isDoubleJumping = False

        if ifCollidedWithPlatform:
            #print('collided with platform')
            platformHeight = collidedPlatform.yCoord
            platformXCoord = collidedPlatform.xCoord
            if platformCollisionDirection == 'top':
                print('collided from top')
                #self.x -= self.vx
                self.vx = Player.speed
                self.y = platformHeight - Tile.height
                self.vy = 0
                self.ax = 0
                self.isJumping = False
                self.isDoubleJumping = False
            elif platformCollisionDirection == 'bottom':
                print('collided from bottom')
                #self.x -= self.vx
                self.vx = Player.speed
                self.y = platformHeight + self.height
                self.vy = self.ay
                self.ax = 0
            else:
                print('collided from front')
                #self.x = platformXCoord - self.width
                self.y -= self.vy
                self.vx = -3
                self.vy += self.ay
                self.ax = 0.5

        if ifCollidedWithObstacle:
            print('collided with obstacle')
            # obstacleYCoord = self.map.findObstacleYCoord(self.x)
            # obstacleXCoord = self.map.findObstacleXCoord(self.x) 
            if obstacleCollisionDirection == 'front': #TODO
                print('collided from front')
                #self.x = collidedObstacle.obstacle.xCoord - self.width
                #self.y -= self.vy
                self.vx = 0
                self.ax = 0
            else:
                print('collided from top')
                #self.x -= self.vx
                self.vx = Player.speed
                self.y = collidedObstacle.obstacle.yCoord - collidedObstacle.obstacle.height
                self.vy = 0
                self.ax = 0
        else:
            self.vx = Player.speed

    def checkIfCollidedWithObstacle(self):
        if self.map.obstacleList == []: return False, None, None
        for obstacle in self.map.obstacleList:
            if obstacle.obstacle.xCoord - self.width <=self.x<= obstacle.obstacle.xCoord:
                playerCenterX = self.x + self.width//2
                playerCenterY = self.y - self.height//2
                obstacleCenterX = obstacle.obstacle.xCoord + obstacle.obstacle.width//2
                obstacleCenterY = obstacle.obstacle.yCoord - obstacle.obstacle.height//2
                #print(playerCenterY, obstacleCenterY)
                if self.intersect(playerCenterX, playerCenterY, self.width, self.height,   
                                obstacleCenterX, obstacleCenterY, obstacle.obstacle.width, obstacle.obstacle.height): #TODO
                    #print('intersect')
                    if abs(obstacleCenterX-playerCenterX) < abs(obstacleCenterY-playerCenterY): #collided from top
                        return True, obstacle, 'top'
                    else:
                        return True, obstacle, 'front'
                #print('no intersect')
                # if obstacleCenterX-playerCenterX  == (self.width + obstacle.obstacle.width)//2:
                #     return True, obstacle, 'front'
                # else:
                #     return True, obstacle, 'top'
        return False, None, None

    def checkIfCollidedWithPlatform(self):
        for platform in self.map.platformList:
            if platform == None: return False, None
            if platform.xCoord - self.width <=self.x <= platform.xCoord + platform.getWidthPixel(platform.width, Tile.width):
                playerCenterX = self.x + self.width//2
                playerCenterY = self.y - self.height//2
                platformCenterX = platform.xCoord + platform.getWidthPixel(platform.width, Tile.width)//2
                platformCenterY = platform.yCoord - platform.getHeightPixel(platform.height, Tile.height)//2
                # print(playerCenterY, platformCenterY)
                if self.intersect(playerCenterX, playerCenterY, self.width, self.height,   
                                platformCenterX, platformCenterY, 
                                platform.getWidthPixel(platform.width, Tile.width), 
                                platform.getHeightPixel(platform.height, Tile.height)):
                    if platformCenterX - playerCenterX == (self.width + platform.getWidthPixel(platform.width, Tile.width))//2:
                        #print(playerCenterX, platformCenterX)
                        #print(self.width, platform.getWidthPixel(platform.width, Tile.width))
                        return True, platform, 'front'
                    if platformCenterY > playerCenterY: #player is above platform
                        return True, platform, 'top'
                    else:
                        return True, platform, 'bottom' #player is below platform
        return False, None, None
    
    @staticmethod
    def intersect(x1,y1,w1,h1,x2,y2,w2,h2):
        if abs(x1-x2) <= (w1+w2)//2 and abs(y1-y2) <= (h1+h2)//2:
            return True
        return False
    
    def checkIfLandedOnTerrain(self): #return True/False for landing, and height of landing
        terrainHeight = self.map.findTerrainHeight(self.x) 
        if self.y >= terrainHeight:
            return True, terrainHeight
        return False, 0
        

    # def checkIfLanded(self): #return True/False for landing, and height of landing
    #     terrainHeight = self.map.findTerrainHeight(self.x) 
    #     platformHeight = self.map.findPlatformHeight(self.x)
    #     if platformHeight != None: #there is a platform
    #         platformTopEdge = platformHeight - Tile.height
    #         platformBottomEdge = platformHeight
    #         if (platformTopEdge <= self.y <= platformBottomEdge): #landing on platform from above 
    #             return True, platformHeight - Tile.height
    #     if self.y >= terrainHeight: #landing on terrain from above
    #         return True, terrainHeight
    #     return False, 0
    
    # def checkFromBelow(self): #return True/False for colliding from below, and height of collision
    #     platformHeight = self.map.findPlatformHeight(self.x)
    #     if platformHeight != None: #there is a platform
    #         platformTopEdge = platformHeight - Tile.height
    #         platformBottomEdge = platformHeight
    #         if (platformTopEdge <= self.y - self.height <= platformBottomEdge): #colliding into the platform from below
    #             return True, platformHeight + self.height
    #     return False, 0
    
    def drawPlayer(self):
        #print(self.y)
        drawRect(self.x, self.y-self.height, self.width, self.height, fill = 'yellow', border='black')
    