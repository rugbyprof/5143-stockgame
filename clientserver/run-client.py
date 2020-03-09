#!/usr/bin/env python3

import random
import time
import subprocess

keys = ["morpheus","ring","dogface","gorilla","dog","camel","rhino"]

while 1:
    random.shuffle(keys)

    #output = subprocess.run(["python3", "app-client.py" ,"10.0.88.181" ,"6000" ,"search" ,keys[0]])
    output = subprocess.run(["python3", "app-client.py" ,"10.0.88.181" ,"6000" ,"search" ,"rhino"])

    time.sleep(.1)
