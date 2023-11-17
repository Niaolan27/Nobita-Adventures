from cmu_graphics import *
import random


class Map:
    def __init__(self):
        #create the initial map
        self.map = self.generateMap()

    def generateMap(self):
        map = []
        previousHeight = 0
        for i in range(3):
            canvas = Canvas(previousHeight)
            map.append(canvas) #(canvas, y) -> y is the ending height of the previous canvas
            previousHeight = canvas.endingHeight
        return map

    def updateMap(self):
        #destroys front part of the map 
        #generates a new part of the map
        pass
    
    def drawMap(self, viewX, viewY):
        canvasStart = viewX % Canvas.width #starting point of the canvas
        canvasIndex = viewX // Canvas.width #which canvas to start with
        #draw the map
        firstCanvas = self.map[canvasIndex]
        for block in firstCanvas.blocks:
            if block.x - viewX < 0 and (viewX-block.x) < block.width:
                startX = 0
                width = block.x + block.width - viewX
            else: 
                startX = block.x - viewX
                width = block.width
            startY = block.y
            height = block.height
            drawRect(startX, startY, width, height, fill = 'black')
        secondCanvas = self.map[canvasIndex+1]
        for block in secondCanvas.blocks:
            if block.x < viewX:
                startX = Canvas.width-viewX+block.x
                width = block.width #it's okay to go off the screen?
                startY = block.height
                height = block.height
                drawRect(startX, startY, width, height, fill = 'black')




class Canvas:
    height = 400
    width = 600
    numBlocks = 3
    def __init__(self, previousHeight):
        self.blocks, self.endingHeight = self.generateBlocks(previousHeight) #list of blocks in the canvas
        #creates one canvas

    def generateBlocks(self, previousHeight):
        blocks = [] #each block should have a color, x, y, width, height
        for i in range(Canvas.numBlocks):
            interval = Canvas.width//Canvas.numBlocks
            xRange = (i*interval, (i+1)*interval) # break the canvas into intervals, and build blocks
            result = self.generateBlock(xRange, previousHeight)
            blocks.append(result[0])
            previousHeight = result[1]
            #     blocks.append(result[0])
            #     endingHeight = result[1]
            # if i == 0: 
            #     blocks.append(self.generateStartingBlock(xRange, previousHeight)) #starting block for canvas
            # elif i == Canvas.numBlocks-1:
            #     result = self.generateEndingBlock(xRange)
            #     blocks.append(result[0])
            #     endingHeight = result[1]
            # else: 
            #     blocks.append(self.generateBlock())
        return blocks, previousHeight
    
    # def generateBlock(self, xRange):
    #     width = random.randint(0, xRange[1] - xRange[0] - 20) #20 is for buffer
    #     height = random.randint(0, Canvas.height//5)
    #     x = random.randint(xRange[0] + 10, xRange[1] - 10) #10 is for buffer
    #     y = height
    #     block = Block(x,y,width,height)
    #     #generate one block
    #     return block
    
    def generateBlock(self, xRange, previousHeight):
        interval = xRange[1] - xRange[0]
        if previousHeight != 0: #there is a block to be continued
            x = 0
            y = previousHeight
            height = previousHeight
            width = random.randint(0, interval)
            block = Block(x,y,width,height)
        else:
            width = random.randint(0, interval) #20 is for buffer
            height = random.randint(0, Canvas.height//5)
            x = random.randint(xRange[0], xRange[0] + (interval-width)) #10 is for buffer
            y = height
            block = Block(x,y,width,height)
        #generate one block
        if block.x+block.width == xRange[1]:
            endingHeight = block.height
        else: endingHeight = 0
        return (block, endingHeight)
    
    # def generateEndingBlock(self, xRange):
    #     width = random.randint(0, xRange[1] - xRange[0] - 20) #20 is for buffer
    #     height = random.randint(0, Canvas.height//5)
    #     x = random.randint(xRange[0] + 10, xRange[1] - 10) #10 is for buffer
    #     y = height
    #     block = Block(x,y,width,height)
    #     #generate one block
    #     return block

class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height