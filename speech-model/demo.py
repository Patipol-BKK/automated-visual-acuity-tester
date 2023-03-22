
import tensorflow as tf
from tensorflow import keras
import scipy
import scipy.io.wavfile as wav
import numpy as np
import wave
import matplotlib.pyplot as plt
import noisereduce
import speechpy
import os
from scipy.cluster.vq import vq, kmeans2, kmeans, whiten
from scipy.spatial import distance
from tqdm.notebook import tqdm
from hmmlearn import hmm
import ruptures as rpt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import soundfile as sf
import sounddevice as sd
import pickle 

training_y = []
training_x = []
for phoneme in tqdm(training_phoneme_signals):
    if phoneme in new_phenome_lookup:
        sample_disp = []
#         print(new_phenome_lookup[phoneme], training_phoneme_signals[phoneme])
        tmp = []
        for i, sample in enumerate(training_phoneme_signals[phoneme]):
            tmp.append(np.array(sample))

            if (i + 1) % 3 == 0:
                training_x.append(np.asarray(tmp))
                tmp = []
                training_y.append(new_phenome_lookup[phoneme])
            if len(training_phoneme_signals[phoneme]) - i < 3:
                break
#             print(tmp)
#             if i < 1000:
#                 sample_disp.append(np.array(sample))
            
#         sample_disp = np.asarray(sample_disp)
#         fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True)
#         fig.supxlabel('Time')
#         fig.set_size_inches(15, 5)

#         ax.pcolor(sample_disp.T)
#         ax.set_title(new_phenome_lookup[phoneme])
training_x = np.asarray(training_x)
training_y = np.asarray(training_y)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, GlobalAveragePooling2D, BatchNormalization
from sklearn.preprocessing import LabelEncoder
import numpy as np
from tensorflow.keras.callbacks import TensorBoard

tensorboard_callback = TensorBoard(log_dir="./logs/v5")

data = np.asarray(training_x)  # shape (577547, 129)
labels = np.asarray(training_y)  # shape (577547,)

# Convert labels to one-hot encoding

encoder = LabelEncoder()
labels_num = encoder.fit_transform(labels)

labels_onehot = tf.keras.utils.to_categorical(labels_num)

print(data.shape)

# Define the input shape of the data
input_shape = (data.shape[1], data.shape[2], 1)

# Add padding to the input data
# data_padded = np.pad(data, ((0,0),(1,1)), mode='constant')

# Define the model architecture
model = Sequential()
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same', input_shape=input_shape))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(GlobalAveragePooling2D())
model.add(Dense(units=128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=12, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Print the model summary
model.summary()

model.fit(data, labels_onehot, epochs=10, batch_size=128, callbacks=[tensorboard_callback])