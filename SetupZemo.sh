#!/usr/bin/bash

#Confirm internet
wget -q --tries=10 --timeout=20 --spider http://google.com
if [[ $? -eq 0 ]]; then
        echo "Network connection successful."
else
        echo "No network found. Please connect to the internet before running this script."
		exit 1
fi

#Set account
read -p "ZeMo account name (Used to connect to online resources): " account
cat $account > ~/ZeMoCode/account

#Move .profile to enable autostart (doesn't work...)
cp -f ~/ZeMoCode/libfm.conf ~/.config/libfm/libfm.conf
cp ~/ZeMoCode/profile ~/.profile
cp ~/ZeMoCode/ZeMo.desktop ~/Desktop/
chmod 777 ~/Destop/ZeMo.desktop

#Install monitor drivers
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/adafruit-pitft.sh
chmod +x adafruit-pitft.sh
sudo ./adafruit-pitft.sh
chmod +x ~/ZeMoCode/Main.py
