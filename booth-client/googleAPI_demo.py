import pyaudio
import io
import os
from google.cloud import speech_v1p1beta1 as speech

# Set up the Google Cloud Speech-to-Text API client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "automated-visual-acuity-tester-867aecad4af4.json"
client = speech.SpeechClient()

# Define the vocabulary for the speech recognition
VOCABULARY = ["c", "d", "h", "kay", "n", "o", "r", "s", "v", "z"]
commands_dict = {
    'c' : 'c',
    'see': 'c',
    'letter c': 'c',
    'letter see': 'c',
    'let us see': 'c',
    'let us c': 'c',
    'd' : 'd',
    'letter d': 'd',
    'h' : 'h',
    'letter h': 'h',
    'k' : 'k',
    'letter k': 'k',
    'n' : 'n',
    'letter n': 'n',
    'o' : 'o',
    'oh' : 'o',
    'letter o': 'o',
    'letter oh': 'o',
    'r' : 'r',
    'are' : 'r',
    'letter r': 'r',
    'letter are': 'r',
    's' : 's',
    'letter s': 's',
    'v' : 'v',
    'letter v': 'v',
    'z' : 'z',
    'that' : 'z',
    'letter z': 'z',
    'letter that': 'z',
}

# Define the microphone audio input properties
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize the PyAudio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Speak now!")

# Continuously listen for speech commands
while True:
    audio_buffer = io.BytesIO()
    for i in range(int(RATE / CHUNK)):
        data = stream.read(CHUNK)
        audio_buffer.write(data)
    audio_buffer.seek(0)

    # Use Google Cloud Speech-to-Text API to recognize speech commands
    audio_data = speech.RecognitionAudio(content=audio_buffer.read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-PH",
        enable_word_time_offsets=True,
        speech_contexts=[{
            "phrases": VOCABULARY
        }]
    )
    response = client.recognize(config=config, audio=audio_data)
    for result in response.results:
        for word in result.alternatives[0].words:
            print(word.word.lower())
            if word.word.lower() in VOCABULARY:
                print(f"Command recognized: {word.word}")