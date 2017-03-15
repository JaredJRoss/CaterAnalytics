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
print(df)
