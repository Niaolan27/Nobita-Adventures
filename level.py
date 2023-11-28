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