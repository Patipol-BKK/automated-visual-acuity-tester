import pyaudio
import requests
import json
from configure import auth_key

# Replace YOUR_API_KEY with your actual AssemblyAI API key
API_KEY = auth_key
API_URL = "wss://api.assemblyai.com/v2/realtime/ws"

# Define the audio stream properties
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

# Define the vocabulary for the transcription
VOCABULARY = ["c", "d", "h", "k", "n", "o", "r", "s", "v", "z"]

# Initialize the PyAudio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Recording...")

# Make the transcription request
headers = {
    "authorization": API_KEY,
    "content-type": "application/json"
}

data = {
    "model": "assemblyai-2.0",
    "language_model": "assemblyai-2.0",
    "audio_config": {
        "sample_rate": RATE,
        "channels": CHANNELS
    },
    "vocabulary": VOCABULARY
}

with requests.post(API_URL, headers=headers, json=data, stream=True) as res:
    res.raise_for_status()
    response_data = json.loads(res.content.decode('utf-8'))
    for line in res.iter_lines():
        if line:
            response_data = json.loads(line.decode('utf-8'))
            if "text" in response_data:
                if response_data["confidence"] > 0.6 and response_data["text"] in VOCABULARY:
                    print(response_data["text"])

print("Recording finished.")

# Stop the audio stream
stream.stop_stream()
stream.close()
audio.terminate()
