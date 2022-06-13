import mouse
from numpy import diff
from screeninfo import get_monitors
import math
import time

"""
Translate the values of any mouse position to that of a hd monitor (1920 x 1080)
"""
def translate(value, leftMin, leftMax, rightMin, rightMax):
    """
    Figure out how 'wide' each range is
    """
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    """
    Convert the left range into a 0-1 range (float)
    """
    valueScaled = float(value - leftMin) / float(leftSpan)
    """
    Convert the 0-1 range into a value in the right range.
    """
    return math.floor(rightMin + (valueScaled * rightSpan))

"""
MouseLogger Module to satisfy the needs of mouse position management. Read the position of the users mouse, 
evaluate the positions frequency and upload the data to firebase
"""
class MouseLogger():
    """
    Find the current main monitors width and height in pixel and store it inside the MouseLogger object
    """
    def __init__(self, queryController):
        self.log = {}
        self.queryController = queryController
        monitors = get_monitors()
        self.screenWidth = 1920
        self.screenHeight = 1080
        biggest = None
        resolution = 0
        for m in monitors:
            res = m.height * m.width
            if res > resolution:
                resolution = res
                biggest = m
        self.screenHeight = biggest.height
        self.screenWidth = biggest.width
        self.clickCounter = 0

    """
    For every new mouse position recording find the translated position and store it in a dictionary.
    The dictionary holds the frequency information about the mouse positions. Upload the dictionary to firebase
    after 500 entries are reached and clear the log
    """
    def main(self):
        recorder = self.recordMouseEvents()
        counter = 50
        for rec in recorder:
            x, y = rec
            x1 = translate(x, 0, self.screenWidth, 0, 1280 )
            y1 = translate(y, 0, self.screenHeight, 0, 720)
            if x1 > 1280:
                continue
            if y1 > 720:
                continue
            key = f'({x1},{y1})'
            if rec not in self.log:
                self.log[key] = 100
            elif rec in self.log:
                self.log[key] = self.log[key] + 100
            counter = counter + 1
            if counter >= 100:
                self.queryController.addToMouseLogs(self.log)
                self.log = {}
                counter = 0

    def main2(self):
        cb = lambda a : self.incrementCounter(a)
        mouse.on_click(cb, args=(1,))
        startTime = time.time()
        while 1:
            endTime = time.time()
            diffTime = math.floor(endTime - startTime)
            if diffTime >= 60:
                CPM = self.clickCounter / diffTime
                print(CPM)
                self.queryController.updateCPM(self.clickCounter, CPM)
                self.clickCounter = 0
                startTime = time.time()

    def incrementCounter(self, a):
        self.clickCounter += a

    """
    Return the position of the mouse every sec, to reduce the amount of data.
    """
    def recordMouseEvents(self):
        while 1:
            x , y = mouse.get_position()
            yield (x , y)
            time.sleep(1)
