#!/bin/sh
echo "Virtual environment activated"
echo "Installing dependencies"
pip3 install https://github.com/google-coral/pycoral/releases/download/release->
pip install opencv-python

DIR="/users/pgrad/rajeeva/aswin_venv/RaspCaptcha"
if [ -d "$DIR" ]; then
  #Directory exists, so move into it and perform classification
  echo "Directory found, starting classification"
  cd RaspCaptcha
  ./classify_tflite.py --captcha-dir captchas_final --output stuff.txt --symbol>
else
  #Directory doesn't exist, git clone and perform classification
  echo "Directory not found, cloning from git"
  git clone https://github.com/aswinrajeevofficial/RaspCaptcha.git
  cd RaspCaptcha
  ./classify_tflite.py --captcha-dir captchas_final --output stuff.txt --symbol>
  exit 1
fi
