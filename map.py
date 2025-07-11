from cmu_graphics import *
from gamePlatform import *
from obstacles import *
from terrain import *
from player import *
from level import *
from imageHandling import *
from powerup import *
from rocket import *
from PIL import Image
import random
import os, pathlib

class Map:
    def __init__(self, app, canvas = None):
        self.app = app
        self.removeBuffer = 400
        self.canvas = Canvas(canvas[0], canvas[1]) #generate a long canvas -> can change the length of canvas to make game longer or shorter
        self.terrainList = []
        self.obstacleList = []
        self.platformList = []
        self.powerUpList = []
        self.rocketList = []
        self.finishDistance = 7000
        self.background = app.levelSelected.background
        self.createMap(app)
    
    def createMap(self, app): #generates a map with obstacles and platforms -> can include parameter for level difficulty
        self.createTerrain(app, start=True)
        self.createObstacle(app, start=True)
        self.createPlatform(app, start=True)
        self.createFinishLine(app)
        
    def createPlatform(self, app, start=False):
        if start == True:
            xMin = 0
            xMax = self.canvas.canvasWidth
            xCoord = random.randint(xMin, xMax)
            yCoord = self.findTerrainHeight(xCoord) - random.randint(100,150)
            platform = GamePlatform(map = self, xCoord = xCoord, yCoord = yCoord)
            if self.checkLegalPlatform(platform):
                self.platformList.append(platform)
            #create obstacles for the starting map
        else:
            #create obstacles to add onto the map -> on the border of the canvas
            xCoord = self.canvas.canvasWidth #at the border of the canvas
            yCoord = self.findTerrainHeight(xCoord) - random.randint(100,150)
            platform = GamePlatform(map = self, xCoord = xCoord, yCoord = yCoord)
            if self.checkLegalPlatform(platform):
                self.platformList.append(platform)

    def createObstacle(self, app, start=False):
        if start == True:
            for i in range(3):
                xMin = i*self.canvas.canvasWidth//3
                xMax = xMin + self.canvas.canvasWidth//3
                xCoord = random.randint(xMin, xMax)
                yCoord = self.findTerrainHeight(xCoord)
                obstacle = Obstacle(map = self, xCoord = xCoord, yCoord = yCoord)
                if self.checkLegalObstacle(obstacle):
                    self.obstacleList.append(obstacle)
            #create obstacles for the starting map
        else:
            #create obstacles to add onto the map -> on the border of the canvas
            xCoord = self.canvas.canvasWidth
            yCoord = self.findTerrainHeight(xCoord)
            obstacle = Obstacle(map = self, xCoord = xCoord, yCoord = yCoord)
            if self.checkLegalObstacle(obstacle):
                self.obstacleList.append(obstacle)
    
    def createTerrain(self, app, start=False):
        if start == True:
            #create a starting terrain
            numBlocks = self.canvas.canvasWidth//Floor.width
            terrain = Terrain(map = self, width = numBlocks, xCoord = 0) #returns a terrain object
        else:
            #create a terrain to add onto the map
            terrain = Terrain(map = self, xCoord = self.canvas.canvasWidth)
        self.terrainList.append(terrain)

    def createPowerUp(self, app, start=False):
        xCoord = self.canvas.canvasWidth
        yCoord = self.findTerrainHeight(xCoord)
        powerUp = PowerUp(map = self, xCoord = self.canvas.canvasWidth, yCoord = yCoord)
        if self.checkLegalPowerUp(powerUp):
            self.powerUpList.append(powerUp)
    
    def createFinishLine(self, app):
        self.finishLine = FinishLine(app, self.finishDistance, 50)

    def createRocket(self, app):
        xCoord = self.canvas.canvasWidth
        yCoord = 50 #arbitrary height
        rocket = Rocket(map = self, xCoord = xCoord, yCoord = yCoord)
        self.rocketList.append(rocket)


    def removeObstacles(self):
        if self.obstacleList == []: return #non empty 
        firstObstacle = self.obstacleList[0]
        if firstObstacle.obstacle.xCoord + firstObstacle.obstacle.width <= -self.removeBuffer:
            self.obstacleList.pop(0)
        return

    def removePlatforms(self):
        if self.platformList == []: return #non empty
        firstPlatform = self.platformList[0]
        if firstPlatform.xCoord + firstPlatform.getWidthPixel(firstPlatform.width, Tile.width) <= -self.removeBuffer: #add some buffer
            self.platformList.pop(0)
        return

    def removeTerrains(self):
        if self.terrainList == []: return #non empty
        firstTerrain = self.terrainList[0]
        if firstTerrain.xCoord + firstTerrain.getWidthPixel(firstTerrain.width, Floor.width) <= -self.removeBuffer:
            self.terrainList.pop(0)
        return
    
    def removePowerUps(self):
        if self.powerUpList == []: return #non empty
        firstPowerUp = self.powerUpList[0]
        if firstPowerUp.xCoord + firstPowerUp.getWidthPixel(firstPowerUp.width, PowerUp.width) <= -self.removeBuffer:
            self.powerUpList.pop(0)
        return
    
    def removeRockets(self, rocket = None):
        if rocket != None:
            try:
                self.rocketList.remove(rocket) #if a rocket is specified
            except ValueError:
                pass
        else:
            if self.rocketList == []: return
            firstRocket = self.rocketList[0]
            if firstRocket.xCoord + firstRocket.width <= 0: #the moment the rocket disappears, pop it
                self.rocketList.pop(0)

    def findTerrainHeight(self, xCoord):
        for terrain in self.terrainList:
            if terrain.xCoord <= xCoord <= terrain.xCoord + terrain.getWidthPixel(terrain.width, Floor.width):
                return terrain.yCoord
        return None
    
    def checkLegalObstacle(self, obstacle): #check if a piece legal
        #does not check for platform; it is fine to have obstacles below platforms
        minDistFromObstacle = 150
        minDistFromTerrain = 150
        minDistFromPowerUp = 150
        #check if it is far enough from other obstacles
        otherObstacles = self.obstacleList
        for otherObstacle in otherObstacles:
            #other obstacles will definitely be before this 
            if obstacle.obstacle.xCoord - otherObstacle.obstacle.xCoord - otherObstacle.obstacle.width < minDistFromObstacle:
                return False
        
        powerUps = self.powerUpList
        for powerUp in powerUps:
            if obstacle.obstacle.xCoord - powerUp.xCoord - powerUp.getWidthPixel(powerUp.width, PowerUp.width) < minDistFromPowerUp:
                return False
    
        #check if it is far enough from terrain 
        nearestTerrainIndex = self.findNearestTerrain(obstacle.obstacle.xCoord)

        #check terrain before
        try:
            terrainBefore = self.terrainList[nearestTerrainIndex-1]
            distanceFromBefore = obstacle.obstacle.xCoord - terrainBefore.xCoord - terrainBefore.getWidthPixel(terrainBefore.width, Floor.width)
            if distanceFromBefore < minDistFromTerrain:
                return False
        except IndexError:
            pass
        return True
    
    def checkLegalPowerUp(self, powerUp):
        #does not check for platform
        minDistFromObstacle = 150
        minDistFromTerrain = 150
        minDistFromPowerUp = 150
        #check if it is far enough from other obstacles
        otherObstacles = self.obstacleList
        for otherObstacle in otherObstacles:
            #other obstacles will definitely be before this 
            if powerUp.xCoord - otherObstacle.obstacle.xCoord - otherObstacle.obstacle.width < minDistFromObstacle:
                return False
        otherPowerUps = self.powerUpList
        for otherPowerUp in otherPowerUps:
            if powerUp.xCoord - otherPowerUp.xCoord - otherPowerUp.getWidthPixel(otherPowerUp.width, PowerUp.width) < minDistFromPowerUp:
                return False
        #check if it is far enough from terrain 
        nearestTerrainIndex = self.findNearestTerrain(powerUp.xCoord)

        #check terrain before
        try:
            terrainBefore = self.terrainList[nearestTerrainIndex-1]
            distanceFromBefore = powerUp.xCoord - terrainBefore.xCoord - terrainBefore.getWidthPixel(terrainBefore.width, Floor.width)
            if distanceFromBefore < minDistFromTerrain:
                return False
        except IndexError:
            pass
        return True
    
    def checkLegalPlatform(self, platform): #check if a piece legal
        #does not check with obstacles, it is fine to have platforms on top of obstacles
        minDistFromPlatform = 150
        minDistFromTerrain = 150
        minDistFromPowerUp = 150
        #check if it is far enough from other obstacles
        otherPlatforms = self.platformList
        for otherPlatform in otherPlatforms:
            #other obstacles will definitely be before this 
            if platform.xCoord - otherPlatform.xCoord - otherPlatform.getWidthPixel(otherPlatform.width, Tile.width) < minDistFromPlatform:
                return False
        powerUps = self.powerUpList
        for powerUp in powerUps:
            if platform.xCoord - powerUp.xCoord - powerUp.getWidthPixel(powerUp.width, PowerUp.width) < minDistFromPowerUp:
                return False
        nearestTerrainIndex = self.findNearestTerrain(platform.xCoord)

        #check terrain before
        try:
            terrainBefore = self.terrainList[nearestTerrainIndex-1]
            
            distanceFromBefore = platform.xCoord - terrainBefore.xCoord - terrainBefore.getWidthPixel(terrainBefore.width, Floor.width)
            if distanceFromBefore < minDistFromTerrain:
                return False
        except IndexError:
            pass
        try:
            terrainAfter = self.terrainList[nearestTerrainIndex+1]
            distanceFromAfter = terrainAfter.xCoord - platform.xCoord - platform.getWidthPixel(platform.width, Tile.width)
            if distanceFromAfter < minDistFromTerrain:
                return False
        except IndexError:
            pass
        return True
    
    def findNearestTerrain(self,xCoord):
        #finds the terrain at that xCoord
        terrains = self.terrainList
        for terrainIndex in range(len(terrains)):
            if terrains[terrainIndex].xCoord <= xCoord <= terrains[terrainIndex].xCoord + terrains[terrainIndex].getWidthPixel(terrains[terrainIndex].width, Floor.width):
                nearestTerrainIndex = terrainIndex
        return nearestTerrainIndex
        #check distance from terrain before this terrain
        
    def findNearestObstacle(self,xCoord):
        obstacles = self.obstacleList
        shortestDistance = 100000
        nearestIndex = 0
        for obstacleIndex in range(len(obstacles)):
            obstacle = obstacles[obstacleIndex]
            distance = xCoord - obstacle.obstacle.xCoord - obstacle.obstacle.width
            if distance < shortestDistance:
                shortestDistance = distance
                nearestIndex = obstacleIndex
        return nearestIndex
    
    def findNextObstacle(self, xCoord):
        #finds the obstacle after that xCoord
        obstacles = self.obstacleList
        for obstacleIndex in range(len(obstacles)):
            obstacle = obstacles[obstacleIndex]
            if obstacle.obstacle.xCoord >= xCoord:
                return obstacle

    def findNextPlatform(self, xCoord):
        #finds the next platform after the xCoord
        platforms = self.platformList
        for platformIndex in range(len(platforms)):
            platform = platforms[platformIndex]
            if platform.xCoord >= xCoord:
                return platform
    
    def checkIfFinishLinePassed(self, player):
        if player.x > self.finishLine.xCoord:
            return True
        return False
    
    def drawBackground(self, app):
        drawImage(self.background, 0, 0, width = app.width, height = app.height)


class Canvas: 
    def __init__(self, canvasWidth, canvasHeight):
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight

class FinishLine:
    image = getCMUImage('Images/arrow.png')
    def __init__(self, app, xCoord, yCoord):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.width = 50
        self.height = 50
        self.image = FinishLine.image
    
    def updateXCoord(self, step):
        self.xCoord += step

    def draw(self):
        drawLabel('Finish Line', self.xCoord + self.width//2, 50, align = 'center', font = 'DORAEMON', size = 20)
        drawImage(self.image, self.xCoord + self.width//2, 70, width = 20, height = 20, rotateAngle = 90, align = 'center')
