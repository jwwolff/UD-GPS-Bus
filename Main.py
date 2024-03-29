# imports serial and time libraries
from Controls import *
from decimal import *
import datetime
import RPi.GPIO as GPIO
import serial
import csv
import time
import Config

ser = serial.Serial('/dev/ttyS0',115200)
power_key = 6
power_on(power_key)
gps_on(power_key)

while True:
    ser.write(('\x41\x54\x2b\x43\x47\x50\x53\x49\x4e\x46\x4f'+'\r\n').encode())
    time.sleep(.1)
    line = ser.readline().decode('utf-8')
    time.sleep(.1)
    gps_data = conversion(line)
    if gps_data is not None:
        Lat = gps_data[0]
        Long = gps_data[1]
        DBInsertgpsdata(datetime.datetime.today(),1,Lat,Long)
        print(Lat,Long)
    
    

    
