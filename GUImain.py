#!/usr/bin/python3
# This Python program will run the GUI interface needed to collect data by the bus driver
# will then write data to CSV file where it will be sent to email at end of work day
# this was created by UD-GPS team. All rights resevered University Of Dayton, 11/5/2020

from globals import *
import tkinter as tk
import csv
import datetime
from os import path 
import configparser
from sys import platform
from DBComm import *
import Config

############################################################################
############################################################################

#some variable setup
entryData = [0]*5
entries = []
date = datetime.date.today()
t = date.strftime("%m-%d-%y")

############################################################################
############################################################################
'''
#Config File Setup
config = configparser.ConfigParser()
#detects if a config file exists and creates one if it doesn't
if path.exists("config.ini") == False:
    config["Basic Settings"] = {
        "#Names of the Bus stops with line brakes to seperate each stop\n"
        "Bus-Stops": "Terminal Stop\nPython Stop\nConsole Stop",
        "Fullscreen": "True",
        "#Maximum Capacity of the bus\n"
        "Max-Capacity": "7",
        "DBHost":"64.93.229.203",
        "DBusername":"root",
        "DBpassword":"UDBus",
        "BusID":"1"
        }
    with open('config.ini', 'w') as conf:
        config.write(conf)
#reads the config and processes variables
config.read("config.ini")
BusStops = config.get("Basic Settings","Bus-Stops").split("\n")
BusCap = config.get("Basic Settings","Max-Capacity")
globals.user = config.get("Basic Settings","DBusername")
globals.password = config.get("Basic Settings","DBpassword")
globals.host = config.get("Basic Settings","DBHost")
globals.database = "udbus"
BusID = config.get("Basic Settings","BusID")
############################################################################
############################################################################
'''
fields = ['Getting on', 'Getting Off', 'Left at Stop', 'Bus Stop']
ans = []
my_file = path.exists("Data " + t + '.csv')

#Checks if a CSV file has been made for the day
if my_file == False:
    with open(("Data " + t + '.csv'),'a+',newline='') as file: 
        writer = csv.writer(file)
        writer.writerow(["Date:",fields[0],fields[1],fields[2],fields[3]])

############################################################################
############################################################################

#Writes a new row to the CSV file using data from gathered from GUI
#entryData is (0) Getting on (1) Getting Off (2) Left at Stop (3) Bus Stop (4) Current Capacity 
def fetch(entries):
    #quick code for testing

    DBInsertBusstopdata(BusID,1,entryData[0],entryData[1],entryData[2],datetime.datetime.today())

    with open(("Data " + t + '.csv'),'a+',newline='') as file: 
        writer = csv.writer(file)
        writer.writerow([date,entryData[0],entryData[1],entryData[2],entries[3][1].get()])
        entryData[0],entryData[1],entryData[2],entryData[3] = [0,0,0,0]
        entries[0][1].config(text = entryData[0])
        entries[1][1].config(text = entryData[1])
        entries[2][1].config(text = entryData[2])
        ans.clear()

############################################################################
############################################################################

# increment function for the buttons: simply adds 1 and updates the label
def increment(i):
    if i == 0:
        PassMod = 1
    elif i == 1:
        PassMod = -1
    else:
        PassMod = 0
    entryData[i] = entryData[i]+1
    entryData[4] = entryData[4]+1*PassMod
    entries[i][1].config(text = entryData[i])
    if(entryData[4] > int(BusCap)):
        entries[4][1].config(text = "Current Passengers: "+str(entryData[4])+" !Warning: Over Capacity!",fg="red")
    else:
        entries[4][1].config(text = "Current Passengers: "+str(entryData[4]),fg="black")
    

# decrement function for the buttons: Simply subtracts 1 and updates the label
def decrement(i):
    if i == 0:
        PassMod = 1
    elif i == 1:
        PassMod = -1
    else:
        PassMod = 0
    if entryData[i] != 0:
        entryData[i] = entryData[i]-1
        entryData[4] = entryData[4]-1*PassMod
    entries[i][1].config(text = entryData[i])
    if(entryData[4] > int(BusCap)):
        entries[4][1].config(text = "Current Passengers: "+str(entryData[4])+" !Warning: Over Capacity!",fg="red")
    else:
        entries[4][1].config(text = "Current Passengers: "+str(entryData[4]),fg="black")

# formats the main screen and sets up the GUI
def makeform(root, fields):
    row1 = tk.Frame(root)
    row2 = tk.Frame(root)
    row1.pack(expand=tk.YES,fill=tk.X,side=tk.TOP)
    row2.pack(expand=tk.YES,fill=tk.BOTH,side=tk.TOP)
    i = 0
    PassLabel = tk.Label(row1,text="Current Passengers: 0",padx=5,pady=5)
    PassLabel.pack(side=tk.LEFT)
    for field in fields:
        #Creates the Bus Stop dropdown menu
        if field == "Bus Stop":
            lab = tk.Label(row1, width = 10, text=field,padx=5,pady=5)
            BusStopVar = tk.StringVar()
            BusStopVar.set(BusStops[0])
            ent = tk.OptionMenu(row1,BusStopVar,*BusStops)
            entries.append((field,BusStopVar))
            #alinement in GUI
            lab.pack(side=tk.LEFT,expand=tk.YES,fill=tk.X)
            ent.pack(side=tk.RIGHT)
        #Creates the buttons for increasing a decreasing values
        else:
            col = tk.Frame(row2)
            lab = tk.Label(col, width = 10, text=field,padx=5,pady=5)
            ent = tk.Label(col,text=0,relief=tk.SUNKEN)
            entries.append((field,ent))
            button1 = tk.Button(col,text="+",font=("Arial",30),command=lambda idx = i: increment(idx))
            button2 = tk.Button(col,text="-",font=("Arial",30),command=lambda idx = i: decrement(idx))
            #alinement in GUI
            col.pack(side=tk.LEFT,expand=tk.YES,fill=tk.BOTH)
            lab.pack(side=tk.TOP)
            button1.pack(expand=tk.YES,fill=tk.BOTH)
            ent.pack(expand=tk.YES,fill=tk.BOTH,padx=6,pady=4)
            button2.pack(expand=tk.YES,fill=tk.BOTH)
        i = i+1
    entries.append(("Passengers",PassLabel))
    return entries


#code to the starts the GUI
if __name__ == '__main__':
    root = tk.Tk()
    row3 = tk.Frame(root)
    ents = makeform(root, fields)
    row3.pack(side=tk.BOTTOM)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = tk.Button(row3, text='Save', command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(row3, text='Quit', command=root.destroy)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    if Fullscreen:
        root.attributes('-fullscreen',True)
    root.mainloop()