#!/usr/bin/python
#
# Power Probe - Wattage of smartplugs - JSON Output

import pytuya
from time import sleep
import datetime
import time
import os
import sys

# Device Info - EDIT THIS
DEVICEID=sys.argv[1]
DEVICEIP=sys.argv[2]
DEVICEKEY=sys.argv[3]
DEVICEVERS=sys.argv[4] if len(sys.argv) >= 5 else '3.1'

PLUGID=os.getenv('PLUGID', DEVICEID)
PLUGIP=os.getenv('PLUGIP', DEVICEIP)
PLUGKEY=os.getenv('PLUGKEY', DEVICEKEY)
PLUGVERS=os.getenv('PLUGVERS', DEVICEVERS)

# how my times to try to probe plug before giving up
RETRY=5

def deviceInfo( deviceid, ip, key, vers ):
    watchdog = 0
    now = datetime.datetime.utcnow()
    iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ") 
    while True:
        try:
            d = pytuya.OutletDevice(deviceid, ip, key)
            if vers == '3.3':
                d.set_version(3.3)

            data = d.status()
            if(d):
                sw =data['dps']['1']

                if vers == '3.3':
                    if '19' in data['dps'].keys():
                        w = (float(data['dps']['19'])/10.0)
                        mA = float(data['dps']['18'])
                        V = (float(data['dps']['20'])/10.0)
                        ret = "{ \"datetime\": \"%s\", \"switch\": \"%s\", \"power\": \"%s\", \"current\": \"%s\", \"voltage\": \"%s\" }" % (iso_time, sw, w, mA, V)
                        return(ret)
                    else:
                        ret = "{ \"switch\": \"%s\" }" % sw
                        return(ret)
                else:
                    if '5' in data['dps'].keys():
                        w = (float(data['dps']['5'])/10.0)
                        mA = float(data['dps']['4'])
                        V = (float(data['dps']['6'])/10.0)
                        ret = "{ \"datetime\": \"%s\", \"switch\": \"%s\", \"power\": \"%s\", \"current\": \"%s\", \"voltage\": \"%s\" }" % (iso_time, sw, w, mA, V)
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

responsejson = deviceInfo(PLUGID,PLUGIP,PLUGKEY,PLUGVERS)
print(responsejson)


