import sounddevice as sd
from scipy.io.wavfile import write
import os
import time

class MicroLogger():
    def __init__(self, queryController):
        self.queryController = queryController
        self.fps = 44100 #rate
        self.seconds = 2 #duration of recording
        self.fileName = os.getcwd() + "\\PSICO-Buerger-Software\\modules\\micro\\storage\\recording.wav"
        self.wavFile = os.getcwd() + "\\PSICO-Buerger-Software\\modules\\micro\\storage\\txt2speech.wav"

    def record(self):
        print('recording started')
        recording = sd.rec(int(self.seconds*self.fps), samplerate=self.fps, channels=2) #record
        sd.wait() #wait till recording complete
        print('recording finished')
        print(recording)
        write(self.fileName, self.fps, recording) #save to WAV file

    def main(self):
        self.record()
        time.sleep(2)

ML = MicroLogger("")
ML.main()
