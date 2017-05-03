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
    print(re.search(r'PMrevproj',str(filename)))
    #Sees if file is Projected Revenue File
    if re.search(r'PMrevproj',str(filename)) is not None:
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
        df.to_csv('PMRevProj.csv')
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
                year = r['Year']
            #makes the month tab hold both the month and year
            df.loc[i,'Month'] = r['Month']+" "+str(year)
        #drops the year tab since month keeps track of it
        df = df.drop('Year', axis=1)
        df_old =  pd.read_csv('Tasting.csv')
        df_old  = df_old.drop('Unnamed: 0', axis = 1)
        df = df.combine_first(df_old)
        df.to_csv('Tasting.csv')
        print(df)




root = Tk()
root.title("Catering Analytics")

s = Style()
s.configure('My.TFrame', background='grey')


mainframe = ttk.Frame(root, padding="12 12 12 12",style='My.TFrame')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
#mainframe.columnconfigure(0, weight=2)
#mainframe.rowconfigure(0, weight=2)
mainframe['borderwidth'] = 2
mainframe['relief'] = 'sunken'

photo1 = PhotoImage(file = "Image1.png")
label1 = ttk.Label(mainframe,image = photo1)
label1.image = photo1 #reference!
label1.grid(column = 0,row = 0,columnspan=3, padx = 5, pady = 5)

photo2 = PhotoImage(file = "Image2.png")
label2 = ttk.Label(mainframe,image = photo2)
label2.image = photo2 #reference!
label2.grid(column = 0,row = 1,columnspan=3,  padx = 5, pady = 5)

photo3 = PhotoImage(file = "Image3.png")
label3 = ttk.Label(mainframe,image = photo3)
label3.image = photo3 #reference!
label3.grid(column = 0,row = 3,columnspan=3,  padx = 3, pady = 3)




var1 = IntVar()
var = StringVar(mainframe)

def function():
    selection = var1.get()

    if  (selection == 1):
        var.set("Operations")

    elif (selection == 2):
        var.set("Culinary")

    else:
        var.set("Staffing")


Label(mainframe, text = "Choose a Metric to Calculate").grid(column = 0,row = 2,columnspan=3,  padx = 3, pady = 3)
Radiobutton(mainframe, text = "Operations", variable = var1, value = 1,width=15).grid(column = 0,row = 4,  padx = 3, pady = 3,sticky=W)
Radiobutton(mainframe, text = "Culinary", variable = var1, value = 2,width=15).grid(column = 1,row = 4,  padx = 3, pady = 3)
Radiobutton(mainframe, text = "Staffing", variable = var1, value = 3,width=15).grid(column = 2,row = 4,  padx = 3, pady = 3,sticky=E)
Button(mainframe, text = "OK", command = function).grid(column = 2,row = 6,  padx = 3, pady = 3,sticky=W)
#ttk.Button(mainframe, text="Open File", command=openFile,width=15).grid(column = 0,row = 5,columnspan=3,  padx = 3, pady = 3,sticky=(N,W,E,S))


start = StringVar()
end = StringVar()

label1 = ttk.Label( mainframe, text="From",width=5)
E1 = ttk.Entry(mainframe,textvariable=start,width=10)

label2 = ttk.Label( mainframe, text="To",width=5)
E2 = ttk.Entry(mainframe, textvariable= end,width=10)


label1.grid(column = 0,row = 6,sticky=W)
E1.grid(column = 1,row = 6,sticky=W)
label2.grid(column = 0,row = 7,sticky=W)
E2.grid(column = 1,row = 7,sticky=W)


#creates metrics based off dropdown selection
def CreateMetrics():
    
    if var.get() == "Operations":
        #read in project revenue csv we created
        df = pd.read_csv('PMRevProj.csv')
        start_date = datetime.strptime(start.get(),'%m/%d/%Y')
        end_date = datetime.strptime(end.get(),'%m/%d/%Y')
        #makes the eventdate a datetime object so we can manipulate it
        df['Event Date'] = pd.to_datetime(df['Event Date'])
        df['Subtotal'] = df['Subtotal'].astype(float)
        #gets event $ executed from dates in textbox
        EventDollars = df[df['Event Date'].between(start_date,end_date)]['Subtotal'].sum()
        #gets event # executed from dates in textbox
        EventCount = df[df['Event Date'].between(start_date,end_date)]['Event#'].count()
        #gets events covers
        Cover = df[df['Event Date'].between(start_date,end_date)]['Adult Guests'].sum()
        #gets avg check
        AvgCheck = EventDollars/Cover
    elif var.get() == "Culinary":
        print('culinary')
    elif var.get() == "Staffing":
        #read in both csv files
        df_rev = pd.read_csv('PMRevProj.csv')
        df_staffing = pd.read_csv('PMpostSched.csv')
        start_date = datetime.strptime(start.get(),'%m/%d/%Y')
        end_date = datetime.strptime(end.get(),'%m/%d/%Y')
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
        EventDollars = df_rev[df_rev['Event Date'].between(start_date,end_date)]['Subtotal'].sum()
        print('looking at')
        print('staff Costs')
        print(staffCosts)
        print('Event Dollars')
        print(EventDollars)
        print('staff Charges')
        print(staffCharges)
        staffProfit = EventDollars - staffCosts
        percent = 100*(staffCharges/staffProfit)
        print('Results')
        print('staff profit')
        print(staffProfit)
        print('percent')
        print(percent)
    else:
        print('none selected')



ttk.Button(mainframe, text="Get Metrics", command=CreateMetrics).grid(column=2, row=6,ipadx=2,ipady=2,sticky=E)


root.mainloop()
