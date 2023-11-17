from cmu_graphics import *
from map import Map

def onAppStart(app):
    app.map = Map()
    app.viewX = 0
    app.viewY = 0
    app.paused = True

def redrawAll(app):
    app.map.drawMap(app.viewX, app.viewY)
    pass

def onKeyPress(app, key):
    if key == 'right':
        takeStep(app)

def onStep(app):
    if not app.paused:
        takeStep(app)

def takeStep(app):
    app.viewX += 10

def main():
    runApp()

if __name__ == '__main__':
    main()