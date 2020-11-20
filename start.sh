#!/bin/sh
echo "Virtual environment activated"
echo "Installing dependencies"
pip3 install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp38-cp38-linux_armv7l.whl
pip install opencv-python

DIR="/users/pgrad/rajeeva/aswin_venv/RaspCaptcha"
if [ -d "$DIR" ]; then
  #Directory exists, so move into it and perform classification
  echo "Directory found, starting classification"
  cd RaspCaptcha
  ./classify_tflite.py --captcha-dir captchas_final --output stuff.txt --symbols symbols.txt
  git add .
  git commit -m "Classified from script"
  git push https://github.com/aswinrajeevofficial/RaspCaptcha.git
else
  #Directory doesn't exist, git clone and perform classification
  echo "Directory not found, cloning from git"
  git clone https://github.com/aswinrajeevofficial/RaspCaptcha.git
  cd RaspCaptcha
  ./classify_tflite.py --captcha-dir captchas_final --output stuff.txt --symbols symbols.txt
  git add .
  git commit -m "Classified from script"
  git push https://github.com/aswinrajeevofficial/RaspCaptcha.git
  exit 1
fi
