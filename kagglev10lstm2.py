# -*- coding: utf-8 -*-
"""kagglev10LSTM2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wHLfrY9C78DsKgPilbeXBegByDExf8Ye
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

train1=np.reshape(train,(train.shape[0],500,60))
train1.shape

test1=np.reshape(test,(test.shape[0],500,60))
test1.shape

train_labels.shape

train.shape[1]

from scipy import misc
import sklearn
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

train_x, test_x, train_y, test_y = train_test_split(train1, y_train, random_state = 101, test_size=0.25)

def fit_and_evaluate(t_x, val_x, t_y, val_y, EPOCHS=200, BATCH_SIZE=128):
    results = model.fit(t_x, t_y, epochs=EPOCHS, batch_size=BATCH_SIZE, 
              verbose=1, validation_split=0.1)  
    print("Val Score: ", model.evaluate(val_x, val_y))
    return results

from keras.layers import Input, LSTM, Dense, TimeDistributed, Activation, BatchNormalization, Dropout, Bidirectional, ELU
from keras.models import Sequential
from keras.utils import Sequence
from keras.layers import LSTM

"""NO"""

model = models.Sequential()
model.add(Bidirectional(LSTM(10, return_sequences=True), input_shape=(500,60)))
model.add(Dense(500))
model.add(Dropout(0.2))
model.add(Bidirectional(LSTM(60)))
model.add(Dense(100))
model.add(ELU())
model.add(Dropout(0.2))
model.add(Dense(10))
model.add(Activation('softmax'))

model.summary()

"""no"""

model.compile(loss='categorical_crossentropy', optimizer='rmsprop',
              metrics=['accuracy'])

n_folds=4
epochs=200
batch_size=128

#save the model history in a list after fitting so that we can plot later
model_history = [] 

for i in range(n_folds):
    print("Training on Fold: ",i+1)
    t_x, val_x, t_y, val_y = train_test_split(train_x, train_y, test_size=0.1, 
                                               random_state = np.random.randint(1,1000, 1)[0])
    model_history.append(fit_and_evaluate(t_x, val_x, t_y, val_y, epochs, batch_size))
    print("======="*12, end="\n\n\n")

pred = model.predict(test1)

np.argmax(pred[1])

predLabel = np.empty([len(test),2],dtype=int)
for i in range(len(pred)):
  predLabel[i][0] = np.int(i)
  predLabel[i][1] = np.int(np.argmax(pred[i]))

df = pd.DataFrame(predLabel, columns= ['id', 'label'])

df.to_csv (r'haiqzhu10.csv', index = False, header=True)

sample_submission

df