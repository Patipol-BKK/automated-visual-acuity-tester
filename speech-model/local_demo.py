import numpy as np
import sounddevice as sd
import soundfile as sf
import tensorflow as tf
from tensorflow.keras.models import load_model
import librosa
import speechpy

# Load the pre-trained model
model = load_model('mfcc_256.h5')

# Define the labels for phonemes
phoneme_labels = ['a', 'ch', 'd', 'e', 'h', 'i', 'k', 'o', 'r', 's', 'v', 'z']

# Define the parameters for audio recording
sample_rate = 16000
duration = 1.0

# Define a function to predict phoneme from audio data
def predict_phoneme(data):
    # Reshape the data to the shape (1, 13)
    data = np.reshape(data, (1, 13))
    # Normalize the data using the mean and std of the training data
    data_normalized = (data - mean) / std
    # Make the prediction using the pre-trained model
    prediction = model.predict(data_normalized)
    # Get the index of the maximum value in the prediction
    index = np.argmax(prediction)
    # Return the predicted phoneme label
    return phoneme_labels[index]

# Load the mean and std of the training data for normalization
mean = np.load('mfcc_256_mean.npy')
std = np.load('mfcc_256_std.npy')

# Start recording audio and predicting phonemes in real-time
print('Start speaking...')
while True:
    # Record audio
    data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    # Wait until recording is finished
    sd.wait()
    # Resample the audio data to 16kHz
    data = np.squeeze(data)
    data_resampled = librosa.resample(data, sample_rate, 16000)
    # Extract the MFCC features from the audio data

    # Pre-emphasize signal
    signal_preemphasized = speechpy.processing.preemphasis(data_resampled, cof=0.98)

    # Extract MFCC features
    mfcc = speechpy.feature.mfcc(signal_preemphasized, sample_rate, num_cepstral=13)

    # Apply cepstral mean and variance normalization
    mfcc_cmvn = speechpy.processing.cmvn(mfcc, variance_normalization=True)

    # print(mfcc_cmvn)
    # Predict the phoneme from the MFCC features
    phoneme = predict_phoneme(mfcc_cmvn[0])
    # Print the predicted phoneme label
    print(phoneme)