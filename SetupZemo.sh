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
echo "$account" | cat - "$account" > ~/ZeMoCode/account

#Auto Start ZeMo on boot
cp ~/ZeMoCode/ZeMo.desktop ~/Desktop/
chmod 777 ~/Desktop/ZeMo.desktop
chmod 777 ~/ZeMoCode/Main.py
mkdir ~/.config/autostart
cp ~/ZeMoCode/ZeMo.desktop ~/.config/autostart/
chmod 777 ~/.config/autostart/ZeMo.desktop
touch ~/.config/autostart/ZeMo.desktop

sudo apt-get install xserver-xorg-video-fbdev
cat 'Section "Device"  
  Identifier "myfb"
  Driver "fbdev"
  Option "fbdev" "/dev/fb1"
EndSection' > /usr/share/X11/xorg.conf.d/99-fbdev.conf

#Install monitor drivers
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/adafruit-pitft.sh
chmod +x adafruit-pitft.sh
sudo ./adafruit-pitft.sh
