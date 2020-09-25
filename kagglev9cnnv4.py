# -*- coding: utf-8 -*-
"""kagglev9CNNv4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13xDEr0yd02z8PB5-pgWPT0ShRozYhvsI
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tensorflow.keras.layers import Bidirectional

from google.colab import drive
drive.mount('/content/drive')

train=np.load("./drive/My Drive/audio_train.npy")
test=np.load("./drive/My Drive/audio_test.npy")

train_labels=pd.read_csv("./drive/My Drive/labels_train.csv")
sample_submission=pd.read_csv("./drive/My Drive/sample_submission.csv")

train_labels

label = list(train_labels['label'])

y_train = np.empty([len(train),1])
for i in range(len(label)):
  y_train[i] = label[i]
y_train = np.array(y_train, dtype='uint8')

num_classes = 10
y_train = keras.utils.to_categorical(y_train, num_classes)



plt.plot(train[2])

print(train_labels.label.unique())

print(sample_submission.label.unique())

print(np.shape(test)[1])

verbose, epochs, batch_size = 0, 10, 32

n_timesteps, n_features, n_outputs = train.shape[0], train.shape[1], train_labels.shape[0]

n_timesteps

train.shape[0],train.shape[1]

train1=np.reshape(train,(train.shape[0],500,60,1))
train1.shape

test1=np.reshape(test,(test.shape[0],500,60,1))
test1.shape

train_labels.shape

train.shape[1]

from keras.layers import Input, LSTM, Dense, TimeDistributed, Activation, BatchNormalization, Dropout, Bidirectional, ELU, Conv2D, MaxPooling2D,Flatten,Dropout
from keras.models import Sequential
from keras.utils import Sequence
from keras.layers import LSTM

input_shape=(500,60,1)

model = models.Sequential()
model.add(Conv2D(32, (3, 3), padding='same',
                 input_shape=(500,60,1)))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))
model.add(Conv2D(128, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(128, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

#Define Model
model = models.Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(500,60,1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))

model.add(Flatten())
model.add(Dropout(0.25))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.summary()

"""no"""

from keras import regularizers, optimizers

model.compile(optimizers.RMSprop(lr=0.0005, decay=1e-6),loss="categorical_crossentropy",metrics=["accuracy"])
history = model.fit(train1, y_train, epochs=200)

pred = model.predict(test1)

np.argmax(pred[1])

predLabel = np.empty([len(test),2],dtype=int)
for i in range(len(pred)):
  predLabel[i][0] = np.int(i)
  predLabel[i][1] = np.int(np.argmax(pred[i]))

df = pd.DataFrame(predLabel, columns= ['id', 'label'])

df.to_csv (r'haiqzhu9.csv', index = False, header=True)

sample_submission

df