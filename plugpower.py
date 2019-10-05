#!/usr/bin/python
#
# Power Probe - Wattage of smartplugs - Text Output

import pytuya
from time import sleep
import datetime
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
    while True:
        try:
            d = pytuya.OutletDevice(deviceid, ip, key)
            if vers == '3.3':
                d.set_version(3.3)

            data = d.status()
            if(d):
                print('Dictionary %r' % data)
                print('Switch On: %r' % data['dps']['1'])

                if vers == '3.3':
                    if '19' in data['dps'].keys():
                        w = (float(data['dps']['19'])/10.0)
                        mA = float(data['dps']['18'])
                        V = (float(data['dps']['20'])/10.0)
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


print("Polling Device %s at %s with key %s and protocol version %s" % (PLUGID,PLUGIP,PLUGKEY,PLUGVERS))

devicepower = deviceInfo(PLUGID,PLUGIP,PLUGKEY,PLUGVERS)


