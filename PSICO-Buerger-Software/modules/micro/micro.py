from audioop import byteswap
import io
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
        self.seconds = 5 #duration of recording
        self.fileName = getCWD() + "\\PSICO-Buerger-Software\\modules\\micro\\storage\\recording.wav"
        self.queryController = queryController

    """
    Record user audio at a sample rate of 44100 hz, for 5 sec and store it in the storage folder.
    """
    def record(self):
        try:
            print('recording started')
            recording = sd.rec(int(self.seconds*self.fps), samplerate=self.fps, channels=2) #record
            sd.wait() #wait till recording complete
            print('recording finished')
            write("test.wav", self.fps, recording) #save to WAV file
        except:
            print('No micro detected')

    def uploadAudio(self):
        with open(self.fileName, "rb") as wavFile:
            input_wav = wavFile.read()
        rate, data = read(io.BytesIO(input_wav))
        reversed_data = data[::-1]
        bytes_wav = bytes()
        byte_io = io.BytesIO(bytes_wav)
        write(byte_io, rate, reversed_data)
        output_wav = byte_io.read()
        self.queryController.uploadAudio(output_wav)


    def main(self):
        self.record()
        time.sleep(2)
        
