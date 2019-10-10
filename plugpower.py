#!/usr/bin/python
#
# PowerMonitor (Tuya Power Stats)
#      Power Probe - Wattage of smartplugs - Text Output

import pytuya
from time import sleep
import datetime
import os
import sys

# Read command line options or set defaults
if (len(sys.argv) < 2) and not (("PLUGID" in os.environ) or ("PLUGIP" in os.environ)):
    print('PowerMonitor (Tuya Power Stats)\n')
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

# How my times to try to probe plug before giving up
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


