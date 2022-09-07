# -*- coding: utf-8 -*-
"""CNN_DuBaoThoiTiet_Nhom22.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Pu_PUbKupUP5Ni5osBoiPqP3JpzT6_TG
"""

!pip install tensorflow

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
import random
import shutil

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img

import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

import cv2,os
data_path='/content/drive/MyDrive/THỰC HÀNH MÁY HỌC/WEATHER/'
categories=os.listdir(data_path)
labels=[i for i in range(len(categories))]

label_dict=dict(zip(categories,labels)) #empty dictionary
print(label_dict)
print(categories)
print(labels)

img_size=100
data=[]
target=[]

for category in categories:
    folder_path=os.path.join(data_path,category)
    img_names=os.listdir(folder_path)
        
    for img_name in img_names:
        img_path=os.path.join(folder_path,img_name)
        img=cv2.imread(img_path)

        try:  
            resized=cv2.resize(img,(img_size,img_size))
            #resizing the image  into 100x100, since we need a fixed common size for all the images in the dataset
            data.append(resized)
            target.append(label_dict[category])
            #appending the image and the label(categorized) into the list (dataset)
        except Exception as e:
            print('Exception:',e)
            #if any exception rasied, the exception will be printed here. And pass

data

target

import numpy as np
data=np.array(data)/255.0
data=np.reshape(data,(data.shape[0],img_size,img_size,3))
target=np.array(target)
from keras.utils import np_utils
new_target=np_utils.to_categorical(target)

new_target.shape

import seaborn as sns
plt.figure(figsize=(9,7))
plt.style.use("fivethirtyeight")
sns.countplot(target)
plt.show()

fig = plt.figure(figsize=(12,7))
for i in range(15):
    sample =  random.choice(range(len(data)))
    image = data[sample]
    category = target[sample]
    plt.subplot(3,5,i+1)
    plt.subplots_adjust(hspace=0.3)
    plt.imshow(image)
    plt.xlabel(category)
    
plt.tight_layout()
plt.show()

"""#CNN"""

data.shape

data.shape[1:]

from keras.models import Sequential
from keras.layers import Dense,Activation,Flatten,Dropout
from keras.layers import Conv2D,MaxPooling2D
from keras.callbacks import ModelCheckpoint
import tensorflow
from tensorflow import keras
model = keras.models.Sequential()

model=Sequential()

model.add(Conv2D(200,(3,3),input_shape=data.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
#The first CNN layer followed by Relu and MaxPooling layers

model.add(Conv2D(100,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
#The second convolution layer followed by Relu and MaxPooling layers

model.add(Flatten())
model.add(Dropout(0.5))
#Flatten layer to stack the output convolutions from second convolution layer
model.add(Dense(50,activation='relu'))
#Dense layer of 64 neurons
model.add(Dense(6,activation='softmax'))
#The Final layer with two outputs for two categories

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

model.summary()

"""#split"""

from sklearn.model_selection import train_test_split
train_data,test_data,train_target,test_target=train_test_split(data,new_target,test_size=0.1)

train_data.shape

train_target.shape

history=model.fit(train_data,train_target,epochs=20,validation_split=0.2)

from matplotlib import pyplot as plt

# plot the training loss and accuracy
N = 20
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), history.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), history.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), history.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), history.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="center right")
plt.savefig("CNN_WeatherModel")

"""#predict"""

plt.figure(figsize = (15, 4))
plotnumber = 1

for i in range(3):
    if plotnumber <= 2:
        ax = plt.subplot(1, 2, plotnumber)
        plt.imshow(test_data[i], cmap = 'binary')
  
        plt.axis('off')
    plotnumber += 1
plt.tight_layout()
plt.show()

loss,accuracy = model.evaluate(test_data,test_target)
print(f"Loss: {loss}")
print(f"Accuracy: {accuracy}")

y_probs = model.predict(train_data)
y_preds = y_probs.argmax(axis = 1)
y_preds[:100]

plt.figure(figsize=(15,4))
plt.style.use("ggplot")
for i in range(1):
    sample = random.choice(range(len(test_data)))
    plt.subplot(2,5,i+1)
    plt.subplots_adjust(hspace=0.3)
    plt.imshow(test_data[sample])
    plt.grid(False)
    plt.xlabel(f"Actual: {test_target[sample]}\n Predicted: {y_preds[sample]}")
    
plt.tight_layout()    
plt.grid(False)
plt.show()

model.save('/content/drive/MyDrive/THỰC HÀNH MÁY HỌC/model_CNN.h5')



