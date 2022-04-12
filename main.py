import StellarPlayer
import os
import sys
import time
import threading
import random
import math

from StellarPlayer import ImageDrawingDescription

plugin_dir = os.path.dirname(__file__)

class Snow:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.randint(4, 10) 
        self.px = random.randint(300, 500) 
        self.r = random.randint(2, 5)
        self.dy = 1 + random.randint(0, 2)
        self.dot = b'\xff\xff\xff' + (random.randint(200, 255)).to_bytes(1,'big')
    
    def get(self, t):
        self.y += self.dy
        return ImageDrawingDescription(
            x=self.x + self.dx * math.sin(t/(self.px)),
            y=self.y,
            w=self.r,
            h=self.r,
            width=1,
            height=1,
            buffer=self.dot)

COUNT = 222

class MyPlugin(StellarPlayer.IStellarPlayerPlugin):
    def __init__(self, player: StellarPlayer.IStellarPlayer):
        super().__init__(player)
        self.on = True
        self.canvas = None
        self.thread = None        
        self.w = 2000
        self.h = 1200
        self.snows = []
        

    def start(self):
        super().start()
        self.canvas = self.player.newCanvas(30)        

    def genSnow(self):
        if random.randint(1, 100) < 13 and len(self.snows) < COUNT:
            s = Snow(random.randint(0, self.w), 0)
            self.snows.append(s)
        
    def show(self):
        self.player.toast({"page" : "", "message": "播放视频看看下雪吧"})

    def onVideoRendered(self, pts):        
        self.genSnow()
        buffers = []
        for snow in self.snows[:]:
            if snow.y > self.h:
                self.snows.remove(snow)
            else:
                buffers.append(snow.get(pts))
        
        self.canvas.drawBuffers(self.w, self.h, 0, 0, self.w, self.h, buffers)


def newPlugin(player: StellarPlayer.IStellarPlayer, *arg):
    plugin = MyPlugin(player)
    return plugin


def destroyPlugin(plugin: StellarPlayer.IStellarPlayerPlugin):
    plugin.stop()
