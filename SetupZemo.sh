#!/usr/bin/bash

cd ~

#Move .bashrc for autostart
cp ~/ZeMoCode/bashrc ~/.profile

#Install monitor drivers
wget https://raw.githubusercontent.com/adafruit/Adafruit-PiTFT-Helper/master/adafruit-pitft-helper2.sh
chmod +x adafruit-pitft-helper2.sh
printf "1\n3\ny\ny/n" | sudo ./adafruit-pitft-helper2.sh 
