#!/usr/bin/python
#
# Power Probe - Wattage of smartplugs - Text Output

import pytuya
from time import sleep
import datetime
import os

# Device Info - EDIT THIS
DEVICEID="01234567891234567890"
DEVICEIP="10.1.1.1"
DEVICEKEY="0123456789abcdef"

PLUGID=os.getenv('PLUGID', DEVICEID)
PLUGIP=os.getenv('PLUGIP', DEVICEIP)
PLUGKEY=os.getenv('PLUGKEY', DEVICEKEY)

# how my times to try to probe plug before giving up
RETRY=5

def deviceInfo( deviceid, ip, key ):
    watchdog = 0
    while True:
        try:
            d = pytuya.OutletDevice(deviceid, ip, key)
            data = d.status()
            if(d):
                print('Dictionary %r' % data)
                print('Switch On: %r' % data['dps']['1'])
                if '5' in data['dps'].keys():
                    w = (float(data['dps']['5'])/10.0)
                    mA = float(data['dps']['4'])
                    V = (float(data['dps']['6'])/10.0)
                    day = (w/1000.0)*24
                    week = 7.0 * day
                    month = (week * 52.0)/12.0
                    print('Power (W): %f' % w)
                    print('Current (mA): %f' % mA)
                    print('Voltage (V): %f' % V)
                    print('Projected usage (kWh):  Day: %f  Week: %f  Month: %f' % (day, week, month))
                    return(float(data['dps']['5'])/10.0)
                else:
                    return(0.0)
            else:
                return(0.0)
            break
        except KeyboardInterrupt:
            pass
        except:
            watchdog+=1
            if(watchdog>RETRY):
                print("ERROR: No response from plug %s [%s]." % (deviceid,ip))
                return(0.0)
            sleep(2)


print("Polling Device %s at %s with key %s" % (PLUGID,PLUGIP,PLUGKEY))

devicepower = deviceInfo(PLUGID,PLUGIP,PLUGKEY)


