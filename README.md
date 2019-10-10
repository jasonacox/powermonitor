# PowerMonitor (Tuya Power Stats)
Monitor power usage through WiFi Smart Plug

This script will will poll [Tuya](https://en.tuya.com/) campatible Smart Plugs for state (on/off), current (mA), voltage (V), and power (wattage).  

This project is based on the python pytuya library to poll [Tuya](https://en.tuya.com/) campatible Smart Plugs for state and power data that can be used for point in time monitoring or stored for trending.  There are two scripts here. The `powerplug.py` script responds with a human redable output of state (on/off), current (mA), voltage (V), and power (W).  The `powerjson.py` script responds with JSON containing the same but adds a timestamp for convient time series processing.

REQUIRED: IP address and Device ID of  smart plug.

## Preparation
1. Download the Smart Life - Smart Living app for iPhone or Android. Pair with your smart plug (this is important as you cannot monitor a plug that has not been paired).  
	* https://itunes.apple.com/us/app/smart-life-smart-living/id1115101477?mt=8
	* https://play.google.com/store/apps/details?id=com.tuya.smartlife&hl=en
2. Device ID - Inside the app, select the plug you wish to monitor, select the 3 dots(Jinvoo) or the edit/pencil icon(Tuya & SmartLife) in the top right and then "Device Info".  The page should display "Device ID" which the script will use to poll the plug. It's also worth noting the MAC address of the device as it can come in handy in step 3.
3. IP Address - If your router displays a list of all the devices that are connected to it, you can search for the MAC address of the device. This is often the quickest way to locate your device IP.

	Alternatively, you will need to manually determine what IP address your network assigned to the Smart Plug - this is more difficult but it looks like `arp-scan` can help identify devices on your network.  WiFi Routers often have a list of devices connected as well. Look for devices with a name like "ESP_xxxxxx". Many modern routers allow you to set the hostname of connected devices to something more memorable, once you have located it.

4. Firmware Version - Devices with newer firmware (1.0.5 and above) are typically using a different protocol. These devices need to be communicated with using encryption and the resultant data is packaged slightly differently. It's a good idea therefore to check the Firmware version of the device(s) too. Again in the Tuya/SmartLife/Jinvoo app there will be a device option "Check for Firmware Upgrade" or similar. Open this option and take note of the Wi-Fi Module & MCU Module numbers. These are usually the same.

5. Device Key - If your device is running Firmware 1.0.5 or above, you will need to obtain the Device Key. This is used to connect with the device  decrypt the power consumption data. For details on how to do this, see point 2: https://github.com/clach04/python-tuya/wiki 


## Setup: Option 1 - Docker

Build a docker container using `Dockerfile` or get it at Docker Hub: https://hub.docker.com/r/jasonacox/powermonitor
```
# build powermonitor container
docker build -t powermonitor .

# Devices with older firmware (1.0.4 and below)
# run powermonitor container - replace with device ID and IP 
docker run -e PLUGID='01234567891234567890' -e PLUGIP="10.0.1.x" -e PLUGKEY="0123456789abcdef" powermonitor

# Devices with newer firmware (1.0.5 and above)
# run powermonitor container - replace with device ID and IP 
docker run -e PLUGID='01234567891234567890' -e PLUGIP="10.0.1.x" -e PLUGKEY="0123456789abcdef" -e PLUGINVERS="3.3"  powermonitor
```

## Setup: Option 2 - Manually (Tested on RaspberryPi):  

The script does not need docker but it does require the pycrypto python library. Follow these steps to set it up and run the script:

1. Install pip and python libraries if you haven't already:

```
 sudo apt-get install python-crypto python-pip		
 pip install pycrypto
 pip install Crypto		# some systems will need this
 pip install pyaes		# some systems will need this
```

2. Run the python script:
```
 #Devices with older firmware (1.0.4 and below)
 python plugpower.py {DEVICEID} {DEVICEIP} {DEVICEKEY [optional]} {DEVICEVERS [optional]}
```
eg:
```
 #Devices with older firmware (1.0.4 and below)
 python plugpower.py 01234567890 10.0.1.99 0123456789abcdef
```

```
 #Devices with newer firmware (1.0.5 and above)
 python plugpower.py 01234567890 10.0.1.99 0123456789abcdef 3.3
```

## JSON Output Script
The `plugjson.py` script works the same as `plugpower.py` but produces the data in JSON output with a datetime stamp.  This makes it easier to feed into other systems for recording, alerting or graphing.

## Example Output
### Docker
```
$ docker run -e PLUGID='01234567891234567890' -e PLUGIP="10.0.1.99" -e PLUGKEY="0123456789abcdef" jasonacox/powermonitor

Polling Device 01234567891234567890 at 10.0.1.99 with key 0123456789abcde1
Dictionary {'devId': '01234567891234567890', 'dps': {'1': True, '2': 0, '4': 69, '5': 12, '6': 1181}}
Switch On: True
Power (W): 1.200000
Current (mA): 69.000000
Voltage (V): 118.100000
Projected usage (kWh):  Day: 0.028800  Week: 0.201600  Month: 0.873600
```

### Command Line / Bash Script
```
$ bash test.sh 01234567890 10.0.1.99 0123456789abcdef 3.1
JSON Output - plugjson.py:
{ "datetime": "2019-08-31T07:20:59Z", "switch": "True", "power": "1.2", "current": "70.0", "voltage": "122.1" }

TEXT Output - plugpower.py:
Polling Device 01234567891234567890 at 10.0.1.99 with key 0123456789abcde1
Dictionary {u'devId': u'01234567891234567890', u'dps': {u'1': True, u'2': 0, u'5': 13, u'4': 70, u'6': 1220}}
Switch On: True
Power (W): 1.300000
Current (mA): 70.000000
Voltage (V): 122.000000
Projected usage (kWh):  Day: 0.031200  Week: 0.218400  Month: 0.946400
```

Please note, these smart plugs and this script do not hold power usage data in memory so the "Projected usage" reported is an estimate based on current power readings and assumed steady state over time. 

## Example Products 
* TanTan Smart Plug Mini Wi-Fi Enabled Outlet with Energy Monitoring - https://www.amazon.com/gp/product/B075Z17987/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1
* SKYROKU SM-PW701U Wi-Fi Plug Smart Plug - see https://wikidevi.com/wiki/Xenon_SM-PW701U
* Wuudi SM-S0301-US - WIFI Smart Power Socket Multi Plug with 4 AC Outlets and 4 USB Charging
* Gosund SP1 - WiFi High Amp RatedSmart Power Socket (eu) using 3.3 Protocol - see https://www.amazon.de/Steckdose-Stromverbrauch-Funktion-Fernsteurung-Netzwerk/dp/B07B911Y6V


## Acknowledgements
* https://github.com/clach04/python-tuya

## Contributers
* Phill Healey ([codeclinic](https://github.com/codeclinic)) - Integration for firmwares (1.0.5+) / protocol v3.3 & commandline arguments.
