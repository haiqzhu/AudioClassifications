# -*- coding: utf-8 -*-
"""minst_dcgan.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j-uFm_wc3XkyDfcegYUcjiOjGqDWLmsw
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import BatchNormalization, Activation, ZeroPadding2D
from tensorflow.keras.layers import LeakyReLU, Dense, Reshape, Dropout, BatchNormalization, Flatten
from tensorflow.keras.layers import UpSampling2D, Conv2D
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Input

# import mnist data and visualize first image
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# scale data and reshape
X_train = X_train.astype('float32')

X_train = X_train / 127.5 - 1.

X_train = X_train.reshape(-1,28,28,1)

# generator
modelG = Sequential()
modelG.add(Dense(128 * 7 * 7, activation="relu", input_dim=100))
modelG.add(Reshape((7, 7, 128)))
modelG.add(UpSampling2D())
modelG.add(Conv2D(128, kernel_size=3, padding="same"))
modelG.add(BatchNormalization(momentum=0.8))
modelG.add(Activation("relu"))
modelG.add(UpSampling2D())
modelG.add(Conv2D(64, kernel_size=3, padding="same"))
modelG.add(BatchNormalization(momentum=0.8))
modelG.add(Activation("relu"))
modelG.add(Conv2D(1, kernel_size=3, padding="same"))
modelG.add(Activation("tanh"))

# discriminator
modelD = Sequential()
modelD.add(Conv2D(32, kernel_size=3, strides=2, input_shape=(28,28,1), padding="same"))
modelD.add(LeakyReLU(alpha=0.2))
modelD.add(Dropout(0.25))
modelD.add(Conv2D(64, kernel_size=3, strides=2, padding="same"))
modelD.add(ZeroPadding2D(padding=((0,1),(0,1))))
modelD.add(BatchNormalization(momentum=0.8))
modelD.add(LeakyReLU(alpha=0.2))
modelD.add(Dropout(0.25))
modelD.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))
modelD.add(BatchNormalization(momentum=0.8))
modelD.add(LeakyReLU(alpha=0.2))
modelD.add(Dropout(0.25))
modelD.add(Conv2D(256, kernel_size=3, strides=1, padding="same"))
modelD.add(BatchNormalization(momentum=0.8))
modelD.add(LeakyReLU(alpha=0.2))
modelD.add(Dropout(0.25))
modelD.add(Flatten())
modelD.add(Dense(1, activation='sigmoid'))

optimizer = Adam(0.0002, 0.5)

# compile the discriminator
modelD.compile(loss='binary_crossentropy',
    optimizer=optimizer,
    metrics=['accuracy'])

# The generator takes noise as input and generates imgs
z = Input(shape=(100,))
img = modelG(z)

# For the combined model we will only train the generator
modelD.trainable = False

# The discriminator takes generated images as input and determines if real or fake
real = modelD(img)

# The combined model  (stacked generator and discriminator)
# Trains the generator to fool the discriminator
combined = Model(z, real)
combined.compile(loss='binary_crossentropy', optimizer=optimizer)

batch_size=128

# Adversarial ground truths
real = np.ones((batch_size, 1))
fake = np.zeros((batch_size, 1))

for epoch in range(4000):
    
    # Select random batch of real images
    idx = np.random.randint(0, X_train.shape[0], batch_size)
    imgs = X_train[idx]

    # Sample noise and generate a batch of fake images
    noise = np.random.normal(0, 1, (batch_size, 100))
    gen_imgs = modelG.predict(noise)

    # Train the discriminator (real classified as ones and generated as zeros)
    d_loss_real = modelD.train_on_batch(imgs, real)
    d_loss_fake = modelD.train_on_batch(gen_imgs, fake)
    d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

    # Train the generator (wants discriminator to mistake images as real)
    g_loss = combined.train_on_batch(noise, real)

    # Plot the progress
    print ("%d [D loss: %f, acc.: %.2f%%] [G loss: %f]" % (epoch, d_loss[0], 100*d_loss[1], g_loss))
    if epoch % 50 == 0:
        r, c = 5, 5
        noise = np.random.normal(0, 1, (r * c, 100))
        gen_imgs = modelG.predict(noise)

        # Rescale images 0 - 1
        gen_imgs = 0.5 * gen_imgs + 0.5

        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[i,j].imshow(gen_imgs[cnt, :,:,0], cmap='gray')
                axs[i,j].axis('off')
                cnt += 1
        fig.savefig("gen_images/mnist_%d.png" % epoch)
        plt.close()










