ZEMO: The Open Source Aquarium Monitor
======================================

# Introduction

ZeMo (derived from ZEbrafish MOnitor) is designed to be a low-cost, automated aquarium
monitoring system. It was created specifically with research zebrafish in mind, but can be
used for any aquatic species. Although customizable, it is designed to read water
temperature, pH, Conductivity (salt content), and Dissolved Oxygen. It also includes the
ability to view parameter histories online, and to receive remote notifications when
one or more measurements are outside the specified ranges. Assembly of the device is
designed to minimize the technical expertise needed, but should be done by someone with
basic soldering and command line experience.

More information can be found at zemoproject.org

# Assembly

Parts lists and assembly instruction can be found at zemoproject.org

# Software Installation

ZeMo uses a raspberry pi zero w to take measurements and post to the web. This requires
installation of the raspbian OS and ZeMo software onto a microSD card (8 GB recommended)
before device assembly. The device is then assembled and ZeMo setup on the device.

1. Download and install PiBakery from http://www.pibakery.org/
2. Open a new PiBakery window and create a custom script by connecting the following
blocks (or you can import the ZeMoPiBakeryRecipe.xml file on Github):
	- On first boot
	- Set user password (insert your desired password)
	- Set hostname (must be different from any others you have tied to your account)
	- Enable automatic loading of I2C kernal module
	- Set Pi Zero OTG Mode to Ethernet (usually defaults are fine)
	- Reboot
	- On every boot (this starts a new chain of blocks)
	- Enable VNC
3. Write to SD card
4. Assemble ZeMo
5. Plug into USB port and allow to startup.
6. Open terminal window on computer
7. Connect by typing ssh pi@rack1.local (substitute hostname you entered in step 2 for
"rack1")
8. Edit the wpa_supplicant to connect to the internet. This step depends on your
particular network configuration. More information is available from here (https://www.systutorials.com/docs/linux/man/5-wpa_supplicant.conf/) or from your
network administrator.
9. Run command: sudo reboot
10. After restarting, reconnect by ssh (see step 7)
11. Run command: git clone https://github.com/ZeMoProject/ZeMoCode
12. Run command: bash ~/ZeMoCode/SetupZemo.sh
13. Respond to prompts:
	- Enter ZeMo Account name. If you have not set one up, you may do so at zemoproject.org
	- Select configuration:
		1. **PiTFT 2.4", 2.8" or 3.2" resistive (240x320)**
		2. PiTFT 2.2" no touch (240x320)
		3. PiTFT 2.8" capacitive touch (240x320)
		4. PiTFT 3.5" resistive touch (320x480)
		5. Quit without installing
	- Select rotation:
		1. 90 degrees (landscape)
		2. 180 degrees (portait)
		3. **270 degrees (landscape)**
		4. 0 degrees (portait)
	- Would you like the console to appear on the PiTFT display? [y/n] **n**
	- Would you like the HDMI display to mirror to the PiTFT display? [y/n] **y**
	- REBOOT NOW? [y/N] **y**
14. After restarting, reconnect by ssh (see step 7)
15. Run command: sudo raspi-config
16. Change timezone, language, etc. for your location. See http://geek-university.com/raspberry-pi/internationalisation-options/ for more information.
