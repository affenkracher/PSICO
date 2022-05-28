import winsound
import time
import os

cwd = os.getcwd()

hymne = cwd + '\\PSICO-Buerger-Software\\res\\hymne.wav'

def play(soundFile):
    try:
        time.sleep(2)
        winsound.PlaySound(soundFile, winsound.SND_FILENAME | winsound.SND_ASYNC)
        time.sleep(4)
        winsound(None, winsound.SND_PURGE)
    except:
        return

play(hymne)