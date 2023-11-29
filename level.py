def calculateStars(distance, speed, timeTaken):
    perfectTime = distance / speed
    print(perfectTime)
    oneStar = perfectTime * 1.25
    twoStar = perfectTime * 1.15
    threeStar = perfectTime
    print(oneStar, twoStar, threeStar)
    if timeTaken < threeStar:
        return '3 stars'
    elif timeTaken < twoStar:
        return '2 stars'
    elif timeTaken < oneStar:
        return '1 star'
    else:
        return 'failed'
    
class Level:
    obstacleClassProb = {'easy': [0.95, 0.05],
                         'medium': [0.8, 0.2],
                         'hard': [0.5, 0.5]}
    platformClassProb = {'easy': [0.95, 0.05],
                         'medium': [0.9, 0.1],
                         'hard': [0.8, 0.2]}
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.preview = '' #url of preview image
        self.obstacleProbability = Level.obstacleClassProb[difficulty]
        self.platformProbability = Level.platformClassProb[difficulty]



    def drawLevel(app, level):
        if level == app.levelSelected:
            #draw a border around it
            pass
        pass

    def loadLevel(app, level):
        pass