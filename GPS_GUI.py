
# This Python program will run the GUI interface needed to collect data by the bus driver
# will then write data to CSV file where it will be sent to email at end of work day
# this was created by UD-GPS team. All rights resevered University Of Dayton, 11/5/2020

import tkinter as tk
import csv
import datetime
from os import path 

############################################################################
############################################################################
entryData = [0]*4
entries = []
date = datetime.date.today()
t = date.strftime("%m-%d-%y")

BusStops = ["Terminal Stop","Python Stop","Console Stop"]


fields = ['Getting on', 'Getting Off', 'Left at Stop', 'Bus Stop']
ans = []
my_file = path.exists("Data " + t + '.csv')

if my_file == False:
    with open(("Data " + t + '.csv'),'a+',newline='') as file: 
        writer = csv.writer(file)
        writer.writerow(["Date:",fields[0],fields[1],fields[2],fields[3]])

############################################################################
############################################################################

def fetch(entries):
    with open(("Data " + t + '.csv'),'a+',newline='') as file: 
        writer = csv.writer(file)
        writer.writerow([t,entryData[0],entryData[1],entryData[2],entries[3][1].get()])
        entryData[0],entryData[1],entryData[2],entryData[3] = [0,0,0,0]
        entries[0][1].config(text = entryData[0])
        entries[1][1].config(text = entryData[1])
        entries[2][1].config(text = entryData[2])
        ans.clear()

############################################################################
############################################################################

# def makeform(root, fields):
#     entries = []
#     for field in fields:
#         row = tk.Frame(root)
#         lab = tk.Label(row, width=30, text=field, anchor='w')
#         ent = tk.Entry(row)
#         row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
#         lab.pack(side=tk.LEFT)
#         ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
#         entries.append((field, ent))
#     return entries

# increment function for the buttons: simply adds 1 and updates the label
def increment(i):
    entryData[i] = entryData[i]+1
    entries[i][1].config(text = entryData[i])

# decrement function for the buttons: Simply subtracts 1 and updates the label
def decrement(i):
    entryData[i] = entryData[i]-1
    if entryData[i] < 0:
         entryData[i] = 0
    entries[i][1].config(text = entryData[i])

# formats the main screen and sets up the GUI
def makeform(root, fields):
    row1 = tk.Frame(root)
    row2 = tk.Frame(root)
    row1.pack()
    row2.pack(expand=tk.YES,fill=tk.BOTH)
    i = 0
    for field in fields:
        if field == "Bus Stop":
            lab = tk.Label(row1, width = 10, text=field,padx=5,pady=5)
            BusStopVar = tk.StringVar()
            BusStopVar.set(BusStops[0])
            ent = tk.OptionMenu(row1,BusStopVar,*BusStops)
            entries.append((field,BusStopVar))
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        else:
            col = tk.Frame(row2)
            lab = tk.Label(col, width = 10, text=field,padx=5,pady=5)
            ent = tk.Label(col,text=0,relief=tk.SUNKEN)
            entries.append((field,ent))
            button1 = tk.Button(col,text="+",font=("Arial",30),command=lambda idx = i: increment(idx))
            button2 = tk.Button(col,text="-",font=("Arial",30),command=lambda idx = i: decrement(idx))
            col.pack(side=tk.LEFT,expand=tk.YES,fill=tk.BOTH)
            lab.pack()
            button1.pack(expand=tk.YES,fill=tk.BOTH)
            ent.pack(expand=tk.YES,fill=tk.BOTH,padx=6,pady=4)
            button2.pack(expand=tk.YES,fill=tk.BOTH)
        i = i+1
    return entries



if __name__ == '__main__':
    root = tk.Tk()
    row3 = tk.Frame(root)
    ents = makeform(root, fields)
    row3.pack(side=tk.BOTTOM)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = tk.Button(row3, text='Save', command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(row3, text='Quit', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()