from tkinter import *
from tkinter import filedialog as fd, ttk
import pandas as pd
from pandas import DataFrame, read_csv
import matplotlib
import sys
from tkinter.ttk import *
import re
import math
import os.path
import datetime as dt
from datetime import datetime, timedelta
from dateutil import parser
import calendar
import glob
from dateutil.relativedelta import relativedelta


#finds where the headers end for the report
def find_start(df):
    for i, r in df.iterrows():
        if not pd.isnull(r[1]):
            return i


#Makes the collumns the correct name
def resetColName(df):
        #finds where the data starts and drops the header rows
        df.drop(df.index[:find_start(df)],inplace= True)
        df = df.reset_index(drop=True)
        df.columns = df.iloc[0]
        #sets the column names in the dataframe and then drops them
        df.drop(df.index[0], inplace = True)
        df = df.reset_index(drop=True)
        #drops row with definitive
        df.drop(df.index[0],inplace = True)
        return df


#creates metrics based off dropdown selection
def CreateMetrics():
    df_metric = pd.read_csv("Scorecard.csv")
    df_metric['From'] = pd.to_datetime(df_metric['From'])
    df_metric['To'] = pd.to_datetime(df_metric['To'])

    df_temp = pd.DataFrame(columns  = df_metric.columns.values)
    if start.get() == "Pick A Date":
        today = datetime.now()
        today = today - dt.timedelta(days=5)
        offset = (today.weekday() - 2) % 7
        start_date = today - timedelta(days=offset)
    else:
        start_date = parser.parse(start.get())
    if end.get() == "Pick A Date":
        end_date = start_date + dt.timedelta(days=6)
    else:
        end_date = parser.parse(end.get())

    if var.get() == "Operations":
        #read in project revenue csv we created
        df = pd.read_csv('PMRevProj.csv')
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

        if df_metric[(df_metric['From'].dt.date == start_date.date()) & (df_metric['To'].dt.date == end_date.date())].empty:
            print("here")
            df_temp.loc[0,'From'] = start_date.date()
            df_temp.loc[0,'To'] = end_date.date()
            df_temp.loc[0,'Operations Event Executed Money'] = EventDollars
            df_temp.loc[0,'Operations - Event Number'] = EventCount
            df_temp.loc[0,'Operations - Cover'] = Cover
            df_temp.loc[0,'Operations - Avg Check'] = AvgCheck
            df_metric = df_metric.append(df_temp)
            print(df_metric)
            df_metric.to_csv('ScoreCard.csv' ,index=False)
        else:
            print('else')
            index = df_metric[(df_metric['From'].dt.date == start_date.date()) & (df_metric['To'].dt.date == end_date.date())].index.tolist()[0]
            df_metric.loc[index,'Operations Event Executed Money'] = EventDollars
            df_metric.loc[index,'Operations - Event Number'] = EventCount
            df_metric.loc[index,'Operations - Cover'] = Cover
            df_metric.loc[index,'Operations - Avg Check'] = AvgCheck
            df_metric.to_csv('ScoreCard.csv' ,index=False)

    elif var.get() == "Culinary":
        #Read csv
        df_culin = pd.read_csv('Tasting.csv')
        df_culin['Month'] = pd.to_datetime(df_culin['Month'])
        now = datetime.now()
        #gets the current years information only
        temp = df_culin[df_culin['Month'].dt.year==now.year]
        #finds from last 3 months and this one
        curr = temp[temp['Month'].between(now - relativedelta(months = 3),now)]
        #calculate percents
        signed = curr['Unsign Number'].sum()
        lost = curr['Unsign Signed'].sum()
        tentative = curr['Unsign Tentative'].sum()
        lost_tent = lost+(tentative*.744)
        if df_metric[(df_metric['From'].dt.date == start_date.date()) & (df_metric['To'].dt.date == end_date.date())].empty:
            df_temp.loc[0,'From'] = start_date.date()
            df_temp.loc[0,'To'] = end_date.date()
            df_temp.loc[0,'Culinary - Tasing Closings 2 Previous Month And Current'] = (lost_tent/signed)*100
            df_metric = df_metric.append(df_temp)
            print(df_metric)
            df_metric.to_csv('ScoreCard.csv' ,index=False)
        else:
            index = df_metric[(df_metric['From'].dt.date == start_date.date()) & (df_metric['To'].dt.date == end_date.date())].index.tolist()[0]
            df_metric.loc[index,'Culinary - Tasing Closings 2 Previous Month And Current'] = (lost_tent/signed)*100
            print(df_metric)
            df_metric.to_csv('ScoreCard.csv' ,index=False)
        print(signed)
        print(lost_tent)
        print(100*(lost_tent/signed))


    elif var.get() == "Staffing":
        #read in both csv files
        df_rev = pd.read_csv('PMRevProjDisc.csv')
        df_staffing = pd.read_csv('PMpostSched.csv')
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
        if df_metric[(df_metric['From'].dt.date == start_date.date()) & (df_metric['To'].dt.date == end_date.date())].empty:
            df_temp.loc[0,'From'] = start_date.date()
            df_temp.loc[0,'To'] = end_date.date()
            df_temp.loc[0,'Staffing - Staffing Profit'] = percent
            df_metric = df_metric.append(df_temp)
            print(df_metric)
            df_metric.to_csv('ScoreCard.csv' ,index=False)
        else:
            index = df_metric[(df_metric['From'].dt.date == start_date.date()) & (df_metric['To'].dt.date == end_date.date())].index.tolist()[0]
            df_metric.loc[index,'Staffing - Staffing Profit'] = percent
            print(df_metric)
            df_metric.to_csv('ScoreCard.csv' ,index=False)

    elif var.get() == "Sales":
        df_sales = pd.read_csv('PMRevProj.csv')
        #Gets the raw data to add tentative events
        #glob.glob() uses regex to find files ONLY ONE CSV FOR THAT REPORT CAN BE THERE AT TIME
        df_tent = pd.read_csv(glob.glob('Raw\\\\*mecreveprojbyae.csv')[0], names =['Unnamed 0','Unnamed 1','Unnamed 2','Unnamed 3','Unnamed 4'\
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
        df_tent = resetColName(df_tent)
        df_tent.drop('Discount', axis =1, inplace = True)
        index = df_tent[df_tent['Event Date'] == 'FOR TENTATIVE EVENTS'].index[0]
        df_tent.drop(df_tent.index[:index],inplace = True)
        df_sales['Definite']= pd.to_datetime(df_sales['Definite'])
        df_tent = df_tent[pd.notnull(df_tent['Event Date'])]
        df_tent['Event Date'] = pd.to_datetime(df_tent['Event Date'])
        df_tent[' Subtotal'] = df_tent[' Subtotal'].astype(float)
        df_sales[' Subtotal'] = df_sales[' Subtotal'].astype(float)

        #print(df_sales)
        #Signed Contracts, # and Signed Contracts, $
        SignedContractsNum = df_sales[df_sales['Definite'].between(start_date,start_date.replace(year = start_date.year + 2))][' Subtotal'].count()
        SignedContractsSum = df_sales[df_sales['Definite'].between(start_date,start_date.replace(year = start_date.year + 2))][' Subtotal'].sum()
        #New $$$ in the Month for the Month
        NewMonthMoney = df_sales[df_sales['Definite'].between(start_date.replace(day = 1),\
        start_date.replace(day = calendar.monthrange(start_date.year, start_date.month)[1]))][' Subtotal'].sum()
        #Current Month Tentative
        TentThisMonth = df_tent[df_tent['Event Date'].between(start_date.replace(day = 1),\
        start_date.replace(day = calendar.monthrange(start_date.year, start_date.month)[1]))][' Subtotal'].sum()
        print(NewMonthMoney)
        print(TentThisMonth)
        #Next month and Tenative
        start_date1 = start_date + relativedelta(months =1)
        NextMonthMoney = df_sales[df_sales['Definite'].between(start_date1.replace(day = 1),\
        start_date1.replace(day = calendar.monthrange(start_date1.year, start_date1.month)[1]))][' Subtotal'].sum()
        TentNextMonth = df_tent[df_tent['Event Date'].between(start_date1.replace(day = 1),\
                start_date1.replace(day = calendar.monthrange(start_date1.year, start_date1.month)[1]))][' Subtotal'].sum()
        start_date2 = start_date + relativedelta(months =2)
        #2 months ahead and Tentative
        TwoMonthMoney = df_sales[df_sales['Definite'].between(start_date2.replace(day = 1),\
        start_date2.replace(day = calendar.monthrange(start_date2.year, start_date2.month)[1]))][' Subtotal'].sum()
        TentTwoMonth = df_tent[df_tent['Event Date'].between(start_date2.replace(day = 1),\
                start_date2.replace(day = calendar.monthrange(start_date2.year, start_date2.month)[1]))][' Subtotal'].sum()

        if df_metric[(df_metric['From'].dt.date == start_date.date()) & (df_metric['To'].dt.date == end_date.date())].empty:
            df_temp.loc[0,'From'] = start_date.date()
            df_temp.loc[0,'To'] = end_date.date()
            df_temp.loc[0,'Sales - Signed Contracts Number'] = SignedContractsNum
            df_temp.loc[0,'Sales - Signed Contracts Money'] = SignedContractsSum
            df_temp.loc[0,'Sales - New Money in the Month'] = NewMonthMoney
            df_temp.loc[0,'Sales - Current Month Sales Money'] = NewMonthMoney
            df_temp.loc[0,'Sales - Current Month Sales Money Tentative'] = TentThisMonth
            df_temp.loc[0,'Sales - Next Month Sales Money'] = NextMonthMoney
            df_temp.loc[0,'Sales - Next Month Sales Money Tentative'] = TentNextMonth
            df_temp.loc[0,'Sales - Two Month Sales Money'] = TwoMonthMoney
            df_temp.loc[0,'Sales - Two Month Sales Money Tenative'] = TentTwoMonth
            df_metric = df_metric.append(df_temp)
            print(df_metric)
            df_metric.to_csv('ScoreCard.csv' ,index=False)
        else:
            index = df_metric[(df_metric['From'].dt.date == start_date.date()) & (df_metric['To'].dt.date == end_date.date())].index.tolist()[0]
            df_metric.loc[index,'Sales - Signed Contracts Number'] = SignedContractsNum
            df_metric.loc[index,'Sales - Signed Contracts Money'] = SignedContractsSum
            df_metric.loc[index,'Sales - New Money in the Month'] = NewMonthMoney
            df_metric.loc[index,'Sales - Current Month Sales Money'] = NewMonthMoney
            df_metric.loc[index,'Sales - Current Month Sales Money Tentative'] = TentThisMonth
            df_metric.loc[index,'Sales - Next Month Sales Money'] = NextMonthMoney
            df_metric.loc[index,'Sales - Next Month Sales Money Tentative'] = TentNextMonth
            df_metric.loc[index,'Sales - Two Month Sales Money'] = TwoMonthMoney
            df_metric.loc[index,'Sales - Two Month Sales Money Tenative'] = TentTwoMonth
            print(df_metric)
            df_metric.to_csv('ScoreCard.csv', index=False)

    elif var.get() == "All":
        print("here")
        var.set("Operations")
        CreateMetrics()
        var.set("Culinary")
        CreateMetrics()
        var.set("Staffing")
        CreateMetrics()
        var.set("Sales")
        CreateMetrics()
        var.set("All")
        print('done')

    else:
        print('none selected')


def win_deleted():
    print("window closed ")
    root.destroy()
    sys.exit()


def openFile(*args):
    # opens a filedialog
    filename = fd.askopenfilename()
    location = str(filename)
    # convert the contents of that file in a df
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
        df = resetColName(df)
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
        df.to_csv('PMRevProj.csv' ,index=False)


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
        df = resetColName(df)
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
        df.to_csv('PMRevProjDisc.csv' ,index=False)


    #sees if file is Post Schedule report
    elif re.search(r'PMpostsched',str(filename))is not None:
        #have to create  columns to reflect columns in data set so everything is filled correctly
        df = pd.read_csv(location,names =['Unnamed 0','Unnamed 1','Unnamed 2','Unnamed 3','Unnamed 4'\
        ,'Unnamed 5','Unnamed 6','Unnamed 7','Unnamed 8','Unnamed 9','Unnamed 10',\
        'Unnamed 11','Unnamed 12','Unnamed 13'])
        df = resetColName(df)

        df['Event Date'] = pd.to_datetime(df['Event Date'])
        df_old =  pd.read_csv('PMpostSched.csv')
        df_old['Event Date'] = pd.to_datetime(df_old['Event Date'])
        df_old  = df_old.drop('Unnamed: 0', axis = 1)
        df = df.combine_first(df_old)
        df.to_csv('PMpostSched.csv' ,index=False)
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
        df.to_csv('Tasting.csv' ,index=False)


def function():
    selection = var1.get()

    if  (selection == 1):
        var.set("Operations")

    elif (selection == 2):
        var.set("Culinary")

    else:
        var.set("Staffing")

#GUI
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
start.set("Pick A Date")
end.set("Pick A Date")
var.set("NULL") # initial value
option = OptionMenu(mainframe, var, 'Choose a Metric to Calculate',"Operations", "Culinary", "Staffing","Sales", "All")
option.grid()

label1 = ttk.Label( mainframe, text="From")
E1 = ttk.Entry(mainframe,textvariable=start)

label2 = ttk.Label( mainframe, text="To")
E2 = ttk.Entry(mainframe, textvariable= end)


label1.grid()
E1.grid()
label2.grid()
E2.grid()


root.protocol("WM_DELETE_WINDOW", win_deleted)
ttk.Button(mainframe, text="Get Metrics", command=CreateMetrics).grid(column=1, row=3, sticky=S)


root.mainloop()
