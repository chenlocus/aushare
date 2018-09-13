# -*- coding:utf-8 -*- 
"""
Fundamental data interface 
Created on 2018/09/07
@author: Hao Chen
@contact: chenlocus@hotmail.com
"""
from aushare.stock import cons as ct 
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



def getAllASXListCode():
    
    url = ct.ASXLIST_FILE
    if os.path.isdir(ct.ASXLIST_FILE_NAME):
        dataFile = ct.ASXLIST_FILE_NAME
    else:
        data = urllib.request.urlopen(url).read().decode('ascii','ignore')
        dataFile = StringIO(data)
    df =pd.read_csv(dataFile,header=1)
    return df['ASX code']
    
    
def getASXListName(code=None):
    
    url = ct.ASXLIST_FILE
    if os.path.isdir(ct.ASXLIST_FILE_NAME):
        dataFile = ct.ASXLIST_FILE_NAME
    else:
        data = urllib.request.urlopen(url).read().decode('ascii','ignore')
        dataFile = StringIO(data)
    df =pd.read_csv(dataFile,header=1)
    if (code ==None):
        print(df['Company name'])
        return df['Company name']
    else:
        print(df['Company name'][df['ASX code']==code])
        return (df['Company name'][df['ASX code']==code])

def getASXListIndustry(code=None):
    
    url = ct.ASXLIST_FILE
    if os.path.isdir(ct.ASXLIST_FILE_NAME):
        dataFile = ct.ASXLIST_FILE_NAME
    else:
        data = urllib.request.urlopen(url).read().decode('ascii','ignore')
        dataFile = StringIO(data)
    df =pd.read_csv(dataFile,header=1)
    if (code ==None):
        return df['GICS industry group']
    else:
        return df['GICS industry group'][df['ASX code']==code]

def getCompanyBasicInfo(code=None):
    
    url = ct.ASXLIST_FILE
    if os.path.isdir(ct.ASXLIST_FILE_NAME):
        dataFile = ct.ASXLIST_FILE_NAME
    else:
        data = urllib.request.urlopen(url).read().decode('ascii','ignore')
        dataFile = StringIO(data)
    df =pd.read_csv(dataFile,header=1)
    if (code ==None):
        print(df['GICS industry group','Company name'])
        return df['GICS industry group','Company name']
    else:
        print(df[['GICS industry group','Company name']][df['ASX code']==code])
        return df[['GICS industry group','Company name']][df['ASX code']==code]


#get income from annual report in yahoo finance

def getRevenueDiff(code='APT'):
    
    try:
        urlbase = ct.INCOME_ANNUAL_REPORT
        url = urlbase%(code,code)
        print(url)
        response = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(response, "lxml")
        #tb = soup.find("table",attrs = {"data-reactid":"29"})
        tb = soup.find("table",attrs = ct.TB_INCOME)
        df1 = pd.read_html(str(tb),header=0,index_col=0)
        df =df1[0].T
        df2 = pd.to_numeric(df["Total Revenue"],downcast='float')
    
        df3 = pd.DataFrame(data=df2.pct_change(periods=-1)).reset_index()
        df3.columns=['date','difference']
    except:
        print('No revenue report found for the code %s'%code)
        df3 =None
        
    print(df3)
    return df3

def getWeeklyPrice(code='APT',Year='2016'):
    
    try:
        urlbase = ct.WEEKLY_PRICE
        s = "01/01/{}".format(Year)
        period1= int(time.mktime(datetime.strptime(s, "%d/%m/%Y").timetuple()))
        s = "31/12/{}".format(Year)
        period2= int(time.mktime(datetime.strptime(s, "%d/%m/%Y").timetuple()))
        code = code
        url = urlbase%(code,period1,period2)
        print(url)
        response = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(response, "lxml")
        tb = soup.find("table",attrs = {"data-test":"historical-prices"})
        na_values = ['NaN', 'N/A', '-']
        df1 = pd.read_html(str(tb),header=0,index_col=0,na_values=na_values)
        return df1[0]
    except:
        print('No weekly price found for the code ')
        return None

    
    
def getMeanPriceDiffPercentage(code,startYear,endYear):
    df1 = getWeeklyPrice(code,startYear) 
    if df1.empty:
        return None
    meanprice_year1 = df1['Close*'].mean()
    print(meanprice_year1)
    
    df2 = getWeeklyPrice(code,endYear) 
    if df2.empty:
        return None
    
    meanprice_year2 = df2['Close*'].mean()
    print(meanprice_year2)
    return 0 if meanprice_year1==0 else round(meanprice_year2-meanprice_year1,4)*100/meanprice_year1

#get balance sheet from annual report in yahoo finance

def getBalanceSheet(code='APT'):
    
    try:
        urlbase = ct.BALANCE_SHEET_ANNUAL_REPORT
        url = urlbase%(code,code)
        print(url)
        response = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(response, "lxml")
        tb = soup.find("table")
        df1 = pd.read_html(str(tb),header=0,index_col=0)
        df =df1[0].T
        # df2 = pd.to_numeric(df["Total Revenue"],downcast='float')
    
        # df3 = pd.DataFrame(data=df2.pct_change(periods=-1)).reset_index()
        # df3.columns=['date','difference']
    except:
        print('No balance sheet  found for the code %s'%code)
        df =None
    
    return df

#get cash flow from annual report in yahoo finance
def getCashflow(code='APT'):    
    try:
        urlbase = ct.CASH_FLOW_ANNUAL_REPORT
        url = urlbase%(code,code)
        print(url)
        response = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(response, "lxml")
        tb = soup.find("table")
        df1 = pd.read_html(str(tb),header=0,index_col=0)
        df =df1[0].T
    except:
        print('No cash flow  found for the code %s'%code)
        df =None
    
    return df



