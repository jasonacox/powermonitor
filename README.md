# powermonitor
Monitor power usage through WiFi Smart Plug

This script will will poll the Smart Plugs for state and energy usage (Watts)

Instructions for Capatible Smart Plugs

To monitor a smart plug, you will need to know its IP address and Device ID.

## Setup
1. Download the Smart Life - Smart Living app for iPhone or Android. Pair with your smart plug (this is important as you cannot monitor a plug that has not been paired).  
	* https://itunes.apple.com/us/app/smart-life-smart-living/id1115101477?mt=8
	* https://play.google.com/store/apps/details?id=com.tuya.smartlife&hl=en
2. Device ID - Inside the app, select the plug you wish to monitor, select the three dot top right and "Device Info".  The page should display "Device ID" which the script will use to poll the plug.
3. IP Address - You will need to determine what IP address your network assigned to the Smart Plug - this is more difficult but tooks like `arp-scan` can help identify devices on your network.  WiFi Routers often have a list of devices connected as well.  Look for devices with a name like "ESP_xxxxxx".

## Run
You can use the following to pull and run the powermonitor docker container using the following command.  You will need to replace the enviroinmental values to your devices IP and ID values.

```
# run powermonitor container - replace with device ID and IP 
docker run -e PLUGID='01234567891234567890' -e PLUGIP="10.0.1.x" jasonacox/powermonitor
```

Docker Hub: https://hub.docker.com/r/jasonacox/powermonitor

## Build and Run

**OPTION 1**: Build a docker container using `Dockerfile`
```
# build powermonitor container
docker build -t powermonitor .

# run powermonitor container - replace with device ID and IP 
docker run -e PLUGID='01234567891234567890' -e PLUGIP="10.0.1.x" powermonitor
```

**OPTION 2**: Manually install required python libraries:  

* Edit `plugpower.py` and add your Device ID and IP Address.

```
# RaspberryPi 

sudo apt-get install python-crypto python-pip
pip install pycrypto
pip install Crypto
pip install pyaes
```

## Example Output
```
$ docker run -e PLUGID='01234567891234567890' -e PLUGIP="10.0.1.99" jasonacox/powermonitor

Polling Device 01234567891234567890 at 10.0.1.99
Dictionary {'devId': '01234567891234567890', 'dps': {'1': True, '2': 0, '4': 69, '5': 12, '6': 1181}}
Switch On: True
Power (W): 1.200000
Current (mA): 69.000000
Voltage (V): 118.100000
Projected usage (kWh):  Day: 0.028800  Week: 0.201600  Month: 0.873600

```

## Example Products 
* TanTan Smart Plug Mini Wi-Fi Enabled Outlet with Energy Monitoring - https://www.amazon.com/gp/product/B075Z17987/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1
* SKYROKU SM-PW701U Wi-Fi Plug Smart Plug - see https://wikidevi.com/wiki/Xenon_SM-PW701U
* Wuudi SM-S0301-US - WIFI Smart Power Socket Multi Plug with 4 AC Outlets and 4 USB Charging
