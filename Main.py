# imports serial and time libraries
from controls import *
from decimal import *
from datetime import datetime
import RPi.GPIO as GPIO
import serial
import csv
import time

ser = serial.Serial('/dev/ttyS0',115200)
power_key = 6
power_on(power_key)
gps_on(power_key)

while True:
    ser.write(('\x41\x54\x2b\x43\x47\x50\x53\x49\x4e\x46\x4f'+'\r\n').encode())
    time.sleep(1)
    line = ser.readline().decode('utf-8')
    time.sleep(.5)
    conversion(line)
    time.sleep(1)
    
    

    
