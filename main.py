import time
from cmu_graphics import *
from map import Map




def onAppStart(app):
    app.map = Map()
    app.stepsPerSecond = 30
    app.paused = True
    app.startTime = time.time()
    app.stepInterval = 1/app.stepsPerSecond
    app.width = 600
    app.height = 400
    #app.generateInterval = 2


def redrawAll(app):
    obstacles = app.map.obstacleList
    platforms = app.map.platformList
    for obstacle in obstacles: #draws each obstacle
        obstacle.drawObstacle()
    for platform in platforms: #draws each platform
        platform.drawPlatform()
    

def onKeyPress(app, key):
    pass

def onStep(app):
    takeStep(app)

def takeStep(app):
    #currentTime = time.time()
    obstacles = app.map.obstacleList
    platforms = app.map.platformList
    for obstacle in obstacles:
        obstacle.updateXCoord(-10)
    for platform in platforms:
        platform.updateXCoord(-10)
    #print(pythonRound(currentTime-app.startTime, 1)%app.generateInterval)
    # if pythonRound(currentTime-app.startTime, 1)%app.generateInterval == 0.0: #create an obstacle right outside the canvas
    #     #print(app.map.canvas.canvasWidth)
    #     app.map.createObstacle(app.map.canvas.canvasWidth)
    

def main():
    runApp()

if __name__ == '__main__':
    main()