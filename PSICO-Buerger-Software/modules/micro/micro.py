import sounddevice as sd
from scipy.io.wavfile import write

fps = 44100 #rate
seconds = 5 #duration of recording
filename = "recording.wav"

def main(fps, seconds, filename):
    print('recording started')

    recording = sd.rec(int(seconds*fps), samplerate=fps, channels=2) #record
    sd.wait() #wait till recording complete

    print('recording finished')
    print(recording)

    write(filename, fps, recording) #save to WAV file

#test
#main(fps, seconds, filename)

