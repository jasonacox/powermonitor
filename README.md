# powermonitor
Monitor power usage through WiFi Smart Plug

This script will will poll the Smart Plugs for state and energy usage (Watts)

Instructions for Capatible Smart Plugs

To monitor a smart plug, you will need to know its IP address and Device ID.

1. Download the Smart Life - Smart Living app for iPHone or Android. Pair with your smart plug (this is important as you cannot monitor a plug that has not been paired).  
	* https://itunes.apple.com/us/app/smart-life-smart-living/id1115101477?mt=8
	* https://play.google.com/store/apps/details?id=com.tuya.smartlife&hl=en
2. Device ID - Inside the app, select the plug you wish to monitor, select the three dot top right and "Device Info".  The page should display "Device ID" which the script will use to poll the plug.
3. IP Address - You will need to determine what IP address your network assigned to the Smart Plug - this is more difficult but tooks like `arp-scan` can help identify devices on your network.  WiFi Routers often have a list of devices connected as well.  Look for devices with a name like "ESP_xxxxxx".
4. Edit `plugpower.py` and add your Device ID and IP Address.
5. OPTION 1: Build a docker container using `Dockerfile`
```
# build powermonitor container
docker build -t powermonitor .

# run powermonitor container
docker run powermonitor
```
6. OPTION 2: Manually install required python libraries:  
```
# RaspberryPi 

sudo apt-get install python-crypto python-pip
pip install pycrypto
pip install Crypto
pip install pyaes
```

Example Products 
* TanTan Smart Plug Mini Wi-Fi Enabled Outlet with Energy Monitoring - https://www.amazon.com/gp/product/B075Z17987/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1
* SKYROKU SM-PW701U Wi-Fi Plug Smart Plug - see https://wikidevi.com/wiki/Xenon_SM-PW701U
* Wuudi SM-S0301-US - WIFI Smart Power Socket Multi Plug with 4 AC Outlets and 4 USB Charging
