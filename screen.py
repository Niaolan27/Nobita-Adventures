from PIL import Image
from cmu_graphics import *
from imageHandling import *
from level import *

# def loadStartScreen(app):
#     app.startScreen = True
#     #let the player select the level
#     #for gameLevel in app.levels:
#     level.drawLevel(app, app.levels[app.levelSelectedIndex]) #TODO
#     app.level = 1
#     app.startScreen = False
#     app.startGame = True
#     pass
class Screen:
    image = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/backgrounds/background.png')
    starImage = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/star.png')
    splashScreenImage = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/backgrounds/splash.png')
    rightArrowImage = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/arrow.png')
    leftArrowImage = getCMUImageFlipped('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/arrow.png')
    
    def __init__(self, app):
        self.image = Screen.image

    def loadSplashScreen(self, app):
        app.splashScreen = True
    
    def drawSplashScreen(self,app):
        drawImage(Screen.splashScreenImage, 0, 0, width = app.width, height = app.height)
        drawLabel('Nobita Adventures', app.width//2, 70, font = 'DORAEMON', size = 50)
        drawLabel('Press Enter to begin the game', app.width//2, app.height - 30, font = 'DORAEMON', size = 20)

    def drawStartScreen(self, app):
        #background = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/backgrounds/background.png')
        levelSelected = app.levels[app.levelSelectedIndex]
        drawImage(self.image, 0, 0, width = app.width, height = app.height)
        drawRect(app.width//2, app.height//2, app.width//2 + 10, app.height//2 + 10, align = 'center', border = 'black', borderWidth = 10)
        drawImage(levelSelected.background, app.width//2, app.height//2, align = 'center', width = app.width//2, height = app.height//2)
        if levelSelected.difficulty not in app.levelsAvailable:
            drawRect(app.width//2, app.height//2, app.width//2, app.height//2, align = 'center', fill = 'white', opacity = 50)
            drawLabel('unlock previous level', app.width//2, app.height//2, align = 'center', font = 'DORAEMON', size = 20)
        else:
            #print(app.levelStars[levelSelected.difficulty])
            self.drawStars(app.levelStars[levelSelected.difficulty], yCoord = 50)
        drawLabel(f'{levelSelected.difficulty}', app.width//2, app.height-50, align = 'center', font = 'DORAEMON', size = 50)
        drawImage(Screen.leftArrowImage, 70, app.height - 50, width = 30, height = 30, align = 'center')
        drawImage(Screen.rightArrowImage, app.width - 70, app.height - 50, width = 30, height = 30, align = 'center')
    
    def drawGameOverScreen(self, app):
        drawRect(0,0,app.width,app.height, fill = 'white', opacity = 80)
        drawLabel(f'You finished the game in {app.timeTaken:.2f} seconds!', app.width//2, app.height//2, font = 'DORAEMON', size = 20)
        if app.stars == 'failed':
            drawLabel('You failed to get any stars', app.width//2, app.height//2 + 20, font = 'DORAEMON', size = 20)
        else:
            drawLabel(f'You got {app.stars} stars!', app.width//2, app.height//2 + 20, font = 'DORAEMON', size = 20)
            self.drawStars(app.stars, yCoord = app.height//2 - 50)
        drawLabel('Press r to go back to the main menu', app.width//2, app.height - 50, align = 'center', font = 'DORAEMON', size = 20)
            
    @staticmethod
    def drawStars(stars, yCoord):
        if stars == 1:
            drawImage(Screen.starImage, app.width//2, yCoord, width = 30, height = 30, align = 'center')
        if stars == 2:
            drawImage(Screen.starImage, app.width//2 - 30, yCoord, width = 30, height = 30, align = 'center')
            drawImage(Screen.starImage, app.width//2 + 30, yCoord, width = 30, height = 30, align = 'center')
        if stars == 3:
            drawImage(Screen.starImage, app.width//2 - 30, yCoord, width = 30, height = 30, align = 'center')
            drawImage(Screen.starImage, app.width//2, yCoord, width = 30, height = 30, align = 'center')
            drawImage(Screen.starImage, app.width//2 + 30, yCoord, width = 30, height = 30, align = 'center')
