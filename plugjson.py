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
                sw =data['dps']['1']
                if '5' in data['dps'].keys():
                    w = (float(data['dps']['5'])/10.0)
                    mA = float(data['dps']['4'])
                    V = (float(data['dps']['6'])/10.0)
                    ret = "{ \"switch\": \"%s\", \"power\": \"%s\", \"current\": \"%s\", \"voltage\": \"%s\" }" % (sw, w, mA, V)
                    return(ret)
                else:
                    ret = "{ \"switch\": \"%s\" }" % sw
                    return(ret)
            else:
                ret = "{\"result\": \"Incomplete response from plug %s [%s].\"}" % (deviceid,ip)
                return(ret)
            break
        except KeyboardInterrupt:
            pass
        except:
            watchdog+=1
            if(watchdog>RETRY):
                ret = "{\"result\": \"ERROR: No response from plug %s [%s].\"}" % (deviceid,ip)
                return(ret)
            sleep(2)


responsejson = deviceInfo(PLUGID,PLUGIP,PLUGKEY)
print(responsejson)


