import winsound
import time
import os

"""
Play the any audio file on windows
"""
class MusicPlayer():
    def __init__(self):
        self.hymnePath = os.getcwd() + '\\PSICO-Buerger-Software\\res\\hymne.wav'

    """
    As the library imported does not support stopping the audio file after a given amount of time,
    force a playback stop by crashing the moduels execution and catching the error without harm to any
    other part of the software
    """
    def play(self, soundFilePath):
        try:
            time.sleep(2)
            winsound.PlaySound(soundFilePath, winsound.SND_FILENAME | winsound.SND_ASYNC)
            time.sleep(4)
            winsound(None, winsound.SND_PURGE)
        except:
            return

    """
    Main method of the class to give the user a little bit of a preperation time
    to stand up and listen to any hymne etc while saluting
    """
    def main(self):
        time.sleep(1)
        self.play(self.hymnePath)