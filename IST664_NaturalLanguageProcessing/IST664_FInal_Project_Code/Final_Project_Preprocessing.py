#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import pandas as pd
import nltk
import re,os
# open and write csv file
csv_file = open('/Users/yibofeng/nlp/Final_Project_Data.csv', 'w', encoding='UTF-8', newline='')
myWriter=csv.writer(csv_file)
myWriter.writerow(["title","text"])
# read 2018_01
file_root1 = os.getcwd()+os.sep+"nlp/archive/2018_01"+os.sep
for file in os.listdir(path = file_root1):
    f = open(file_root1+file,"r",encoding="utf-8")
    for line in f.readlines():
        data_pyobj=json.loads(line)
        title=data_pyobj['title']
        text=data_pyobj['text']
        myWriter.writerow([title,text])
# read 2018_02
file_root2 = os.getcwd()+os.sep+"nlp/archive/2018_02"+os.sep
for file in os.listdir(path = file_root2):
    f = open(file_root2+file,"r",encoding="utf-8")
    for line in f.readlines():
        data_pyobj=json.loads(line)
        title=data_pyobj['title']
        text=data_pyobj['text']
        myWriter.writerow([title,text])
# read 2018_03
file_root3 = os.getcwd()+os.sep+"nlp/archive/2018_03"+os.sep
for file in os.listdir(path = file_root3):
    f = open(file_root3+file,"r",encoding="utf-8")
    for line in f.readlines():
        data_pyobj=json.loads(line)
        title=data_pyobj['title']
        text=data_pyobj['text']
        myWriter.writerow([title,text])

csv_file.close()



