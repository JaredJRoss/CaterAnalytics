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
import os.path
import datetime as dt
from datetime import datetime
from dateutil import parser


#finds where the headers end for the report
def find_start(df):
    for i, r in df.iterrows():
        if not pd.isnull(r[1]):
            return i

def openFile(*args):
    # opens a filedialog
    filename = fd.askopenfilename()
    location = str(filename)
    # convert the contents of that file in a df
    print(re.search(r'mecreveproj',str(filename)))
    #Sees if file is Projected Revenue File
    if re.search(r'mecreveproj',str(filename)) is not None:
        #have to create 74 columns to reflect columns in data set so everything is filled correctly
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
        #finds where the data starts and drops the header rows
        df.drop(df.index[:find_start(df)],inplace= True)
        df = df.reset_index(drop=True)
        df.columns = df.iloc[0]
        #sets the column names in the dataframe and then drops them
        df.drop(df.index[0], inplace = True)
        df = df.reset_index(drop=True)
        #drops row with definitive
        df.drop(df.index[0],inplace = True)
        #finds all tentative events and drops them
        index = df[df['Event Date'] == 'FOR TENTATIVE EVENTS'].index[0]
        df.drop(df.index[index-2:],inplace = True)
        df[' Subtotal'].fillna(0,inplace=True)
        df['Adult Guests'].fillna(0,inplace = True)
        #makes event date a datetime abject so it can be easily manipulated
        df['Event Date'] = pd.to_datetime(df['Event Date'])
        df.drop('Discount',axis=1,inplace=True)
        #loads data that is already available
        df_old =  pd.read_csv('PMRevProj.csv')
        df_old['Event Date'] = pd.to_datetime(df_old['Event Date'])
        df_old  = df_old.drop('Unnamed: 0', axis = 1)
        print(df_old.columns)
        print(df.columns)
        #Performs a union on all the data so new data is added without adding data already in the dataset
        df = df.combine_first(df_old)
        df.to_csv('PMRevProj.csv')
    #sees if file is Post Schedule report
    elif re.search(r'PMrevproj',str(filename)) is not None:
        #have to create 74 columns to reflect columns in data set so everything is filled correctly
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
        #finds where the data starts and drops the header rows
        df.drop(df.index[:find_start(df)],inplace= True)
        df = df.reset_index(drop=True)
        df.columns = df.iloc[0]
        #sets the column names in the dataframe and then drops them
        df.drop(df.index[0], inplace = True)
        df = df.reset_index(drop=True)
        #drops row with definitive
        df.drop(df.index[0],inplace = True)
        #finds all tentative events and drops them
        index = df[df['Event Date'] == 'FOR TENTATIVE EVENTS'].index[0]
        df.drop(df.index[index-2:],inplace = True)
        #makes event date a datetime abject so it can be easily manipulated
        df['Event Date'] = pd.to_datetime(df['Event Date'])
        df['Subtotal'] = df['Subtotal'].astype(float)
        #loads data that is already available
        df_old =  pd.read_csv('PMRevProj.csv')
        df_old['Event Date'] = pd.to_datetime(df_old['Event Date'])
        df_old  = df_old.drop('Unnamed: 0', axis = 1)
        #Performs a union on all the data so new data is added without adding data already in the dataset
        df = df.combine_first(df_old)
        print(df)
        df.to_csv('PMRevProjDisc.csv')
    #sees if file is Post Schedule report
    elif re.search(r'PMpostsched',str(filename))is not None:
        #have to create  columns to reflect columns in data set so everything is filled correctly
        df = pd.read_csv(location,names =['Unnamed 0','Unnamed 1','Unnamed 2','Unnamed 3','Unnamed 4'\
        ,'Unnamed 5','Unnamed 6','Unnamed 7','Unnamed 8','Unnamed 9','Unnamed 10',\
        'Unnamed 11','Unnamed 12','Unnamed 13'])
        #finds where the headers end
        df.drop(df.index[:find_start(df)],inplace = True)
        df.columns = df.iloc[0]
        df.drop(df.index[0], inplace = True)
        df = df.reset_index(drop=True)
        df['Event Date'] = pd.to_datetime(df['Event Date'])
        df_old =  pd.read_csv('PMpostSched.csv')
        df_old['Event Date'] = pd.to_datetime(df_old['Event Date'])
        df_old  = df_old.drop('Unnamed: 0', axis = 1)
        df = df.combine_first(df_old)
        df.to_csv('PMpostSched.csv')
        print(df)
    #sees if file is for Tasing report
    elif re.search(r'Tasting',str(filename)) is not None:
        #reads the file
        df = pd.read_excel(location)
        df.drop(df.index[:find_start(df)],inplace = True)
        df = df.reset_index(drop = True)
        #have to hard code names because collumns in report are across two lines
        df.columns = ['Year','Month','Total Tastings','Presign Number', 'Presign Lost', 'Unsign Number', 'Unsign Signed', \
        'Unsigned Lost', 'Unsign Tentative','Sign Ave','Total Signed Event Value',\
         'Total Lost Event Value', 'Total Tentative Event Value','Ave Signed Event Value','Ave Lost Event Value','Ave Tent Event Value']
        #gets rid of collumns that calculate totals
        df = df[df['Month'] != 'Totals/Ave']
        #drop empty months
        df = df.dropna(subset=['Month'])
        year = 0
        #goes through the dataframe
        for i, r in df.iterrows():
            #checks if the year tab is null and if not set that as the current year
            if not math.isnan(r['Year']):
                temp = int(str(r['Year'])[:4])
            #makes the month tab hold both the month and year
            df.loc[i,'Month'] = parser.parse(r['Month']).replace(year = temp, day = 1)
        #drops the year tab since month keeps track of it
        df = df.drop('Year', axis=1)
        df_old =  pd.read_csv('Tasting.csv')
        df_old  = df_old.drop('Unnamed: 0', axis = 1)
        df = df.combine_first(df_old)
        df.to_csv('Tasting.csv')




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

var = StringVar(mainframe)
start = StringVar()
end = StringVar()

var.set("one") # initial value
option = OptionMenu(mainframe, var, 'Choose a Metric to Calculate',"Operations", "Culinary", "Staffing")
option.grid()

label1 = ttk.Label( mainframe, text="From")
E1 = ttk.Entry(mainframe,textvariable=start)

label2 = ttk.Label( mainframe, text="To")
E2 = ttk.Entry(mainframe, textvariable= end)


label1.grid()
E1.grid()
label2.grid()
E2.grid()
#creates metrics based off dropdown selection
def CreateMetrics():
    if var.get() == "Operations":
        #read in project revenue csv we created
        df = pd.read_csv('PMRevProj.csv')
        start_date = parser.parse(start.get())
        end_date = parser.parse(end.get())
        #makes the eventdate a datetime object so we can manipulate it
        df['Event Date'] = pd.to_datetime(df['Event Date'])
        df[' Subtotal'] = df[' Subtotal'].astype(float)
        #gets event $ executed from dates in textbox
        EventDollars = df[df['Event Date'].between(start_date,end_date)][' Subtotal'].sum()
        #gets event # executed from dates in textbox
        EventCount = df[df['Event Date'].between(start_date,end_date)]['Event Date'].count()
        #gets events covers
        Cover = df[df['Event Date'].between(start_date,end_date)]['Adult Guests'].sum()
        #gets avg check
        AvgCheck = EventDollars/Cover
        print(AvgCheck)
    elif var.get() == "Culinary":
        df_culin = pd.read_csv('Tasting.csv')
        df_culin['Month'] = pd.to_datetime(df_culin['Month'])
        now = datetime.now()
        print(now.month-2)
        print(now.year)
        temp = df_culin[df_culin['Month'].dt.year==now.year]
        curr = temp[temp['Month'].between(now.replace(month = now.month-3 ),now)]
        print(curr)
        signed = curr['Unsign Number'].sum()
        lost = curr['Unsign Signed'].sum()
        tentative = curr['Unsign Tentative'].sum()
        lost_tent = lost+(tentative*.744)
        print(signed)
        print(lost_tent)
        print(100*(lost_tent/signed))
    elif var.get() == "Staffing":
        #read in both csv files
        df_rev = pd.read_csv('PMRevProjDisc.csv')
        df_staffing = pd.read_csv('PMpostSched.csv')
        start_date = parser.parse(start.get())
        end_date = parser.parse(end.get())
        #turns event date in both into date time objects
        df_rev['Event Date'] = pd.to_datetime(df_rev['Event Date'])
        df_staffing['Event Date'] = pd.to_datetime(df_staffing['Event Date'])
        # gets staff charges
        staffCharges  = df_rev[df_rev['Event Date'].between(start_date,end_date)]['Event Personnel'].sum()
        #narrows the dataframe to only include dates we want
        df_staffing = df_staffing[df_staffing['Event Date'].between(start_date,end_date)]
        #gets rid of any position type we dont want
        df_staffing = df_staffing[(df_staffing['Position Type'] != 'Mkt Event + Tasting Butler') & (df_staffing['Position Type'] != 'Production Kitchen at MEC')]
        print(df_staffing)
        #this is because floats cant have , for 1,000 it must be 1000
        df_staffing['Amount'] = df_staffing['Amount'].str.replace(',','')
        df_staffing['Amount'] = df_staffing['Amount'].astype(float)
        staffCosts = df_staffing['Amount'].sum()
        # gets money charged to customers
        print('looking at')
        print('staff Costs')
        print(staffCosts)
        print('staff Charges')
        print(staffCharges)
        staffProfit = staffCharges - staffCosts
        percent = 100*(staffProfit/staffCharges)
        print('Results')
        print('staff profit')
        print(staffProfit)
        print('percent')
        print(percent)
    elif var.get() == "Sales":
    else:
        print('none selected')



ttk.Button(mainframe, text="Get Metrics", command=CreateMetrics).grid(column=1, row=3, sticky=S)


root.mainloop()
