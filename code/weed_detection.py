# -*- coding: utf-8 -*-
"""WEED_DETECTION

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kZLD41OlewUYq4ms6pUuXOb7LQhUmL_B
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np                                     # linear algebra
import pandas as pd                                    # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os

from google.colab import drive
drive.mount('/content/drive')

import os
for dirname, _, filenames in os.walk('/content/drive/MyDrive/DATASETS/rice disease/rice_leaf_diseases'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import PIL
import tensorflow as tf


from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

data_dir = '/content/drive/MyDrive/DATASETS/rice disease/rice_leaf_diseases'

data_dir

import pathlib
data_dir=pathlib.Path(data_dir)
data_dir

list(data_dir.glob("*DSC*.jpg"))

bacteria=list(data_dir.glob("Bacterial leaf blight/*"))
len(bacteria)

PIL.Image.open(str(bacteria[0]))

brown=list(data_dir.glob("Brown spot/*"))
len(brown)

dict={"bacteria":list(data_dir.glob("Bacterial leaf blight/*")),"brown":list(data_dir.glob("Brown spot/*")),"smut":list(data_dir.glob("Leaf smut/*"))}

labels_dict = {
    'bacteria': 0,
    'brown': 1,
    'smut': 2,
   
}

str(dict["smut"][0])

img=cv2.imread(str((dict["smut"][0])))

cv2.resize(img,(180,180)).shape

X, y = [], []

for name, images in dict.items():
    for image in images:
        img = cv2.imread(str(image))
        resized_img = cv2.resize(img,(180,180))
        X.append(resized_img)
        y.append(labels_dict[name])

y[:5]

X = np.array(X)
y = np.array(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

len(X_test)

X_train_scaled = X_train / 255
X_test_scaled = X_test / 255

num_classes = 3
model = Sequential([
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
              
model.fit(X_train_scaled, y_train, epochs=30)

model.evaluate(X_test_scaled,y_test)

predictions = model.predict(X_test_scaled)
predictions

score = tf.nn.softmax(predictions[0])

np.argmax(score)

y_test[0]

data_augmentation = keras.Sequential(
  [

    layers.experimental.preprocessing.RandomZoom(0.2),
    layers.experimental.preprocessing.RandomRotation(0.1),
    layers.experimental.preprocessing.RandomFlip("horizontal")
  ]
)

plt.axis('off')
plt.imshow(X[0])

plt.axis('off')
plt.imshow(data_augmentation(X)[0].numpy().astype("uint8"))

num_classes = 3

model = Sequential([
  data_augmentation,
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Dropout(0.1),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
              
model.fit(X_train_scaled, y_train, epochs=40)

model.evaluate(X_test_scaled,y_test)