from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import pandas as pd
from pandas import DataFrame, read_csv
import matplotlib
import sys
from tkinter.ttk import *
import re
import math


def find_start(df):
    for i, r in df.iterrows():
        if not pd.isnull(r[1]):
            return i

def openFile(*args):
    # opens a filedialog
    filename = fd.askopenfilename()
    location = str(filename)
    # convert the contents of that file in a df
    print(re.search(r'PMrevproj',str(filename)))
    if re.search(r'PMrevproj',str(filename)) is not None:
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
        df.drop(df.index[:find_start(df)],inplace= True)
        df = df.reset_index(drop=True)
        df.columns = df.iloc[0]
        df.drop(df.index[0], inplace = True)
        df = df.reset_index(drop=True)
        df.drop(df.index[0],inplace = True)
        index = df[df['Event Date'] == 'FOR TENTATIVE EVENTS'].index[0]
        df.drop(df.index[index-2:],inplace = True)
        df['Event Date'] = pd.to_datetime(df['Event Date'])
        df['Subtotal'] = df['Subtotal'].astype(float)
        print(df[df['Event Date'].between('3/1/2017','3/7/2017')]['Subtotal'])
        print(df[df['Event Date'].between('3/1/2017','3/7/2017')]['Subtotal'].sum())
    elif re.search(r'PMpostsched',str(filename))is not None:
        df = pd.read_csv(location,names =['Unnamed 0','Unnamed 1','Unnamed 2','Unnamed 3','Unnamed 4'\
        ,'Unnamed 5','Unnamed 6','Unnamed 7','Unnamed 8','Unnamed 9','Unnamed 10',\
        'Unnamed 11','Unnamed 12','Unnamed 13'])
        df.drop(df.index[:find_start(df)],inplace = True)
        df.columns = df.iloc[0]
        df.drop(df.index[0], inplace = True)
        df = df.reset_index(drop=True)
        print(df)
    elif re.search(r'Tasting',str(filename)) is not None:
        df = pd.read_excel(location)
        print(find_start(df))
        df.drop(df.index[:find_start(df)],inplace = True)
        df = df.reset_index(drop = True)
        df.columns = ['Year','Month','Total Tastings','Presign Number', 'Presign Lost', 'Unsign Number', 'Unsign Signed', \
        'Unsigned Lost', 'Unsign Tentative','Sign Ave','Total Signed Event Value',\
         'Total Lost Event Value', 'Total Tentative Event Value','Ave Signed Event Value','Ave Lost Event Value','Ave Tent Event Value']
        df = df[df['Month'] != 'Totals/Ave']
        df = df.dropna(subset=['Month'])
        year = 0
        for i, r in df.iterrows():
            if not math.isnan(r['Year']):
                year = r['Year']
            df.loc[i,'Month'] = r['Month']+" "+str(year)
        print(df)

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
