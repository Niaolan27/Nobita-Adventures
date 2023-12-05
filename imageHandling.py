from cmu_graphics import *
from PIL import Image
import os, pathlib

@staticmethod
def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def getCMUImage(fileName):
     #print('image loading')
     url = fileName
     image = openImage(url)
     image = CMUImage(image)
     return image

def getCMUImageFlipped(fileName):
     #print('image loading')
     url = fileName
     image = openImage(url)
     image = image.transpose(Image.FLIP_LEFT_RIGHT)
     image = CMUImage(image)
     return image
     

def loadGameImages(app): #load all the game images and stores them as CMUImage
    for imageName in app.imageURL:
        imageURL = app.imageURL[imageName]
        image = openImage(imageURL)
        image = CMUImage(image)
        app.imageDict[imageName] = image