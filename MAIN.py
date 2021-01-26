############################################################################
############################################################################

# This Python program will parse incoming GNSS data as well as connect
# SIM7600x to internet, this was created by UD-GPS team. All rights resevered
# University Of Dayton, 11/5/2020

# imports serial and time libraries
from decimal import *
from datetime import datetime
import RPi.GPIO as GPIO
import serial
import csv
import time


############################################################################
############################################################################
# Code for turning on and off GNSS Hat
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

# Opens serial connection between Rpi and SIM7600x, uses GPIO pins 14,15
ser = serial.Serial('/dev/ttyS0',115200)
ser.flush()

dir = r"/home/pi/"
with open(dir + 'Test1.csv','a+',newline='') as file: 
    writer = csv.writer(file)
    writer.writerow(["Latitude" , "Longitude"])
############################################################################
############################################################################

# This section conatins the commands used to activate the SIM7600x module
# go to manul for device and convert string commands to hex and format them
# using the examples below, can add more commands if needed 

# Command AT+CGPS = 0 to turn GNSS module off, will be used for kill switch 
Command_Power_Off_GNSS = ('\x41\x54\x2b\x43\x47\x50\x53\x3d\x30')

# Command AT+CGPS = 1 to tunr GNSS module on, will be used to activate GNSS 
Command_Power_On_GNSS = ('\x41\x54\x2b\x43\x47\x50\x53\x3d\x31\x2c\x31\x0a')

# Command AT+CGPSINFO to read parsed NMEA strings, contains GPS coordinates 
Command_INFO_GNSS = ('\x41\x54\x2b\x43\x47\x50\x53\x49\x4e\x46\x4f')

# Command AT to test the serial communication 
Command_Test_AT = ('\x41\x54')

# Sends AT command over serial interface to inititate communication  
ser.write((Command_Test_AT+'\r\n').encode())
#ser.write((Command_Power_Off_GNSS + '\r\n').encode())

############################################################################
############################################################################
# Creates while loop that will iterate through program continuosly 
power_key = 6
power_on(power_key)

while True:
    
    # Stops from overloading code from terminal window 
    time.sleep(.5)
    
    # Reads data from serial port and decods using utf-8 
    line = ser.readline().decode('utf-8')
    #print(line)
        
    # Sends command over serial interface to recieve GPS info (Lat,Long)
    ser.write((Command_INFO_GNSS+'\r\n').encode())
    
    # If the header +CGPSINFO is seen it will then be parsed 
    if (line[0:9] == '+CGPSINFO'):
        # replaces all dilemters with ',' then splits them into an array
        data = line.replace(': ',',').split(',')
        
        # splits the latitude into array that can later be rearranged and formatted in
        # readabel formate using equations below, can be checked with google maps, this
        # section reformats the latitude data entry
        
        digits = list(str(data[1]))
        lat_DD = digits[0] + digits[1]
        lat_DD = int(lat_DD)
        lat_MM = digits[2] + digits[3]
        lat_MMMM = digits[5] + digits[6] + digits[7] + digits[8] + digits[9] + digits[10]
        lat_MMMM = int(lat_MM)+ int(lat_MMMM)/1000000
        lat = lat_DD + lat_MMMM/60
        
        # This section will reformate the code for the longitude data entry, this will
        # make it a readabel formate, equations are same as above 
        digits = list(str(data[3]))
        long_DD = digits[0] + digits[1] + digits[2]
        long_DD = int(long_DD)
        
        # Formate the longitude data entry
        
        long_MM = digits[3] + digits[4]
        long_MMMM = digits[6] + digits[7] + digits[8] + digits[9] + digits[10] + digits[11]
        long_MMMM = int(long_MM) + int(long_MMMM)/1000000
        long = long_DD + long_MMMM/60
        
        # if first number is zero multiples negative 1 to allow
        # for correct representation fo binary number 
        if digits[0] == '0':
            long= long*-1
        
        # prints latitude and longitude to be checked
        time.sleep(.5)
        print("lat: " + str(lat) + " long: " + str(long))
        
        with open(dir + 'Test1.csv','a+',newline='') as file: 
            writer = csv.writer(file)
            writer.writerow([lat , long])

        
    
    


