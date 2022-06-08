import mouse
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

    """
    For every new mouse position recording find the translated position and store it in a dictionary.
    The dictionary holds the frequency information about the mouse positions. Upload the dictionary to firebase
    after 500 entries are reached and clear the log
    """
    def main(self):
        recorder = self.recordMouseEvents()
        counter = 500
        for rec in recorder:
            x, y = rec
            x1 = translate(x, 0, self.screenWidth, 0, 1920 )
            y1 = translate(y, 0, self.screenHeight, 0, 1080)
            key = f'({x1},{y1})'
            if rec not in self.log:
                self.log[key] = 1
            elif rec in self.log:
                self.log[key] = self.log[key] + 1
            counter = counter + 1
            if counter >= 100:
                self.queryController.addToMouseLogs(self.log)
                self.log = {}
                counter = 0

    def clickCounter(self):
        counter = 0
        increment = lambda: counter + 1
        while 1: 
            mouse.on_click(counter, ())
        return counter
        
    """
    Return the position of the mouse every 2 sec, toa reduce the amount of data, otherwise a multiple of 10000
    data pairs isnt abnormal
    """
    def recordMouseEvents(self):
        while 1:
            x , y = mouse.get_position()
            yield (x , y)
            time.sleep(2)