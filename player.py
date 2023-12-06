from cmu_graphics import *
from terrain import *
from gamePlatform import *
from obstacles import *
from powerup import *
from PIL import Image
import os, pathlib
import time


class Player:
    height = 50
    width = 50
    speed = 10
    climbingSpeed = 10
    cadence = 5
    playerRunImage1 = getCMUImage('Images/doraemon_run1.png')
    playerRunImage2 = getCMUImage('Images/doraemon_run2.png')
    playerDeadImage = getCMUImage('Images/doraemon_dead.png')
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
        self.boostTimer = 0
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
            ifCollidedWithPowerUp, collidedPowerUp = self.checkIfCollidedWithPowerUp()
            ifCollidedWithRocket, collidedRocket = self.checkIfCollidedWithRocket()

            if ifLandedOnTerrain:
                self.y = heightLanded
                self.vy = 0
                self.isJumping = False
                self.isDoubleJumping = False
                self.stuck = False
                if self.boostTimer>0:
                    self.boostTimer += 1

            if ifCollidedWithTerrain:
                self.x -= Player.speed #undo the step forward
                self.vx = 0
                self.boostTimer = 0
                return
            
            if ifCollidedWithRocket:
                self.app.map.removeRockets(rocket = collidedRocket)
                self.x -= Player.speed
                self.die()
                return
                
            elif ifCollidedWithPlatform:
                platformHeight = collidedPlatform.yCoord
                platformXCoord = collidedPlatform.xCoord
                if platformCollisionDirection == 'top':
                    self.x -= Player.speed #undo the step forward
                    self.vx = Player.speed
                    self.y = platformHeight - Tile.height
                    self.vy = 0
                    self.ax = 0
                    self.isJumping = False
                    self.isDoubleJumping = False
                elif platformCollisionDirection == 'bottom':
                    self.x -= Player.speed
                    self.vx = Player.speed
                    self.y = platformHeight + self.height
                    self.vy = self.ay
                    self.ax = 0
                else:
                    self.x -= Player.speed
                    self.y -= self.vy
                    self.vx = 0
                    self.boostTimer = 0
                    self.vy = Player.climbingSpeed
                return

            elif ifCollidedWithObstacle:
                if type(collidedObstacle.obstacle) == Square: 
                
                    if obstacleCollisionDirection == 'front': #TODO
                        self.x -= Player.speed
                        self.vx = 0
                        self.boostTimer
                        self.ax = 0
                    else:
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
                    self.x -=Player.speed
                    self.vx = Player.speed//3
                    self.stuck = True

            elif ifCollidedWithPowerUp:
                self.x -= Player.speed
                self.vx = 1.5*Player.speed
                self.boostTimer = 1
                    
            else:
                self.x -= Player.speed
                if 0<self.boostTimer<10:
                    return
                self.vx = Player.speed

        
    
    def die(self):
        if self.deadTimer < 3:
            self.vx = 0
            self.boostTimer = 0
            self.dead = True
            if self.deadTimer > 0: #don't delay on the first time
                time.sleep(0.5)
            self.deadTimer += 1

            
        else:
            self.vx = Player.speed
            self.dead = False
            self.deadTimer = 0
            for obstacle in self.map.obstacleList: #respawn backwards
                obstacle.updateXCoord(self.map.removeBuffer//3)
            for platform in self.map.platformList:
                platform.updateXCoord(self.map.removeBuffer//3)
            for terrain in self.map.terrainList:
                terrain.updateXCoord(self.map.removeBuffer//3)
            for powerUp in self.map.powerUpList:
                powerUp.updateXCoord(self.map.removeBuffer//3)
            self.map.finishLine.updateXCoord(self.map.removeBuffer//3)


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
                    if abs(obstacleCenterX-playerCenterX) < abs(obstacleCenterY-playerCenterY): #collided from top
                        return True, obstacle, 'top'
                    else:
                        return True, obstacle, 'front'
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
                    if normHorDistance < normVerDistance:
                        if playerCenterY < platformCenterY:
                            return True, platform, 'top'
                        else:
                            return True, platform, 'bottom'
                    else:
                        return True, platform, 'front'
        return False, None, None
    
    def checkIfCollidedWithPowerUp(self):
        if self.map.powerUpList == []: return False, None
        for powerUp in self.map.powerUpList:
            if powerUp.xCoord - self.width <= self.x <= powerUp.xCoord+powerUp.width:
                playerCenterX = self.x + self.width//2
                playerCenterY = self.y - self.height//2
                powerUpCenterX = powerUp.xCoord + powerUp.getWidthPixel(powerUp.width, PowerUp.width)//2
                powerUpCenterY = powerUp.yCoord - powerUp.getHeightPixel(powerUp.height, PowerUp.height)//2
                if self.intersect(playerCenterX, playerCenterY, self.width, self.height,   
                                powerUpCenterX, powerUpCenterY, powerUp.getWidthPixel(powerUp.width, PowerUp.width), powerUp.getHeightPixel(powerUp.height, PowerUp.height)): #TODO
                    return True, powerUp
        return False, None
    
    def checkIfCollidedWithRocket(self):
        if self.map.rocketList == []: return False, None
        for rocket in self.map.rocketList:
            playerCenterX = self.x + self.width//2
            playerCenterY = self.y - self.height//2
            rocketCenterX = rocket.xCoord + rocket.width//2
            rocketCenterY = rocket.yCoord - rocket.height//2
            if self.intersect(playerCenterX, playerCenterY, self.width, self.height,   
                                rocketCenterX, rocketCenterY, rocket.width, rocket.height):
                return True, rocket
        return False, None
            
    
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
    
    def drawDeadPlayer(self):
        drawImage(self.playerDeadImage, self.x, self.y-self.height, width = self.width, height = self.height)

    @staticmethod
    def normalize(value, max):
        return value/max