from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import pandas as pd
from pandas import DataFrame, read_csv
import matplotlib
import sys
from tkinter.ttk import *
import re


def openFile(*args):
    # opens a filedialog
    filename = fd.askopenfilename()
    location = str(filename)
    # convert the contents of that file in a df
    print(str(filename))
    if re.search(r'PMrev',str(filename))!='None':
        pd.set_option('display.max_columns', None)
        df = pd.read_csv(location,names =['Unnamed 0','Unnamed 1','Unnamed 2','Unnamed 3','Unnamed 4'\
        ,'Unnamed 5','Unnamed 6','Unnamed 7','Unnamed 8','Unnamed 9','Unnamed 10',\
        'Unnamed 11','Unnamed 12','Unnamed 13','Unnamed 14','Unnamed 15'\
        ,'Unnamed 16','Unnamed 17','Unnamed 18','Unnamed 19','Unnamed 20','Unnamed 21',
        'Unnamed 23','Unnamed 24','Unnamed 25','Unnamed 26','Unnamed 27'\
        ,'Unnamed 28','Unnamed 29','Unnamed 30','Unnamed 31','Unnamed 32','Unnamed 33',\
        'Unnamed 34','Unnamed 35','Unnamed 36','Unnamed 37','Unnamed 38',\
        'Unnamed 39','Unnamed 40','Unnamed 41','Unnamed 42','Unnamed 43','Unnamed 44',\
        'Test 0','Test 1','Test 2','Test 3','Test 4'\
        ,'Test 5','Test 6','Test 7','Test 8','Test 9','Test 10',\
        'Test 11','Test 12','Test 13','Test 14','Test 15'\
        ,'Test 16','Test 17','Test 18','Test 19','Test 20','Test 21',
        'Test 23','Test 24','Test 25','Test 26','Test 27'\
        ,'Test 28','Test 29','Last'])
        df.drop(df.index[:9],inplace= True)
        df = df.reset_index(drop=True)
        df.columns = df.iloc[0]
        df.drop(df.index[0], inplace = True)
        df = df.reset_index(drop=True)
        df.drop(df.index[0],inplace = True)
        index = df[df['Event Date'] == 'FOR TENTATIVE EVENTS'].index[0]
        print(index)
        df.drop(df.index[:index],inplace = True)
    else:
        df = pd.read_csv(location)
        for i, r in df.iterrows():
            if not pd.isnull(r[2]):
                print(df)
                df.drop(df.index[:i],inplace = True)
                df = df.reset_index(drop=True)
                df.columns = df.iloc[0]
                df.drop(df.index[0], inplace = True)
                df = df.reset_index(drop=True)
                df.drop(df.index[2],inplace = True)
                print(df['Event Date'])
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
