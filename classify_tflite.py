#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import cv2
import numpy
import string
import random
import argparse
import tflite_runtime.interpreter as tflite
import time

def decode(characters, y):
    y = numpy.argmax(numpy.array(y), axis=2)[:,0]
    return ''.join([characters[x] for x in y])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--captcha-dir', help='Where to read the captchas to break', type=str)
    parser.add_argument('--output', help='File where the classifications should be saved', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    args = parser.parse_args()

    if args.captcha_dir is None:
        print("Please specify the directory with captchas to break")
        exit(1)

    if args.output is None:
        print("Please specify the path to the output file")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()
    start_time = time.time()
    print("Classifying captchas with symbol set {" + captcha_symbols + "}")
    with open(args.output, 'w') as output_file:
        interpreter = tflite.Interpreter(model_path="model.tflite")
        files = os.listdir(args.captcha_dir)
        files = sorted(files)
        for x in files:
            # load image and preprocess it
            raw_data = cv2.imread(os.path.join(args.captcha_dir, x))
            rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
            image = numpy.array(rgb_data) / 255.0
            (c, h, w) = image.shape
            image = image.reshape([-1, c, h, w]).astype(numpy.float32)
            interpreter.allocate_tensors()
            input_index = interpreter.get_input_details()[0]["index"]
            output_details = interpreter.get_output_details()
            interpreter.set_tensor(input_index, image)
            interpreter.invoke()
            prediction = []
            for i in range(6):
                prediction.append(numpy.array(interpreter.get_tensor(output_details[i]['index'])))
            predictString = decode(captcha_symbols,prediction)
            predictString = predictString.replace(" ", "")
            output_file.write(x + "," + predictString + "\n")
            print('TFLite Classified ' + x)    
    print("--- %s seconds ---" % (time.time() - start_time))
if __name__ == '__main__':
    main()
