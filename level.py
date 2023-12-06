from imageHandling import *

def calculateStars(distance, speed, timeTaken):
    perfectTime = distance / speed
    oneStar = perfectTime * 1.8
    twoStar = perfectTime * 1.5
    threeStar = perfectTime *1.2
    if timeTaken < threeStar:
        return 3
    elif timeTaken < twoStar:
        return 2
    elif timeTaken < oneStar:
        return 1
    else:
        return 'failed'
    
class Level:
    easyBackground = getCMUImage('Images/backgrounds/nope2.png')
    mediumBackground = getCMUImage('Images/backgrounds/mediumBackground.png')
    hardBackground = getCMUImage('Images/backgrounds/hardBackground.png')
    obstacleClassProb = {'easy': [0.98, 0.02],
                         'medium': [0.9, 0.1],
                         'hard': [0.6, 0.4]}
    platformClassProb = {'easy': [0.97, 0.03],
                         'medium': [0.97, 0.03],
                         'hard': [0.99, 0.01]}
    powerUpClassProb = {'easy': [0.99, 0.01],
                        'medium': [0.99, 0.01],
                        'hard': [0.99, 0.01]}
    rocketClassProb = {'easy': [0.9, 0.1],
                       'medium': [0.99, 0.01],
                        'hard': [0.99, 0.01]}
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
        self.powerUpProbability = Level.powerUpClassProb[difficulty]
        self.rocketProbability = Level.rocketClassProb[difficulty]

    def drawLevel(app, level):
        if level == app.levelSelected:
            #draw a border around it
            pass
        pass

    def loadLevel(app, level):
        pass