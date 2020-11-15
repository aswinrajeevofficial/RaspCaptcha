import tensorflow as tf
import os
import cv2
import numpy
import string
import random
import argparse
import tensorflow.keras as keras

# Convert the model
json_file = open('test.h5'+'.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = keras.models.model_from_json(loaded_model_json)
model.load_weights('test.h5.h5')
model.compile(loss='categorical_crossentropy',
                          optimizer=keras.optimizers.Adam(1e-4, amsgrad=True),
                          metrics=['accuracy'])
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('model.tflite', 'wb') as f:
  f.write(tflite_model)