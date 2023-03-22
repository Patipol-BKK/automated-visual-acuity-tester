import pyaudio
import sounddevice as sd
import soundfile as sf
import wave
import datetime
sample_rate = 16000

filename = f'./local_recordings/a-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.wav'
print('Start recording')
mydata = sd.rec(int(60 * sample_rate), samplerate=sample_rate,
                channels=1, blocking=True)
sf.write(filename, mydata, sample_rate)