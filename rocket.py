from imageHandling import *
from gamePlatform import *
from terrain import *
from obstacles import *
import math

class Rocket:
    image = getCMUImage('Images/rocket.png')
    width = 30
    height = 30
    def __init__(self, map, xCoord, yCoord):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.angle = 180
        self.v = 10
        self.vx = self.calculateVx(self.v, self.angle)
        self.vy = self.calculateVy(self.v, self.angle)
        self.width = Rocket.width
        self.height = Rocket.height
        self.diagonal = (2**0.5) * self.width//2
        self.image = Rocket.image
        self.map = map

    def updatePosition(self):
        self.xCoord += self.vx
        self.yCoord += self.vy

    def updateAngleAndVelocity(self, playerX, playerY):
        deltaX = playerX - self.xCoord
        deltaY = playerY - self.yCoord
        self.angle = math.atan(deltaY/deltaX) / math.pi * 180
        if self.angle < 0:
            self.angle += 180
        self.vx = self.calculateVx(self.v, self.angle)
        self.vy = self.calculateVy(self.v, self.angle)

    def updateXCoord(self, step):
        self.xCoord += step

    def drawRocket(self):
        drawImage(self.image, self.xCoord, self.yCoord, width = 30, height = 30, rotateAngle = self.angle)

    def checkCollision(self):
        obstacles = self.map.obstacleList
        platforms = self.map.platformList
        terrainIndex = self.map.findNearestTerrain(self.xCoord)
        terrain = self.map.terrainList[terrainIndex]
        
        # rocketCenterX = self.rocketCenterXHelper(self.xCoord)
        # rocketCenterY = self.rocketCenterYHelper(self.yCoord)
        rocketBoundingWidth = self.getBoundingWidth()
        rocketBoundingHeight = self.getBoundingHeight()
        #print(self.xCoord, self.yCoord)
        rocketCenterX = self.xCoord + rocketBoundingWidth//2
        rocketCenterY = self.yCoord - rocketBoundingHeight//2
        #print(rocketBoundingWidth, rocketBoundingHeight)
        #print(rocketCenterX, rocketCenterY)
        # playerCenterX = self.x + self.width//2
        # playerCenterY = self.y - self.height//2
        # powerUpCenterX = powerUp.xCoord + powerUp.getWidthPixel(powerUp.width, PowerUp.width)//2
        # powerUpCenterY = powerUp.yCoord - powerUp.getHeightPixel(powerUp.height, PowerUp.height)//2
        for obstacle in obstacles:
            obstacleCenterX = obstacle.obstacle.xCoord + obstacle.obstacle.width//2
            obstacleCenterY = obstacle.obstacle.yCoord - obstacle.obstacle.height//2
            if self.intersect(rocketCenterX, rocketCenterY, rocketBoundingWidth, rocketBoundingHeight, obstacleCenterX, obstacleCenterY, obstacle.obstacle.width, obstacle.obstacle.height):
                self.map.removeRockets(rocket = self)
        for platform in platforms:
            platformCenterX = platform.xCoord + platform.getWidthPixel(platform.width, Tile.width)//2
            platformCenterY = platform.yCoord - platform.getHeightPixel(platform.height, Tile.height)//2
            if self.intersect(rocketCenterX, rocketCenterY, rocketBoundingWidth, rocketBoundingHeight, platformCenterX, platformCenterY, platform.getWidthPixel(platform.width, Tile.width), platform.getHeightPixel(platform.height, Tile.height)):
                self.map.removeRockets(rocket = self)
        if rocketCenterY + rocketBoundingHeight >= terrain.yCoord:
            self.map.removeRockets(rocket = self)

    @staticmethod
    def calculateVx(v, angle):
        return v*math.cos(angle/180*math.pi)
    
    @staticmethod
    def calculateVy(v, angle):
        return v*math.sin(angle/180*math.pi)
    
    @staticmethod
    def intersect(x1,y1,w1,h1,x2,y2,w2,h2):
        if abs(x1-x2) < (w1+w2)//2 and abs(y1-y2) < (h1+h2)//2:
            return True
        return False

    def getBoundingWidth(self):
        alpha = 45 - self.angle
        width = abs(2*self.diagonal*math.cos(alpha/180*math.pi))
        height = abs(2*self.diagonal*math.sin(alpha/180*math.pi))
        return max(width,height)
    
    def getBoundingHeight(self):
        alpha = 45 - self.angle
        width = abs(2*self.diagonal*math.cos(alpha/180*math.pi))
        height = abs(2*self.diagonal*math.sin(alpha/180*math.pi))
        return max(width,height)
    
    def rocketCenterYHelper(self, yCoord):
        alpha = 45-self.angle
        height = self.diagonal*math.sin(alpha/180*math.pi)
        return yCoord - height
    
    def rocketCenterXHelper(self, xCoord):
        alpha = 45-self.angle
        width = self.diagonal*math.cos(alpha/180*math.pi)
        return xCoord + width