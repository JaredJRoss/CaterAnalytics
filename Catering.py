#Main file
from tkinter import filedialog as fd
from tkinter import *
import pandas as pd
from pandas import DataFrame, read_csv
import matplotlib
import sys

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
