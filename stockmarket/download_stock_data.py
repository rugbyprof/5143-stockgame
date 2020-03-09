"""
BROKEN!!!
"""

#!/usr/local/bin/python3

import os,sys
import pandas as pd
import yfinance as yf
import yahoofinancials
import yfinance as yf
import json
import logging
from  random import shuffle
from pymongo import MongoClient
import requests
from fake_useragent import UserAgent
import csv

client = MongoClient()
db = client['stockdb']
infocollection = db["stock_data"]
histcollection = db["stock_hist"]

grabbed = []

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


symbol_path = "./data/symbol_data/all.csv"
info_path = "./data/symbol_info/"

def loadStockSymbols(path):
    symbols = []
    fp = open(path,'r')
    data = fp.readlines()
    for d in data:
        d = d.split(",")
        symb = d[0]
        if symb.isalnum() and not symb in symbols:
            symbols.append(symb)
    return symbols

def download1yrCsv(symbol):
    s = requests.Session()
    url = "https://finance.yahoo.com/quote/{symbol}/history?p={symbol}"
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}
    response = s.get(url)
    cookies = s.cookies.get_dict()
    
    url2 = "https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=1552103951&period2=1583722751&interval=1d&events=history&crumb=VsaXTVVlF0w"
 
    download = s.get(url2,headers=headers)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    print(my_list)
    sys.exit()


def getStockInfo(symbol):
    outpath = os.path.join(info_path,symbol+"_data.json")
    gotjson = False
    if os.path.isfile(outpath):
        print(f"{outpath} exists")
        try:
            f = open(outpath,"r")
            data = f.read()
            jdata = json.loads(data.info)
            gotjson = True
        except:
            print("Not valid json in file {symbol}")
            print("Getting data from web ...")


    if not gotjson:
        data = yf.Ticker(symbol)

        try:
            null = data.institutional_holders
        except:
            print(f"Exception getting:  {symbol} ... ")
            return

        try:
            jdata = json.loads(str(data.info))
        except:
            print("Not valid json in {symbol}")
            e = open("errors.log","a")
            e.write(f"{symbol} error getting ...\n")
            e.close()
            return

        print(f"Writing {outpath} ...")
        f = open(outpath,"w")
        f.write(json.dumps(jdata))
        f.close()

        if not os.path.isfile(outpath):
            print(f"Error writing {outpath} !!!")


def loadStockInfo(symbol):

    results = infocollection.find({"_id":symbol})

    if infocollection.count_documents({"_id":symbol}) != 0:
        print(f"Stock: {symbol} in mongo ...")
        return

    data = yf.Ticker(symbol)

    try:
        null = data.institutional_holders
    except:
        print(f"Exception getting:  {symbol} ... ")
        return

    print(f"Inserting {symbol} into mongo ...")
    data.info['_id'] = data.info["symbol"]

    id = infocollection.insert_one(data.info).inserted_id

def fixJsonFiles(symbols):
    bad = 0
    # Read in all the stock symbold into a list
    symbols = loadStockSymbols(symbol_path)
    for symbol in symbols:
        isbad = False
        inpath = os.path.join(info_path,symbol+"_data.json")
        outpath = os.path.join(info_path,symbol+"_data_fixed.json")
        if os.path.isfile(outpath):
            continue
        if os.path.isfile(inpath):
            print(inpath)
            f = open(inpath,"r")
            data = f.read()
            data = data.replace("'",'"')
            data = data.replace('None','null')
            data = data.replace('True','true')
            data = data.replace('False','false')

            try: 
                data = json.loads(data)
            except:
                bad += 1
                print(f"{inpath} is bad!!")
                isbad = True
            f.close()
            
            print(outpath)
            if not isbad:
                f = open(outpath,"w")
                f.write(json.dumps(data,indent=4))
                f.close()
    print(f"Bad: {bad}")

if __name__=='__main__':
    
    if os.path.isdir(os.path.dirname(__file__)):
        os.chdir(os.path.dirname(__file__))

    if not os.path.isfile(symbol_path):
        logging.critical(f"File doesn't exist: {symbol_path}")

    if not os.path.isdir(info_path):
        logging.warning(f"Directory doesn't exist: {info_path} creatin it now ...")
        os.mkdir(info_path)


    # Read in all the stock symbold into a list
    symbols = loadStockSymbols(symbol_path)

    #fixJsonFiles(symbols)
    
    # Shuffle the list so we get all over the alphabet instead
    # of alphabetical order
    shuffle(symbols)

    # loop through each symbol and get info
    for symbol in symbols:
        print(f"Trying {symbol} ... ")
        #getStockInfo(symbol)
        download1yrCsv("GOOG")
        



    # for symbol in symbols:
    #     if(os.path.isfile(os.path.join(info_path,symbol+'_max.json'))):
    #         continue
    #     try:
    #         stockLookup(symbol,"max",info_path)
    #     except AssertionError as error:
    #         print(error)
    #     else:
    #         try:
    #             fp = open('progress.dat','a')
    #             fp.write(f"Last stock processed: {symbol} \n")
    #         except FileNotFoundError as fnf_error:
    #             print(fnf_error)

    #     print(symbol)
