from cmu_graphics import *
import os, pathlib

class GameSound:
    #insert the URLs here?
    jumpSoundURL = 'Sounds/jump.mp3'
    splashScreenSoundURL = 'Sounds/splash_theme_song.mp3'
    startScreenSoundURL = 'Sounds/start_theme_song.mp3'
    levelScreenSoundURL = 'Sounds/game_theme_song.mp3'

    def __init__(self):
        self.sound = None
        self.playing = False
        self.repeat = False
        self.jumpSound = self.loadSound(GameSound.jumpSoundURL)
        self.splashScreenSound = self.loadSound(GameSound.splashScreenSoundURL)
        self.startScreenSound = self.loadSound(GameSound.startScreenSoundURL)
        self.levelScreenSound = self.loadSound(GameSound.levelScreenSoundURL)

    @staticmethod
    def loadSound(relativePath):
        # Convert to absolute path (because pathlib.Path only takes absolute paths)
        absolutePath = os.path.abspath(relativePath)
        # Get local file URL
        url = pathlib.Path(absolutePath).as_uri()
        # Load Sound file from local URL
        #print(url)
        return Sound(url)

    def playJumpSound(self):
        self.jumpSound.play(restart = True)
        return

    def playSplashScreenSound(self):
        self.splashScreenSound.play(restart = False)
        return

    def pauseSplashScreenSound(self):
        self.splashScreenSound.pause()
        return
    
    def playStartingScreenSound(self):
        self.startScreenSound.play(restart = False)
        return
    
    def pauseStartingScreenSound(self):
        self.startScreenSound.pause()
        return

    def playLevelScreenSound(self):
        self.levelScreenSound.play(restart = False)
        return
    
    def pauseLevelScreenSound(self):
        self.levelScreenSound.pause()
        return