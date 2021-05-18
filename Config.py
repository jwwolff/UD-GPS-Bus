from globals import *
import configparser
from os import path 

#Config File Setup
config = configparser.ConfigParser()
#detects if a config file exists and creates one if it doesn't
if path.exists("config.ini") == False:
    config["Basic Settings"] = {
        "#Names of the Bus stops with line brakes to seperate each stop\n"
        "Bus-Stops": "Irving Commons\nGosiger\nRoesch Library\n1401 S Main St\nCurran Place\nMarriott",
        "Fullscreen": "True",
        "#Maximum Capacity of the bus\n"
        "Max-Capacity": "7",
        "DBHost":"64.93.229.203",
        "DBusername":"root",
        "DBpassword":"UDBus",
        "DBdatabase":"udbus",
        "BusID":"1"
        }
    with open('config.ini', 'w') as conf:
        config.write(conf)
#reads the config and processes variables
config.read("config.ini")
BusStops = config.get("Basic Settings","Bus-Stops").split("\n")
BusCap = config.get("Basic Settings","Max-Capacity")
user = config.get("Basic Settings","DBusername")
password = config.get("Basic Settings","DBpassword")
host = config.get("Basic Settings","DBHost")
database = config.get("Basic Settings","DBdatabase")
BusID = config.get("Basic Settings","BusID")
Fullscreen = config["Basic Settings"].getboolean("Fullscreen")