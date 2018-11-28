# -*- coding:utf-8 -*- 
"""
Fundamental data interface 
Created on 2018/09/07
@author: Hao Chen
@contact: chenlocus@hotmail.com
"""
from aushare.etf import cons as ct 
import urllib.request
import json
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import csv
import html.parser
import time
from datetime import datetime
import os
import re



def getAllETFListCode():
    
    url = ct.ETFLIST_FILE
    if os.path.isfile(ct.ETFLIST_FILE_NAME):
        dataFile = ct.ETFLIST_FILE_NAME
    else:
        data = urllib.request.urlopen(url).read().decode('ascii','ignore')
        dataFile = StringIO(data)
    df =pd.read_csv(dataFile,header=1)
    return df['Code']