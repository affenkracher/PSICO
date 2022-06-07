import sounddevice as sd
from scipy.io.wavfile import write
import os
import time

"""
Class Module for short 5 sec audio recordings if the user has a connected micro device.
"""
class MicroLogger():
    def __init__(self, queryController):
        self.queryController = queryController
        self.fps = 44100 #rate
        self.seconds = 5 #duration of recording
        self.fileName = os.getcwd() + "\\PSICO-Buerger-Software\\modules\\micro\\storage\\recording.wav"
        self.wavFile = os.getcwd() + "\\PSICO-Buerger-Software\\modules\\micro\\storage\\txt2speech.wav"

    """
    Record user audio at a sample rate of 44100 hz, for 5 sec and store it in the storage folder.
    """
    def record(self):
        try:
            print('recording started')
            recording = sd.rec(int(self.seconds*self.fps), samplerate=self.fps, channels=2) #record
            sd.wait() #wait till recording complete
            print('recording finished')
            write(self.fileName, self.fps, recording) #save to WAV file
        except:
            print('No micro detected')

    def main(self):
        self.record()
        time.sleep(2)
