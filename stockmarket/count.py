#!/usr/local/Cellar/python@3.8/3.8.1/bin/python3
"""
This is a script I ran to keep showing db count in a collection
as I was inserting lots of data. Probably just slowed down the 
insert! :) 
"""
import csv, json
import sys,os
import glob
from pymongo import MongoClient

# connect to local mongo db
client = MongoClient('mongodb://localhost:27017')

# choose a "collection" (will be created if it doesn't exist)
db = client['stockgame']

# Running in VSCode sets base dir at repo home and 
# I want it where file is being run
whereami = os.path.dirname(os.path.abspath(__file__))

# Change to where file being run is
os.chdir(whereami)

while 1:
    result = db['data_med'].find({})
    countme = []
    for r in result:
        countme.append(r)
    print(len(countme))


