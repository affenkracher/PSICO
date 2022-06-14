import sounddevice as sd
from scipy.io.wavfile import write, read
import os
import time

def getCWD():
    CWD = os.getcwd()
    if CWD.find("\\PSICO-Buerger-Software") >= 0:
        cut = len("\\PSICO-Buerger-Software")
        CWD = CWD[0:-cut]
    return CWD

"""
Class Module for short 5 sec audio recordings if the user has a connected micro device.
"""
class MicroLogger():
    def __init__(self, queryController):
        self.fps = 44100 #rate
        self.seconds = 60 #duration of recording
        self.lastAudioID = self.queryController.lastAudioID
        self.queryController = queryController

    """
    Record user audio at a sample rate of 44100 hz, for 5 sec and store it in the storage folder.
    """
    def record(self):
        try:
            id = self.lastAudioID
            if self.lastAudioID >= 5:
                id = 0
            fileName = self.queryController.queryId + "_" + str(id) + ".wav"
            print('recording started')
            recording = sd.rec(int(self.seconds*self.fps), samplerate=self.fps, channels=2) #record
            sd.wait() #wait till recording complete
            print('recording finished')
            write(fileName, self.fps, recording) #save to WAV file
            newID = self.queryController.uploadAudio(fileName)
            self.lastAudioID = newID
        except:
            print('No micro detected')

    def main(self):
        self.record()
        
