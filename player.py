from cmu_graphics import *
from terrain import *
from gamePlatform import *
from obstacles import *
from PIL import Image
import os, pathlib
import time


class Player:
    height = 50
    width = 50
    speed = 10
    climbingSpeed = 10
    cadence = 5
    playerRunImage1 = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/doraemon_run1.png')
    playerRunImage2 = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/doraemon_run2.png')
    playerDeadImage = getCMUImage('/users/Jason/CMU/15112/Term Project/Speedrunners/Images/doraemon_dead.png')
    def __init__(self, app):
        self.app = app
        self.map = app.map
        self.height = Player.height
        self.width = Player.width
        self.x = 50
        self.y = app.map.terrainList[0].yCoord
        self.vx = Player.speed
        self.vy = 0
        self.ax = 0
        self.ay = 2
        self.dead = False
        self.deadTimer = 0
        self.isJumping = False
        self.isDoubleJumping = False
        self.cadence = Player.cadence
        self.playerRunImage1 = Player.playerRunImage1
        self.playerRunImage2 = Player.playerRunImage2

    def updatePosition(self):
        #take a step and check the legality of the move
        if self.dead: #if dead, pause for a moment
            self.die()
        else:
            self.y += self.vy
            self.x += Player.speed
            self.vy += self.ay

            #do the checks
            ifLandedOnTerrain, heightLanded = self.checkIfLandedOnTerrain()
            ifCollidedWithPlatform, collidedPlatform, platformCollisionDirection = self.checkIfCollidedWithPlatform()
            ifCollidedWithObstacle, collidedObstacle, obstacleCollisionDirection = self.checkIfCollidedWithObstacle()
            ifCollidedWithTerrain, collidedTerrain = self.checkIfCollideWithTerrain()

            if ifLandedOnTerrain:
                self.y = heightLanded
                self.vy = 0
                self.isJumping = False
                self.isDoubleJumping = False
                self.stuck = False

            if ifCollidedWithTerrain:
                #print('collided with terrain')
                self.x -= Player.speed #undo the step forward
                self.vx = 0
                return
                
            if ifCollidedWithPlatform:
                #print('collided with platform')
                platformHeight = collidedPlatform.yCoord
                platformXCoord = collidedPlatform.xCoord
                if platformCollisionDirection == 'top':
                    #print('collided from top')
                    self.x -= Player.speed #undo the step forward
                    self.vx = Player.speed
                    self.y = platformHeight - Tile.height
                    self.vy = 0
                    self.ax = 0
                    self.isJumping = False
                    self.isDoubleJumping = False
                elif platformCollisionDirection == 'bottom':
                    #print('collided from bottom')
                    self.x -= Player.speed
                    self.vx = Player.speed
                    self.y = platformHeight + self.height
                    self.vy = self.ay
                    self.ax = 0
                else:
                    #print('collided from front')
                    self.x -= Player.speed
                    self.y -= self.vy
                    self.vx = 0
                    self.vy = Player.climbingSpeed
                    #self.ax = 0.5
                return

            if ifCollidedWithObstacle:
                if type(collidedObstacle.obstacle) == Square: 
                #print('collided with obstacle')
                    if obstacleCollisionDirection == 'front': #TODO
                        #print('collided from front')
                        self.x -= Player.speed
                        self.vx = 0
                        self.ax = 0
                    else:
                        #print('collided from top')
                        self.x -= Player.speed
                        self.vx = Player.speed
                        self.y = collidedObstacle.obstacle.yCoord - collidedObstacle.obstacle.height
                        self.vy = 0
                        self.ax = 0
                    return
                elif type(collidedObstacle.obstacle) == Fire:
                    self.x -= Player.speed
                    self.die()
                elif type(collidedObstacle.obstacle) == Glue:
                    #print('glue')
                    #print(self.vx)
                    self.x -=Player.speed
                    self.vx = Player.speed//3
                    self.stuck = True
                    
            else:
                self.x-=Player.speed
                self.vx = Player.speed
    
    def die(self):
        #print(self.x)
        if self.deadTimer < 3:
            self.vx = 0
            self.dead = True
            if self.deadTimer > 0: #don't delay on the first time
                time.sleep(0.5)
            self.deadTimer += 1

            
        else:
            self.vx = Player.speed
            self.dead = False
            self.deadTimer = 0
            for obstacle in self.map.obstacleList: #respawn backwards
                obstacle.updateXCoord(self.map.removeBuffer)
            for platform in self.map.platformList:
                platform.updateXCoord(self.map.removeBuffer)
            for terrain in self.map.terrainList:
                terrain.updateXCoord(self.map.removeBuffer)
            self.map.finishLine.updateXCoord(self.map.removeBuffer)


    def checkIfCollideWithTerrain(self):
        try:
            nearestTerrainIndex = self.map.findNearestTerrain(self.x)
            nextTerrain = self.map.terrainList[nearestTerrainIndex+1]
            playerCenterX = self.x + self.width//2
            playerCenterY = self.y - self.height//2
            terrainCenterX = nextTerrain.xCoord + nextTerrain.getWidthPixel(nextTerrain.width, Floor.width)//2
            terrainCenterY = nextTerrain.yCoord + nextTerrain.getHeightPixel(nextTerrain.height, Floor.height)//2
            if self.intersect(playerCenterX, playerCenterY, self.width, self.height,   
                                    terrainCenterX, terrainCenterY, 
                                    nextTerrain.getWidthPixel(nextTerrain.width, Floor.width), 
                                    nextTerrain.getHeightPixel(nextTerrain.height, Floor.height)):
                return True, nextTerrain
            return False, None
        except IndexError: #next terrain not generated yet
            return False, None

    def checkIfCollidedWithObstacle(self):
        if self.map.obstacleList == []: return False, None, None
        for obstacle in self.map.obstacleList:
            if obstacle.obstacle.xCoord - self.width <= self.x <= obstacle.obstacle.xCoord+obstacle.obstacle.width:
                playerCenterX = self.x + self.width//2
                playerCenterY = self.y - self.height//2
                obstacleCenterX = obstacle.obstacle.xCoord + obstacle.obstacle.width//2
                obstacleCenterY = obstacle.obstacle.yCoord - obstacle.obstacle.height//2
                if self.intersect(playerCenterX, playerCenterY, self.width, self.height,   
                                obstacleCenterX, obstacleCenterY, obstacle.obstacle.width, obstacle.obstacle.height): #TODO
                    #print('intersect')
                    if abs(obstacleCenterX-playerCenterX) < abs(obstacleCenterY-playerCenterY): #collided from top
                        return True, obstacle, 'top'
                    else:
                        return True, obstacle, 'front'
                #print('no intersect')
        return False, None, None

    def checkIfCollidedWithPlatform(self):
        for platform in self.map.platformList:
            if platform == None: return False, None
            if platform.xCoord - self.width <= self.x <= platform.xCoord + platform.getWidthPixel(platform.width, Tile.width):
                playerCenterX = self.x + self.width//2
                playerCenterY = self.y - self.height//2
                platformCenterX = platform.xCoord + platform.getWidthPixel(platform.width, Tile.width)//2
                platformCenterY = platform.yCoord - platform.getHeightPixel(platform.height, Tile.height)//2
                platformWidth = platform.getWidthPixel(platform.width, Tile.width)
                platformHeight = platform.getHeightPixel(platform.height, Tile.height)
                if self.intersect(playerCenterX, playerCenterY, self.width, self.height,   
                                platformCenterX, platformCenterY, 
                                platformWidth, 
                                platformHeight):
                    #trying with normalize
                    horDistance = abs(playerCenterX - platformCenterX)
                    maxHorDistance = (self.width + platformWidth)//2
                    verDistance = abs(playerCenterY - platformCenterY)
                    maxVerDistance = (self.height+platformHeight)//2
                    normHorDistance = self.normalize(horDistance, maxHorDistance)
                    normVerDistance = self.normalize(verDistance, maxVerDistance)
                    #print(normHorDistance, normVerDistance)
                    if normHorDistance < normVerDistance:
                        if playerCenterY < platformCenterY:
                            return True, platform, 'top'
                        else:
                            return True, platform, 'bottom'
                    else:
                        return True, platform, 'front'
                    # if self.x > platform.xCoord: #either top or bottom
                    #     #print('top or bottom')
                    #     if self.y > platform.yCoord + 8: #impossible for a player to penetrate from the bottom with this condition
                    #         #this condition is used to prevent players from phasing through from the top
                    #         return True, platform, 'bottom'
                    #     else:
                    #         return True, platform, 'top'
                    # else:
                    #     #print('top bottom front')
                    #     vertEdgeDistance = self.x + self.width - platform.xCoord
                    #     #bottomEdgeDistance = abs(self.y - platform.yCoord)
                    #     #topEdgeDistance = abs((self.y-self.height)-(platform.yCoord-platformHeight))
                    #     bottomEdgeDistance = platform.yCoord - (self.y-self.height)
                    #     topEdgeDistance = self.y -(platform.yCoord-platformHeight)
                    #     #print(vertEdgeDistance, bottomEdgeDistance, topEdgeDistance)
                    #     if vertEdgeDistance < bottomEdgeDistance+10 and vertEdgeDistance < topEdgeDistance+10:
                    #         return True, platform, 'front'
                    #     else:
                    #         if self.y > platform.yCoord:
                    #             return True, platform, 'bottom'
                    #         else:
                    #             return True, platform, 'top'
        return False, None, None
    
    @staticmethod
    def intersect(x1,y1,w1,h1,x2,y2,w2,h2):
        if abs(x1-x2) < (w1+w2)//2 and abs(y1-y2) < (h1+h2)//2:
            return True
        return False
    
    def checkIfLandedOnTerrain(self): #return True/False for landing, and height of landing
        terrainHeight = self.map.findTerrainHeight(self.x) 
        if self.y >= terrainHeight:
            return True, terrainHeight
        return False, 0
    
    def drawPlayer(self, imageIndex):
        if imageIndex == 0:
            drawImage(self.playerRunImage1, self.x, self.y-self.height, width = self.width, height = self.height)
        else:
            drawImage(self.playerRunImage2, self.x, self.y-self.height, width = self.width, height = self.height)
        #drawRect(self.x, self.y-self.height, self.width, self.height, fill = 'yellow', border='black')
    
    def drawDeadPlayer(self):
        drawImage(self.playerDeadImage, self.x, self.y-self.height, width = self.width, height = self.height)

    @staticmethod
    def normalize(value, max):
        return value/max
    
#https://realpython.com/python-sleep/