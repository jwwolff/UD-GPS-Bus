from decimal import *
from datetime import datetime
import RPi.GPIO as GPIO
import serial
import csv
import time
import mariadb 
import globals
from DBComm import *

ser = serial.Serial('/dev/ttyS0',115200)
ser.flush()

Command_Power_Off_GNSS = ('\x41\x54\x2b\x43\x47\x50\x53\x3d\x30')

Command_Power_On_GNSS = ('\x41\x54\x2b\x43\x47\x50\x53\x3d\x31\x2c\x31')

Command_INFO_GNSS = ('\x41\x54\x2b\x43\x47\x50\x53\x49\x4e\x46\x4f')

Command_Test_AT = ('\x41\x54')

def power_on(power_key):
    print('SIM7600X is starting:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(power_key,GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(20)
    ser.flushInput()
    print('SIM7600X is ready')

def power_down(power_key):
    print('SIM7600X is loging off:')
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(3)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(18)
    print('Good bye')

def gps_on(power_key):
    ser.write((Command_Power_On_GNSS+'\r\n').encode())
    time.sleep(1)
    line = ser.readline().decode('utf-8')
    time.sleep(.5)
    
def conversion(line):
    if (line[0:9] == '+CGPSINFO'):
        data = line.replace(': ',',').split(',')
        data.pop(0)
        data.pop(8)
        
        if (data == ['','','','','','','','']):
            print('GPS is not ready')
            time.sleep(.5)

        if (data != ['','','','','','','','']):
            digits = list(str(data[0]))
            lat_DD = digits[0] + digits[1]
            lat_DD = int(lat_DD)
            lat_MM = digits[2] + digits[3]
            lat_MMMM = digits[5] + digits[6] + digits[7] + digits[8] + digits[9] + digits[10]
            lat_MMMM = int(lat_MM)+ int(lat_MMMM)/1000000
            lat = lat_DD + lat_MMMM/60

            digits = list(str(data[2]))
            long_DD = digits[0] + digits[1] + digits[2]
            long_DD = int(long_DD)
                
            long_MM = digits[3] + digits[4]
            long_MMMM = digits[6] + digits[7] + digits[8] + digits[9] + digits[10] + digits[11]
            long_MMMM = int(long_MM) + int(long_MMMM)/1000000
            long = long_DD + long_MMMM/60
        
            if digits[0] == '0':
                long= long*-1
                
            time.sleep(.5)
            return [lat,long]
