import uuid
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
        self.fileName = getCWD() + self.queryController.queryId + "_" + str(uuid.uuid1()) + "_onStartUp.wav"
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
            write(self.fileName, self.fps, recording) #save to WAV file
            self.uploadAudio(self.queryController.storage, self.fileName)
        except:
            print('No micro detected')

    def uploadAudio(self, storage, audio): 
        blob = storage.blob("Audio/" + audio)
        blob.upload_from_filename(filename=audio, content_type="audio/wav")
        blob.make_public()

    def main(self):
        self.record()
        time.sleep(2)
        
