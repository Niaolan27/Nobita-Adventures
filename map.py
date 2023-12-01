from cmu_graphics import *
from gamePlatform import *
from obstacles import *
from terrain import *
from player import *
from level import *
from imageHandling import *
from PIL import Image
import random
import os, pathlib

class Map:
    def __init__(self, app, canvas = None):
        #print(canvas[0], canvas[1])
        self.app = app
        self.removeBuffer = 200
        self.canvas = Canvas(canvas[0], canvas[1]) #generate a long canvas -> can change the length of canvas to make game longer or shorter
        self.terrainList = []
        self.obstacleList = []
        self.platformList = []
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
                #print(self.obstacleList)
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
        #print(len(self.terrainList))
        #self.totalDistance += terrain.width
    
    def createFinishLine(self, app):
        self.finishLine = FinishLine(app, self.finishDistance, 50)


    def removeObstacles(self):
        if self.obstacleList == []: return #non empty 
        firstObstacle = self.obstacleList[0]
        if firstObstacle.obstacle.xCoord + firstObstacle.obstacle.width <= -self.removeBuffer:
            self.obstacleList.pop(0)
        #print(len(self.obstacleList))
        return

    def removePlatforms(self):
        if self.platformList == []: return #non empty
        firstPlatform = self.platformList[0]
        if firstPlatform.xCoord + firstPlatform.getWidthPixel(firstPlatform.width, Tile.width) <= -self.removeBuffer: #add some buffer
            self.platformList.pop(0)
        #print(len(self.platformList))
        return

    def removeTerrains(self):
        if self.terrainList == []: return #non empty
        firstTerrain = self.terrainList[0]
        if firstTerrain.xCoord + firstTerrain.getWidthPixel(firstTerrain.width, Floor.width) <= -self.removeBuffer:
            self.terrainList.pop(0)
        return

    def findTerrainHeight(self, xCoord):
        for terrain in self.terrainList:
            if terrain.xCoord <= xCoord <= terrain.xCoord + terrain.getWidthPixel(terrain.width, Floor.width):
                return terrain.yCoord
        return None
    
    def checkLegalObstacle(self, obstacle): #check if a piece legal
        minDistFromObstacle = 100
        minDistFromTerrain = 100
        #check if it is far enough from other obstacles
        otherObstacles = self.obstacleList
        for otherObstacle in otherObstacles:
            #other obstacles will definitely be before this 
            #print('checking obstacle distance')
            if obstacle.obstacle.xCoord - otherObstacle.obstacle.xCoord - otherObstacle.obstacle.width < minDistFromObstacle:
                return False
    
        #check if it is far enough from terrain 
        nearestTerrainIndex = self.findNearestTerrain(obstacle.obstacle.xCoord)

        #check terrain before
        try:
            #print('checking terrain before')
            terrainBefore = self.terrainList[nearestTerrainIndex-1]
            distanceFromBefore = obstacle.obstacle.xCoord - terrainBefore.xCoord - terrainBefore.getWidthPixel(terrainBefore.width, Floor.width)
            if distanceFromBefore < minDistFromTerrain:
                return False
        except IndexError:
            pass
        return True
    
    def checkLegalPlatform(self, platform): #check if a piece legal
        minDistFromPlatform = 100
        minDistFromTerrain = 100
        #check if it is far enough from other obstacles
        otherPlatforms = self.platformList
        for otherPlatform in otherPlatforms:
            #other obstacles will definitely be before this 
            #print('checking obstacle distance')

            if platform.xCoord - otherPlatform.xCoord - otherPlatform.getWidthPixel(otherPlatform.width, Tile.width) < minDistFromPlatform:
                return False
            
        nearestTerrainIndex = self.findNearestTerrain(platform.xCoord)

        #check terrain before
        try:
            #print('checking terrain before')
            
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
        obstacles = self.obstacleList
        for obstacleIndex in range(len(obstacles)):
            obstacle = obstacles[obstacleIndex]
            if obstacle.obstacle.xCoord >= xCoord:
                return obstacle

    def findNextPlatform(self, xCoord):
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
    image = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/arrow.png')
    def __init__(self, app, xCoord, yCoord):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.width = 50
        self.height = 50
        self.image = FinishLine.image
    
    def updateXCoord(self, step):
        self.xCoord += step

    def draw(self):
        #drawRect(self.xCoord, self.yCoord, self.width, self.height)
        drawLabel('Finish Line', self.xCoord + self.width//2, 50, align = 'center', font = 'DORAEMON', size = 20)
        drawImage(self.image, self.xCoord + self.width//2, 70, width = 20, height = 20, rotateAngle = 90, align = 'center')
