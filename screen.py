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
class startScreen:
    image = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/backgrounds/background.png')
    
    def __init__(self, app):
        self.image = startScreen.image

    def drawStartScreen(self, app):
        #background = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/backgrounds/background.png')
        levelSelected = app.levels[app.levelSelectedIndex]
        drawImage(self.image, 0, 0, width = app.width, height = app.height)
        drawRect(app.width//2, app.height//2, app.width//2 + 10, app.height//2 + 10, align = 'center', border = 'black', borderWidth = 10)
        drawImage(levelSelected.background, app.width//2, app.height//2, align = 'center', width = app.width//2, height = app.height//2)
        drawLabel(f'{levelSelected.difficulty}', app.width//2, app.height//2+150, align = 'center', font = 'DORAEMON', size = 50)
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
def drawGameOverScreen(app):
    drawRect(0,0,app.width,app.height, fill = 'white', opacity = 80)
    drawLabel(f'You finished the game in {app.timeTaken} seconds!', app.width//2, app.height//2, font = 'DORAEMON', size = 20)
    if app.stars == 'failed':
        drawLabel('You failed to get any stars', app.width//2, app.height//2 + 20, font = 'DORAEMON', size = 20)
    else:
        drawLabel(f'You got {app.stars} stars!', app.width//2, app.height//2 + 20, font = 'DORAEMON', size = 20)