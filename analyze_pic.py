import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Flatten, Dense, Dropout
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import numpy as np 
import pandas as pd 
from keras.preprocessing.image import img_to_array, load_img



def analyze_pic(filename = "../icaMark/plots/subj1_series1_6.png"):
    #the definition of cnn parameters    
    cnn = Sequential()
    cnn.add(Conv2D(filters=32, 
    kernel_size=(2,2), 
    strides=(1,1),
    padding='same',
    input_shape=(176,180,3),
    data_format='channels_last'))
    cnn.add(Activation('relu'))
    cnn.add(MaxPooling2D(pool_size=(2,2),
    strides=2))
    cnn.add(Conv2D(filters=64,
    kernel_size=(2,2),
    strides=(1,1),
    padding='valid'))
    cnn.add(Activation('relu'))
    cnn.add(MaxPooling2D(pool_size=(2,2),
    strides=2))
    cnn.add(Flatten())        
    cnn.add(Dense(64))
    cnn.add(Activation('relu'))
    cnn.add(Dropout(0.25))
    cnn.add(Dense(units=1, activation='sigmoid'))
    cnn.compile(loss='binary_crossentropy', optimizer='rmsprop')
    cnn.load_weights('../cnn_baseline.h5')
    #loading image 
    img = load_img(filename) 
    img.thumbnail((180, 176))
    x = img_to_array(img)  
    x = (x - 128.0) / 128.0
    dataset = np.ndarray(shape=(1, 176, 180, 3),dtype=np.float32)
    dataset[0] = x
    #getting cnn prediction
    return cnn.predict_classes(dataset)[0][0]