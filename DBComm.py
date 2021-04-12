#!/usr/bin/python3 
import mariadb 

user="UDBus"
password="UDBus"
host="localhost"
database="udbus"


#methods for use in code
def DBInsertBuses(BusID,BusName):
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        database=database)
    cur = conn.cursor() 
    try: 
        cur.execute("INSERT INTO buses (BusID,BusName) VALUES (?, ?)", (BusID,BusName)) 
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.commit() 
    conn.close()

def DBInsertBusstopdata(BusID,BusStopID,PickedUp,DroppedOff,LeftBehind,Date):
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        database=database)
    cur = conn.cursor() 
    try: 
        cur.execute("INSERT INTO busstopdata (BusID,BusStopID,PickedUp,DroppedOff,LeftBehind,Date) VALUES (?, ?,?,?,?,?)", (BusID,BusStopID,PickedUp,DroppedOff,LeftBehind,Date)) 
    except mariadb.Error as e: 
        print(f"Error: {e}") 
    conn.commit() 
    conn.close()  

def DBInsertBusstops(BusStopID,BusStopName):
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        database=database)
    cur = conn.cursor() 
    try: 
        cur.execute("INSERT INTO busstops (BusStopID,BusStopName) VALUES (?, ?)", (BusStopID,BusStopName)) 
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.commit() 
    conn.close()

def DBInsertgpsdata(TimeStamp,BusID,Latitude,Longitude):
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        database=database)
    cur = conn.cursor() 
    try: 
        cur.execute("INSERT INTO gpsdata (TimeStamp,BusID,Latitude,Longitude) VALUES (?, ?,?,?)", (TimeStamp,BusID,Latitude,Longitude)) 
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.commit() 
    conn.close()


#retrieving information 
#some_name = "Georgi" 
#cur.execute("SELECT first_name,last_name FROM employees WHERE first_name=?", (some_name,)) 

#for first_name, last_name in cur: 
#    print(f"First name: {first_name}, Last name: {last_name}")
    
#insert information 


