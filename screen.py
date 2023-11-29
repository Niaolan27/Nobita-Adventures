import level

def loadStartScreen(app):
    app.startScreen = True
    #let the player select the level
    for gameLevel in app.levels:
        level.drawLevel(app, gameLevel) #TODO
    app.level = 1
    app.startScreen = False
    app.startGame = True
    pass
