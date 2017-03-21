#Main file
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import pandas as pd
from pandas import DataFrame, read_csv
import matplotlib
import sys

def openFile(*args):
    # opens a filedialog
    filename = fd.askopenfilename()
    location = str(filename)

    # convert the contents of that file in a df
    df = pd.read_csv(location)
    df.drop(df.index[:5], inplace = True)
    df = df.reset_index(drop=True)
    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace = True)
    df = df.reset_index(drop=True)
    print(df)
    df.drop(df.index[2],inplace = True)
    df.to_csv('inq.csv')


#create a GUI
root = Tk()
root.title("Catering Analytics")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Button(mainframe, text="Open File", command=openFile).grid(column=3, row=3, sticky=W)
root.mainloop()
