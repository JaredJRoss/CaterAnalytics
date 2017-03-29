from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import pandas as pd
from pandas import DataFrame, read_csv
import matplotlib
import sys
from tkinter.ttk import *

def openFile(*args):
    # opens a filedialog
    filename = fd.askopenfilename()
    location = str(filename)
    # convert the contents of that file in a df
    df = pd.read_csv(location)
    for i, r in df.iterrows():
        if not pd.isnull(r[2]):
            print(r[2])
            df.drop(df.index[:i],inplace = True)
            df = df.reset_index(drop=True)
            df.columns = df.iloc[0]
            df.drop(df.index[0], inplace = True)
            df = df.reset_index(drop=True)
            df.drop(df.index[2],inplace = True)
            break

    df.to_csv('inq.csv')

root = Tk()
root.title("Catering Analytics")

s = Style()
s.configure('My.TFrame', background='black')


mainframe = ttk.Frame(root, padding="12 12 12 12",style='My.TFrame')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=2)
mainframe.rowconfigure(0, weight=2)
mainframe['borderwidth'] = 2
mainframe['relief'] = 'sunken'

photo1 = PhotoImage(file = "Img11.png")
label1 = ttk.Label(mainframe,image = photo1)
label1.image = photo1 #reference!
label1.grid(column = 0,row = 0,  padx = 5, pady = 5)

photo2 = PhotoImage(file = "Img22.png")
label2 = ttk.Label(mainframe,image = photo2)
label2.image = photo2 #reference!
label2.grid(column = 0,row = 1,  padx = 5, pady = 5)

ttk.Button(mainframe, text="Open File", command=openFile).grid(column=0, row=3, sticky=S)

root.mainloop()
