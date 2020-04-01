#!/usr/local/Cellar/python@3.8/3.8.1/bin/python3
"""
This script opens `marketwatch.com` and finds the "sector" and "industry" for a given
stock symbol. Slooooooow, but it works ok.
"""
import sys,os
import requests
from bs4 import BeautifulSoup
import re

# Running in VSCode sets base dir at repo home and 
# I want it where file is being run
whereami = os.path.dirname(os.path.abspath(__file__))

# Change to where file being run is
os.chdir(whereami)

def get_industry_sector(symbol):
    URL = f"https://www.marketwatch.com/investing/stock/{symbol}/profile"
    page = requests.get(URL)

    if page.status_code != 200:
        return None,None

    block = None

    soup = BeautifulSoup(page.content, "html.parser")

    for elem in soup(text=re.compile(r'At a Glance')):
        block = elem.parent.parent

    if not block:
        return None,None
    
    info = block.find_all("div",class_="section") 

    for child in info:
        if len(child.contents) >=3:
            if child.contents[1].text == 'Industry':
                industry = child.contents[3].text
            if child.contents[1].text == 'Sector':
                sector = child.contents[3].text
        
    return (industry,sector)


if __name__=='__main__':
    i,s = get_industry_sector("GOOG")
    print(i,s)
    i,s = get_industry_sector("MSFT")
    print(i,s)
    i,s = get_industry_sector("ZZTOP")
    print(i,s)

