
from cmu_graphics import *
from map import Map
from player import Player
from level import *
from gamePlatform import *
from terrain import *
from imageHandling import *
from screen import *
import time
import random



def onAppStart(app):
    # app.imageURL = {
    #     'playerRun1': '/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/doraemon_transparent.png',
    #     'playerRun2' : '/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/doraemon_run2.png',
    #     'background': '/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/background.png',
    #     'tile': '/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/tile.png',
    #     'platform': '/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/platform.png',
    # }
    #app.imageDict = dict()
    #loadGameImages(app)
    #implement some sort of account
    app.seed = 2
    app.levelsAvailable = {'easy'}
    app.levelStars = {'easy': 0, 'medium': 0, 'hard': 0}
    loadScreen(app)
    app.screen.loadSplashScreen(app)
    startGame(app)

def startGame(app):
    #game state initialization
    app.stepsPerSecond = 25
    app.stepCounter = 0
    app.paused = False
    app.gameOver = False

    #map initialization
    random.seed(app.seed)
    app.width = 600
    app.height = 400
    
    
    #game features initialization
    
    app.finishDistance = 5 #number of blocks
    app.startGame = False
    app.levelDifficulty = ['easy', 'medium', 'hard']
    app.levels = []
    app.levelSelectedIndex = 0
    app.startTime = time.time()
    loadLevels(app)
    app.showStartScreen = True


    
    #app.generateInterval = 2


def redrawAll(app):
    #draw start screen
    if app.splashScreen:
        app.screen.drawSplashScreen(app)

    elif app.showStartScreen:
        app.screen.drawStartScreen(app)
        # for gameLevelIndex in range(len(app.levels)):
        #     gameLevel = app.levels[gameLevelIndex]
        #     if gameLevelIndex == app.levelSelectedIndex:
        #         borderColor = 'red'
        #         borderWidth = 5 
        #     else:
        #         borderColor = 'black'
        #         borderWidth = 1
        #     drawRect((gameLevelIndex+1)*app.width//4, app.height//2, 100, 100, align = 'center', fill = None, border = borderColor, borderWidth = borderWidth)
        #     #drawLabel(gameLevel.difficulty, (gameLevelIndex+1)*app.width//4, app.height//2, align = 'center')
        #     drawImage(app.levels[gameLevelIndex].background, (gameLevelIndex+1)*app.width//4, app.height//2, align = 'center', width = 100, height = 100)
        
    if app.startGame:
        obstacles = app.map.obstacleList
        platforms = app.map.platformList
        terrains = app.map.terrainList
        app.map.drawBackground(app) #TODO
        #print(app.player.dead)
        if not app.player.dead:
            if app.stepCounter // app.player.cadence % 2 == 0:
                app.player.drawPlayer(0)
            else:
                app.player.drawPlayer(1)
        else:
            app.player.drawDeadPlayer()
            



        for terrain in terrains:
            terrain.drawTerrain()
        for obstacle in obstacles: #draws each obstacle
            obstacle.drawObstacle()
        for platform in platforms: #draws each platform
            platform.drawPlatform()
        app.map.finishLine.draw()

    if app.gameOver:
        app.screen.drawGameOverScreen(app)
        
    
    

def onKeyPress(app, key):
    #for start screen
    if app.splashScreen:
        if key == 'enter':
            app.splashScreen = False
    elif app.showStartScreen:
        if key == 'right':
            if app.levelSelectedIndex < len(app.levels) - 1:
                app.levelSelectedIndex += 1
        elif key == 'left':
            if app.levelSelectedIndex > 0:
                app.levelSelectedIndex -= 1
        elif key == 'enter':
            if app.levels[app.levelSelectedIndex].difficulty in app.levelsAvailable:
                app.showStartScreen = False
                app.startGame = True
                app.levelSelected = app.levels[app.levelSelectedIndex]
        if app.startGame:
            #start laoding gameplay
            app.map = Map(app, canvas = (app.width,app.height))
            #create the game player
            app.player = Player(app)

    #for game play
    if app.startGame and not app.gameOver:
        if key == 'p':
            app.paused = not app.paused
        if key == 'up':
            #print('jump')
            if not app.player.stuck:
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
    
    if app.startGame:
        #print(len(app.map.terrainList))
        #revive the dead player?
        # if app.player.dead:
        #     app.player.dead = False
        #     print(app.player.dead)

        #condition for generating terrain is different
        #check if there is any terrain at the border of the canvas
        borderYCoord = app.map.findTerrainHeight(app.width + app.player.vx)
        #print(borderYCoord)
        if borderYCoord == None: 
            app.map.createTerrain(app, start = False)

        #randomly generate obstacles and platforms
        obstacleProb = app.levelSelected.obstacleProbability
        obstacleType = [False, True]
        obstacleBool = random.choices(obstacleType, weights = obstacleProb)[0]
        if obstacleBool:
            app.map.createObstacle(app)
        platformProb = app.levelSelected.platformProbability
        platformType = [False, True]
        platformBool = random.choices(platformType, weights = platformProb)[0]
        if platformBool:
            app.map.createPlatform(app)

        #create finish line if needed
        #print(app.map.totalDistance, app.finishDistance)
        
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
        app.map.finishLine.updateXCoord(-app.player.vx)

        ifFinished = app.map.checkIfFinishLinePassed(app.player)
        if ifFinished:
            #print('finished')
            app.gameOver = True
            app.paused = True
            app.endTime = time.time()
            app.timeTaken = app.endTime - app.startTime
            app.stars = calculateStars(app.map.finishDistance, app.player.speed * app.stepsPerSecond, app.timeTaken)
            if app.stars != 'failed':
                if app.levelSelectedIndex < len(app.levels) - 1:
                    app.levelsAvailable.add(app.levels[app.levelSelectedIndex+1].difficulty)
                currentLevelStars = app.levelStars[app.levels[app.levelSelectedIndex].difficulty]
                if app.stars > currentLevelStars:
                    app.levelStars[app.levels[app.levelSelectedIndex].difficulty] = app.stars
    # print(f'player x: {app.player.x}, player y: {app.player.y}')
    # print(f'player vx: {app.player.vx}, player vy: {app.player.vy}')
    # print(f'player ax: {app.player.ax}, player ay: {app.player.ay}')
    app.stepCounter += 1
    
def loadScreen(app):
    app.showStartScreen = True
    app.screen = Screen(app)

def loadLevels(app):
    for difficulty in app.levelDifficulty:
        app.levels.append(Level(difficulty))



def main():
    runApp()

if __name__ == '__main__':
    main()


#CITATIONS
#https://fontmeme.com/fonts/doraemon-font/
#https://www.spriters-resource.com/snes/doraemon2nobitanotoyslanddaiboukenjpn/sheet/84517/
#https://www.spriters-resource.com/nintendo_switch/doraemonnobitasbrainexerciseadventure/sheet/201368/
#https://www.spriters-resource.com/pc_computer/platagosuperplatformgamemaker/sheet/103669/
#https://www.spriters-resource.com/mobile/doraemonrepairshop/sheet/161998/
#https://www.w3schools.com/python/ref_random_seed.asp
#https://stackoverflow.com/questions/45310254/fixed-digits-after-decimal-with-f-strings -> rounding with f string
#https://www.spriters-resource.com/pc_computer/amongus/sheet/194022/
#https://www.spriters-resource.com/mobile/doraemonrepairshop/sheet/162101/
#https://www.spriters-resource.com/mobile/megarunredfordsadventure/sheet/58884/
#https://www.spriters-resource.com/mobile/doraemonrepairshop/sheet/161988/