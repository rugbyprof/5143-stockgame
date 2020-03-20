#!/usr/local/Cellar/python@3.8/3.8.1/bin/python3
"""
This script should load a mongo DB called stock game with stock data and 
stock information. I'm uploading the actual DB's from mongoexport for everyone
to import. BUT if you want to mess around, here is my code.
"""
import csv, json
import sys,os
import glob
from pymongo import MongoClient
from scrape_info import get_industry_sector
import time
import random

# connect to local mongo db
client = MongoClient('mongodb://localhost:27017')

# choose a "collection" (will be created if it doesn't exist)
db = client['stockgame']

# Running in VSCode sets base dir at repo home and 
# I want it where file is being run
whereami = os.path.dirname(os.path.abspath(__file__))

# Change to where file being run is
os.chdir(whereami)

def delete_unnecessary_csvs():
    files = glob.glob("./data/StockData/*.csv")

    keepers = []

    files = sorted(files)

    # Use csv library to read in the file I chose to use for info
    stockreader = csv.DictReader(open("./data/SymbolData/nasdaq-listed_csv.csv"))
    for row in stockreader:
        keepers.append(row["Symbol"])
    
    for f in files:
        symbol = os.path.basename(os.path.abspath(f))
        symbol = symbol[:-4]

        if not symbol in keepers:
            os.remove(f"./data/StockData/{symbol}.csv")
            print(f"deleting {symbol}.csv")

def filter_stock_data():
    files = glob.glob("./data/StockData/*.csv")

    keepers = []

    # Use csv library to read in the file I chose to use for info
    stockreader = csv.DictReader(open("./data/SymbolData/nasdaq-listed_csv.csv"))
    for row in stockreader:
        keepers.append(row["Symbol"])
    
    for f in files:
        symbol = os.path.basename(os.path.abspath(f))
        symbol = symbol[:-4]

        if not symbol in keepers:
            query = { "Symbol": symbol }
            x = db['data_3yr'].delete_many(query) 
            print(f"{symbol} deleted {x.deleted_count} documents.")

def load_stock_info():
    count = 0
    # Get a list of all csv files in specified folder
    files = glob.glob("./data/StockData/*.csv")

    # Use csv library to read in the file I chose to use for info
    stockreader = csv.DictReader(open("./data/SymbolData/nasdaq-listed_csv.csv"))

    
    needed_symbols = [] # List of all stock symbols that we need info for
    symbols = []        # List of all stock symbols we have stock prices for

    files = sorted(files)

    count = 0

    # csv header (available columns)
    # Symbol,Company Name,Security Name,Market Category,Test Issue,Financial Status,Round Lot Size

    # build a needed list based on all csv files in the data folder
    for f in files:
        symbol = os.path.basename(os.path.abspath(f))
        needed_symbols.append(symbol[:-4])

    # Go through the csv file, and create an info object to insert into mongo
    for row in stockreader:
        filtered = {}
        if row["Symbol"] in needed_symbols:
            filtered["_id"] = row["Symbol"]
            filtered["Symbol"] = row["Symbol"]
            filtered["Name"] = row["Company Name"]
            filtered["Security_Name"] = row["Security Name"]
            filtered["Market_Category"] = row["Market Category"]
            filtered["Test_Issue"] = row["Test Issue"]
            filtered["Financial_Status"] = row["Financial Status"]
            filtered["Round_Lot_Size"] = row["Round Lot Size"]

            # Use beutiful soup to go get industry and sector info for a symbol
            filtered['industry'],filtered['sector'] = get_industry_sector(row["Symbol"])

            # put it in mongo
            result = db['stock_info'].insert_one(filtered)

            print(filtered)
            time.sleep(random.random() * 1.5)



def load_stock_data(start_year=1980,end_year=2021,collection_name='stock_data'):

    files = glob.glob("./data/StockData/*.csv")

    keepers = []

    # Use csv library to read in the file I chose to use for info
    stockreader = csv.DictReader(open("./data/SymbolData/nasdaq-listed_csv.csv"))
    for row in stockreader:
        keepers.append(row["Symbol"])

    files = glob.glob("./data/StockData/*.csv")

    files = sorted(files)

    count = 0

    for f in files:
        symbol = os.path.basename(os.path.abspath(f))
        print(symbol[:-4])
        stockreader = csv.DictReader(open(f))

        # Column Headers (for debugging)
        # Date,Open,High,Low,Close,Adj Close,Volume
        
        for row in stockreader:

            # pull date parts out for seperate columns 
            # should help with querying when date functions
            # are failing
            year,month,day = tuple(row['Date'].split("-"))
            row['Year'] = int(year)
            row['Month'] = int(month)
            row['Day'] = int(day)

            # Do we want to save this one?
            if not (int(year) >= start_year and int(year) <= end_year):
                continue

            row['Symbol'] = symbol[:-4] # grab symbol from file name

            if not row['Symbol'] in keepers:
                continue

            # Still put a properly formatted date in the object
            row['Date'] = datetime.datetime(int(year), int(month), int(day), 12, 0, 0).isoformat()

            

            # Rename column and make it a float.
            if row['Adj Close']:
                row['AdjClose'] = round(float(row['Adj Close']),2)
            else:
                # Adj Close had some bad data somewhere so skipping if previous
                # failed
                continue

            # remove this from row
            del row['Adj Close']

            # make all numbers floats 
            row['High'] = round(float(row['High']),2)
            row['Low'] = round(float(row['Low']),2)
            row['Close'] = round(float(row['Close']),2)
            row['Open'] = round(float(row['Open']),2)

            # create a "Name" entry because in the VSCode 
            # plugin this is what you see in the collection
            # explorer as an object name
            row['Name'] = row['Symbol']+"-"+row['Date']

            result = db[collection_name].insert_one(row)
            count += 1

if __name__=='__main__':
    #load_stock_data(2017,2021)
    #load_stock_info()
    #filter_stock_data()
    delete_unnecessary_csvs()