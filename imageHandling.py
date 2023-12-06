from cmu_graphics import *
from PIL import Image
import os, pathlib

@staticmethod
def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def getCMUImage(fileName):
     url = fileName
     image = openImage(url)
     image = CMUImage(image)
     return image

def getCMUImageFlipped(fileName):
     url = fileName
     image = openImage(url)
     image = image.transpose(Image.FLIP_LEFT_RIGHT)
     image = CMUImage(image)
     return image
     