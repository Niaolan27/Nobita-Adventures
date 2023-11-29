import time
from cmu_graphics import *
from map import Map
from player import Player
import random
from level import *
from gamePlatform import *
from terrain import *



def onAppStart(app):
    #implement some sort of account
    startGame(app)

def startGame(app):
    #game state initialization
    app.stepsPerSecond = 25
    app.paused = False
    app.gameOver = False

    #map initialization
    app.seed = 2
    random.seed(app.seed)
    app.width = 600
    app.height = 400
    app.map = Map(canvas = (app.width,app.height))

    #create the game player
    app.player = Player(app.map)
    
    #game features initialization
    app.finishLine = False
    app.finishDistance = 50 #number of blocks
    app.startGame = False
    app.levelDifficulty = ['easy', 'medium', 'hard']
    app.levels = []
    app.levelSelectedIndex = 0

    app.startTime = time.time()
    loadStartScreen(app)


    
    #app.generateInterval = 2


def redrawAll(app):
    if app.startScreen:
        for gameLevelIndex in range(len(app.levels)):
            gameLevel = app.levels[gameLevelIndex]
            if gameLevelIndex == app.levelSelectedIndex:
                borderColor = 'red'
                borderWidth = 5 
            else:
                borderColor = 'black'
                borderWidth = 1
            drawRect((gameLevelIndex+1)*app.width//4, app.height//2, 100, 100, align = 'center', fill = None, border = borderColor, borderWidth = borderWidth)
            drawLabel(gameLevel.difficulty, (gameLevelIndex+1)*app.width//4, app.height//2, align = 'center')
        
    if app.startGame:
        obstacles = app.map.obstacleList
        platforms = app.map.platformList
        terrains = app.map.terrainList
        app.player.drawPlayer()
        for terrain in terrains:
            terrain.drawTerrain()
        for obstacle in obstacles: #draws each obstacle
            obstacle.drawObstacle()
        for platform in platforms: #draws each platform
            platform.drawPlatform()
        if app.finishLine:
            app.map.finishLine.draw()

    if app.gameOver:
        drawLabel(f'You finished the game in {app.timeTaken} seconds!', app.width//2, app.height//2)
        drawLabel(f'You got {app.stars} stars!', app.width//2, app.height//2 + 20)
    
    

def onKeyPress(app, key):
    #for start screen
    if app.startScreen:
        if key == 'right':
            if app.levelSelectedIndex < len(app.levels) - 1:
                app.levelSelectedIndex += 1
        elif key == 'left':
            if app.levelSelectedIndex > 0:
                app.levelSelectedIndex -= 1
        elif key == 'enter':
            app.startScreen = False
            app.startGame = True
            app.levelSelected = app.levels[app.levelSelectedIndex]

    #for game play
    if app.startGame and not app.gameOver:
        if key == 'p':
            app.paused = not app.paused
        if key == 'up':
            #print('jump')
            if app.player.isJumping == False:
                app.player.isJumping = True
                app.player.vy = -20 #give player a boost upwards
            elif not app.player.isDoubleJumping:
                app.player.isDoubleJumping = True
                app.player.vy = -20
        if key == 's':
            takeStep(app)
    
    # if app.gameOver:
    if key == 'r':
            startGame(app)
    


def onStep(app):
    if not app.paused:
        takeStep(app)

def takeStep(app):
    #currentTime = time.time()

    #condition for generating terrain is different
    #check if there is any terrain at the border of the canvas
    borderYCoord = app.map.findTerrainHeight(app.width + app.player.vx)
    #print(borderYCoord)
    if borderYCoord == None: 
        app.map.createTerrain(start = False)

    #randomly generate obstacles and platforms
    if not app.finishLine:
        obstacleProb = [0.9, 0.1]
        obstacleType = [False, True]
        obstacleBool = random.choices(obstacleType, weights = obstacleProb)[0]
        if obstacleBool:
            app.map.createObstacle()
        platformProb = [0.9, 0.1]
        platformType = [False, True]
        platformBool = random.choices(platformType, weights = platformProb)[0]
        if platformBool:
            app.map.createPlatform()

    #create finish line if needed
    if app.map.totalDistance > app.finishDistance and not app.finishLine:
        app.map.createFinishLine()
        app.finishLine = True
    
    #remove platforms, obstacles and terrains which are off the canvas
    app.map.removePlatforms()
    app.map.removeObstacles()
    app.map.removeTerrains()
    
    #update positions
    app.player.updatePosition()
    obstacles = app.map.obstacleList
    platforms = app.map.platformList
    terrains = app.map.terrainList
    # print(f'player vx: {app.player.vx}')
    # print(f'player x:{app.player.x}')
    for obstacle in obstacles:
        obstacle.updateXCoord(-app.player.vx)
    for platform in platforms:
        platform.updateXCoord(-app.player.vx)
    for terrain in terrains:
        terrain.updateXCoord(-app.player.vx)


    # if the game has finished
    if app.finishLine:
        #print(app.map.finishLine.xCoord)
        app.map.finishLine.updateXCoord(-app.player.vx)
        ifFinished = app.map.checkIfFinishLinePassed(app.player)
        if ifFinished:
            print('finished')
            app.endTime = time.time()
            app.timeTaken = app.endTime - app.startTime
            app.paused = True
            app.gameOver = True
            app.stars = calculateStars(app.map.totalDistance*Floor.width, app.player.speed * app.stepsPerSecond, app.timeTaken)
    # print(f'player x: {app.player.x}, player y: {app.player.y}')
    # print(f'player vx: {app.player.vx}, player vy: {app.player.vy}')
    # print(f'player ax: {app.player.ax}, player ay: {app.player.ay}')
    
def loadStartScreen(app):
        app.startScreen = True
        for difficulty in app.levelDifficulty:
            app.levels.append(Level(difficulty))

def main():
    runApp()

if __name__ == '__main__':
    main()