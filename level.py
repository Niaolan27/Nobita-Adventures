from imageHandling import *

def calculateStars(distance, speed, timeTaken):
    perfectTime = distance / speed
    #print(perfectTime)
    oneStar = perfectTime * 1.8
    twoStar = perfectTime * 1.5
    threeStar = perfectTime *1.2
    #print(oneStar, twoStar, threeStar)
    if timeTaken < threeStar:
        return 3
    elif timeTaken < twoStar:
        return 2
    elif timeTaken < oneStar:
        return 1
    else:
        return 'failed'
    
class Level:
    easyBackground = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/backgrounds/easyBackground.png')
    mediumBackground = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/backgrounds/mediumBackground.png')
    hardBackground = getCMUImage('/Users/Jason/CMU/15112/Term Project/Speedrunners/Images/backgrounds/hardBackground.png')
    obstacleClassProb = {'easy': [0.95, 0.05],
                         'medium': [0.8, 0.2],
                         'hard': [0.6, 0.4]}
    platformClassProb = {'easy': [0.95, 0.05],
                         'medium': [0.95, 0.05],
                         'hard': [0.95, 0.05]}
    def __init__(self, difficulty):
        self.difficulty = difficulty
        if difficulty == 'easy':
            self.background = Level.easyBackground
        elif difficulty == 'medium':
            self.background = Level.mediumBackground
        else:
            self.background = Level.hardBackground
        self.obstacleProbability = Level.obstacleClassProb[difficulty]
        self.platformProbability = Level.platformClassProb[difficulty]



    def drawLevel(app, level):
        if level == app.levelSelected:
            #draw a border around it
            pass
        pass

    def loadLevel(app, level):
        pass