import mouse
from screeninfo import get_monitors
import math

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return math.floor(rightMin + (valueScaled * rightSpan))

class MouseLogger():
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

    def main(self):
        recorder = self.recordMouse()
        counter = 0
        for rec in recorder:
            x, y = rec
            x1 = translate(x, 0, self.screenWidth, 0, 1920 )
            y1 = translate(y, 0, self.screenHeight, 0, 1080)
            key = f'({x1},{y1})'
            if rec not in self.log and counter % 300 == 0:
                self.log[key] = 1
            elif rec in self.log and counter % 300 == 0:
                self.log[key] = self.log[key] + 1
            if counter % 5000 == 0:
                counter = 0
                self.queryController.addToMouseLogs(self.log)
            counter = counter + 1

    def recordMouse(self):
        index = 0
        while 1:
            if index == 50:
                x , y = mouse.get_position()
                index = 0
                yield (x , y)
            index = index + 1