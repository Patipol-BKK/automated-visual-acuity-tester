import numpy as np
import sounddevice as sd
import soundfile as sf
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import librosa
import speechpy
import matplotlib.pyplot as plt
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# Load the pre-trained model
model = load_model('clean-512-0.1-0.0005_100epoch.h5', compile=False)

opt = keras.optimizers.Adam(learning_rate=0.0005)
# Compile the model
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

# Define the labels for phonemes
phoneme_labels = ['c', 'd', 'h', 'k', 'n', 'o', 'r', 's', 'v', 'z', 'other', 'silent']

# Define the parameters for audio recording
sample_rate = 16000
duration = 0.04
stride = 0.02

discard_per_stride = int(sample_rate*stride)
strides_num = 20
# # Define a function to predict phoneme from audio data
a = np.zeros((41, 13))
def predict_phoneme(data):
    # Make the prediction using the pre-trained model

    prediction = model.predict(np.asarray([data]), verbose=0)
    # Get the index of the maximum value in the prediction
    index = np.argmax(prediction)
    # Return the predicted phoneme label
    return phoneme_labels[index], prediction[0][index]

fs = 16000
signal = sd.rec(1 * fs, samplerate=fs, channels=1)
# Wait until recording is finished
sd.wait()
if signal.ndim > 1:
        signal = np.mean(signal, axis=1, dtype=signal.dtype)
signal_buffer = signal[:]

cycles = 0
signal, fs = sf.read('./alph/dsauhd98hwuihdwq.wav')
if len(signal.shape) == 2:
            signal = np.array([x[0] for x in signal])
data = signal[:]
i = 0
signal_max = 0
while True:
    # Record audio
    signal = sd.rec(1 * fs, samplerate=fs, channels=1)
    # signal = data[i:i+16000]
    signal_max = max(np.amax(signal), signal_max)
    signal *= 1/signal_max
    
    # i += 16000
    # Wait until recording is finished
    sd.wait()
    # sf.write(f"./{i}.wav", signal, 16000)
    # print(signal.shape)
    # Resample the audio data to 16kHz
    # data = np.squeeze(data)
    # signal = librosa.resample(signal, orig_sr=fs, target_sr=16000)
    if signal.ndim > 1:
        signal = np.mean(signal, axis=1, dtype=signal.dtype)
    # print(signal)
    
    signal_buffer = signal_buffer[int(fs/2):]
    signal_buffer = np.concatenate((signal_buffer, signal[:int(fs/2)]))

    # fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True)
    # fig.supxlabel('Time')
    # fig.set_size_inches(15, 5)
    # ax.plot(signal_buffer)

    # plt.show()
    # print(signal_buffer.shape)
    # Extract the MFCC features from the audio data

    # Pre-emphasize signal
    # signal_preemphasized = speechpy.processing.preemphasis(data_resampled, cof=0.98)
    # print(signal_buffer)

    mfcc = speechpy.feature.mfcc(signal_buffer, sampling_frequency=fs, frame_length=0.04, frame_stride=0.02,
                                 num_filters=40, fft_length=256, low_frequency=0, high_frequency=None)
    # fig, ax = plt.subplots()
    # fig.supxlabel('Time')
    # fig.set_size_inches(15, 5)
    # ax.pcolor(mfcc.T)
    # plt.show()

    if np.amax(signal_buffer) < 0.2:
        print(f"silence : loudness={np.amax(signal_buffer)}")
    else:
        print(f"{predict_phoneme(mfcc)} : loudness={np.amax(signal_buffer)}")

    signal_buffer = signal[:]

    mfcc = speechpy.feature.mfcc(signal_buffer, sampling_frequency=fs, frame_length=0.04, frame_stride=0.02,
                                 num_filters=40, fft_length=256, low_frequency=0, high_frequency=None)

    if np.amax(signal_buffer) < 0.2:
        print(f"silence : loudness={np.amax(signal_buffer)}")
    else:
        print(f"{predict_phoneme(mfcc)} : loudness={np.amax(signal_buffer)}")

    # cycles += 1
    # # break
    # if cycles > 10:
    #     break



    # # Extract MFCC features
    # mfcc = speechpy.feature.mfcc(signal_preemphasized, sample_rate, num_cepstral=13)

    # # Apply cepstral mean and variance normalization
    # mfcc_cmvn = speechpy.processing.cmvn(mfcc, variance_normalization=True)

    # # print(mfcc_cmvn)
    # # Predict the phoneme from the MFCC features
    # phoneme = predict_phoneme(mfcc_cmvn[0])
    # # Print the predicted phoneme label
    # print(phoneme)