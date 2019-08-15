#!/usr/bin/python
#
# Power Probe - Wattage of smartplugs - JSON Output

import pytuya
from time import sleep
import datetime
import os

# Device Info - EDIT THIS
DEVICEID="01234567891234567890"
DEVICEIP="10.1.1.1"

PLUGID=os.getenv('PLUGID', DEVICEID)
PLUGIP=os.getenv('PLUGIP', DEVICEIP)

# how my times to try to probe plug before giving up
RETRY=5

def deviceInfo( deviceid, ip ):
    watchdog = 0
    while True:
        try:
            d = pytuya.OutletDevice(deviceid, ip, '0123456789abcdef')
            data = d.status()
            if(d):
                print('Dictionary %r' % data)
                print('Switch On: %r' % data['dps']['1'])
                if '5' in data['dps'].keys():
                    print('Power (W): %f' % (float(data['dps']['5'])/10.0))
                    print('Current (mA): %f' % float(data['dps']['4']))
                    print('Voltage (V): %f' % (float(data['dps']['6'])/10.0))
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

print("Polling Device %s at %s" % (PLUGID,PLUGIP))

devicepower = deviceInfo(PLUGID,PLUGIP)


