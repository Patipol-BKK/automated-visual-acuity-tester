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
model = load_model('300k-512-0.1-0.0005_100epoch.h5', compile=False)

opt = keras.optimizers.Adam(learning_rate=0.0005)
# Compile the model
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

# Define the labels for phonemes
phoneme_labels = ['s', 'i', 'd', 'h', 'e', 'ch', 'k', 'n', 'o', 'a', 'r', 'v', 'z', 'silence', 'other']

# Define the parameters for audio recording
sample_rate = 16000
duration = 0.025
stride = 0.01

discard_per_stride = int(sample_rate*stride)
strides_num = 20
# # Define a function to predict phoneme from audio data
a = np.zeros((41, 13))
def predict_phoneme(data):
    data_normalized = np.zeros((41, 13))
    print(data.shape)
    for i, frame in enumerate(data):
        # data_normalized[i] = (frame-base_means)/base_stds * training_stds + training_means
        data_normalized[i] = frame
    a = data[:]
    # print('a', data_normalized.shape)
    # Make the prediction using the pre-trained model
    prediction = model.predict(np.asarray([data_normalized]), verbose=0)
    # Get the index of the maximum value in the prediction
    index = np.argmax(prediction)
    # Return the predicted phoneme label
    return data_normalized, phoneme_labels[index]

# # Load the mean and std of the training data for normalization
training_means = np.load('300k_h#_means.npy')
training_stds = np.load('300k_h#_stds.npy')

# # Start recording audio and predicting phonemes in real-time
# print('Start speaking...')

# Record background noise for calibration
data = sd.rec(int(1 * sample_rate), samplerate=sample_rate, channels=1)
data = np.squeeze(data)
print(data)
data_resampled = librosa.resample(data, orig_sr=sample_rate, target_sr=16000)

base_mfcc = speechpy.feature.mfcc(data_resampled, sampling_frequency=sample_rate, frame_length=0.025, frame_stride=0.01,
    num_filters=40, fft_length=256, low_frequency=0, high_frequency=None)

base_means = np.zeros(13)
base_stds = np.zeros(13)
# for i in range(13):
#     base_stds[i] = np.std([x[i] for x in base_mfcc])
#     base_means[i] = np.mean([x[i] for x in base_mfcc])
# # print(base_stds, base_means)

# signal_buffer = data_resampled[-560 + discard_per_stride:]
# mfcc_buffer = base_mfcc[-41:]
# # print(mfcc_buffer.shape)
# cycles = 0

filename = './local_recordings/i-20230315-062613.wav'
# print('Start recording')
# mydata = sd.rec(int(1 * sample_rate), samplerate=sample_rate,
#                 channels=1, blocking=True)
# sf.write(filename, mydata, sample_rate)

signal, fs = sf.read(filename)
# signal = np.squeeze(signal)
fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True)
fig.supxlabel('Time')
fig.set_size_inches(15, 5)
ax.plot(data_resampled)

plt.show()
mfcc = speechpy.feature.mfcc(signal, sampling_frequency=sample_rate, frame_length=0.025, frame_stride=0.01,
             num_filters=40, fft_length=256, low_frequency=0, high_frequency=None)

print(mfcc)
print( predict_phoneme(mfcc[:41]))
for i in range(mfcc.shape[0] - 41):
    a, phoneme = predict_phoneme(mfcc[i : i + 41])
    print(phoneme)  

while True:
    # Record audio
    # data = sd.rec(strides_num*discard_per_stride, samplerate=sample_rate, channels=1)
    # data = signal
    # Wait until recording is finished
    # sd.wait()
    # Resample the audio data to 16kHz
    # data = np.squeeze(data)
    # data_resampled = librosa.resample(data, orig_sr=sample_rate, target_sr=16000)
    
    signal_buffer = signal_buffer[-560 + discard_per_stride:]
    signal_buffer = np.concatenate((signal_buffer, data_resampled))

    # fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True)
    # fig.supxlabel('Time')
    # fig.set_size_inches(15, 5)
    # ax.plot(signal_buffer)

    # plt.show()
    # print(signal_buffer.shape)
    # Extract the MFCC features from the audio data

    # Pre-emphasize signal
    # signal_preemphasized = speechpy.processing.preemphasis(data_resampled, cof=0.98)

    mfcc = speechpy.feature.mfcc(signal_buffer, sampling_frequency=sample_rate, frame_length=0.025, frame_stride=0.01,
                                 num_filters=40, fft_length=256, low_frequency=0, high_frequency=None)

    # print(signal_buffer.shape, 'mfcc')
    mfcc_buffer = mfcc_buffer[-41:]
    mfcc_buffer = np.concatenate((mfcc_buffer, mfcc), axis=0)
    # print(mfcc_buffer[0])
    for i in range(int(strides_num)):
        
        # print(i, i, mfcc_buffer.shape)
        a, phoneme = predict_phoneme(mfcc_buffer[i : i + 41])
        print(phoneme)
    
    

    cycles += 1
    # break
    if cycles > 10:
        break



    # # Extract MFCC features
    # mfcc = speechpy.feature.mfcc(signal_preemphasized, sample_rate, num_cepstral=13)

    # # Apply cepstral mean and variance normalization
    # mfcc_cmvn = speechpy.processing.cmvn(mfcc, variance_normalization=True)

    # # print(mfcc_cmvn)
    # # Predict the phoneme from the MFCC features
    # phoneme = predict_phoneme(mfcc_cmvn[0])
    # # Print the predicted phoneme label
    # print(phoneme)