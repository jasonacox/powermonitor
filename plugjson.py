#!/usr/bin/python
#
# PowerMonitor (Tuya Power Stats)
#      Power Probe - Wattage of smartplugs - JSON Output

import pytuya
from time import sleep
import datetime
import time
import os
import sys

# Read command line options or set defaults
if (len(sys.argv) < 2) and not (("PLUGID" in os.environ) or ("PLUGIP" in os.environ)):
    print('PowerMonitor (Tuya Power Stats) JSON Output\n')
    print('Usage: %s <PLUGID> <PLUGIP> <PLUGKEY> <PLUGVERS>\n' % sys.argv[0])
    print('    Required: <PLUGID> is the Device ID e.g. 01234567891234567890')
    print('              <PLUGIP> is the IP address of the smart plug e.g. 10.0.1.99')
    print('    Optional: <PLUGKEY> is the Device Keyy (default 0123456789abcdef)')
    print('              <PLUGVERS> is the Firmware Version 3.1 (defualt) or 3.3\n')
    print('    Note: You may also send values via Environmental variables: ')
    print('              PLUGID, PLUGIP, PLUGKEY, PLUGVERS\n')
    exit()
DEVICEID=sys.argv[1] if len(sys.argv) >= 2 else '01234567891234567890'
DEVICEIP=sys.argv[2] if len(sys.argv) >= 3 else '10.0.1.99'
DEVICEKEY=sys.argv[3] if len(sys.argv) >= 4 else '0123456789abcdef'
DEVICEVERS=sys.argv[4] if len(sys.argv) >= 5 else '3.1'

# Check for environmental variables and always use those if available (required for Docker)
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


