from cmu_graphics import *
from map import Map
from player import Player
from level import *
from gamePlatform import *
from terrain import *
from imageHandling import *
from screen import *
from soundHandling import *
import time
import random



def onAppStart(app):
    app.seed = 2
    app.levelsAvailable = {'easy'}
    app.levelStars = {'easy': 0, 'medium': 0, 'hard': 0}
    loadScreen(app)
    loadSound(app)
    app.screen.loadSplashScreen(app)
    app.sound.playSplashScreenSound()
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
    app.startGame = False
    app.levelDifficulty = ['easy', 'medium', 'hard']
    app.levels = []
    app.levelSelectedIndex = 0
    loadLevels(app)
    app.showStartScreen = True


    
    #app.generateInterval = 2


def redrawAll(app):
    #draw start screen
    if app.splashScreen:
        app.screen.drawSplashScreen(app)

    elif app.showStartScreen:
        app.screen.drawStartScreen(app)
        
    if app.startGame:
        obstacles = app.map.obstacleList
        platforms = app.map.platformList
        terrains = app.map.terrainList
        app.map.drawBackground(app) #TODO
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
            app.sound.pauseSplashScreenSound()
            app.sound.playStartingScreenSound()
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
                app.sound.pauseStartingScreenSound()
                
        if app.startGame:
            #start laoding gameplay
            app.map = Map(app, canvas = (app.width,app.height))
            #create the game player
            app.player = Player(app)
            app.startTime = time.time()
            app.sound.playLevelScreenSound()

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
                    app.sound.playJumpSound()
                elif not app.player.isDoubleJumping:
                    app.player.isDoubleJumping = True
                    app.player.vy = -20
                    app.sound.playJumpSound()
            
        
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
        app.sound.playLevelScreenSound()
        #print(len(app.map.obstacleList), len(app.map.platformList), len(app.map.terrainList))

        #condition for generating terrain is different
        #check if there is any terrain at the border of the canvas
        borderYCoord = app.map.findTerrainHeight(app.width + app.player.vx)
    
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
        for obstacle in obstacles:
            obstacle.updateXCoord(-app.player.vx)
        for platform in platforms:
            platform.updateXCoord(-app.player.vx)
        for terrain in terrains:
            terrain.updateXCoord(-app.player.vx)
        app.map.finishLine.updateXCoord(-app.player.vx)

        ifFinished = app.map.checkIfFinishLinePassed(app.player)
        if ifFinished:
            app.sound.pauseLevelScreenSound()
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

def loadSound(app):
    app.sound = GameSound()



def main():
    runApp()

if __name__ == '__main__':
    main()


#CITATIONS
#SPRITES
#https://fontmeme.com/fonts/doraemon-font/
#https://www.spriters-resource.com/snes/doraemon2nobitanotoyslanddaiboukenjpn/sheet/84517/
#https://www.spriters-resource.com/nintendo_switch/doraemonnobitasbrainexerciseadventure/sheet/201368/
#https://www.spriters-resource.com/pc_computer/platagosuperplatformgamemaker/sheet/103669/
#https://www.spriters-resource.com/mobile/doraemonrepairshop/sheet/161998/
#https://www.spriters-resource.com/pc_computer/amongus/sheet/194022/
#https://www.spriters-resource.com/mobile/doraemonrepairshop/sheet/162101/
#https://www.spriters-resource.com/mobile/megarunredfordsadventure/sheet/58884/
#https://www.spriters-resource.com/mobile/doraemonrepairshop/sheet/161988/

#CODE RELATED
#https://www.w3schools.com/python/ref_random_seed.asp
#https://stackoverflow.com/questions/45310254/fixed-digits-after-decimal-with-f-strings -> rounding with f string
#https://realpython.com/python-timer/
#https://www.w3schools.com/python/ref_random_choices.asp
#CMU Graphics Image Handling Demo from Piazza -> link piazza post
#https://piazza.com/class/lkq6ivek5cg1bc/post/2147
#https://www.w3schools.com/python/python_try_except.asp