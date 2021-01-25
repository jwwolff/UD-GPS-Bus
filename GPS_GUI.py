
# This Python program will run the GUI interface needed to collect data by the bus driver
# will then write data to CSV file where it will be sent to email at end of work day
# this was created by UD-GPS team. All rights resevered University Of Dayton, 11/5/2020

import tkinter as tk
import csv
from datetime import date
from os import path 

############################################################################
############################################################################

today = date.today()
t = today.strftime("%m-%d-%y")

fields = (['Getting on', 'Getting Off', 'Left Behind', 'Bus Stop'])
ans = []
my_file = path.exists("Data " + t + '.csv')

if my_file == False:
    with open(("Data " + t + '.csv'),'a+',newline='') as file: 
        writer = csv.writer(file)
        writer.writerow([fields[0],fields[1],fields[2],fields[3]])

############################################################################
############################################################################

def fetch(entries):
    with open(("Data " + t + '.csv'),'a+',newline='') as file: 
        writer = csv.writer(file)
        for entry in entries:
            text = entry[1].get()
            if entry[1].get != text :
                text = (entry[1].get())
                ans.append(text)
        text_1 = ans[0]
        text_2 = ans[1]
        text_3 = ans[2]
        text_4 = ans[3]
        writer.writerow([text_1,text_2,text_3,text_4])
        ans.clear()

############################################################################
############################################################################

def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=30, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries

if __name__ == '__main__':
    root = tk.Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = tk.Button(root, text='Save',
                  command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Quit', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()