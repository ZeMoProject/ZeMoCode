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
cat $account > ~/ACCOUNT

#Move .profile to enable autostart
cp ~/ZeMoCode/profile ~/.profile

#Install monitor drivers
wget https://raw.githubusercontent.com/adafruit/Adafruit-PiTFT-Helper/master/adafruit-pitft-helper2.sh
chmod +x adafruit-pitft-helper2.sh
sudo ./adafruit-pitft-helper2.sh
