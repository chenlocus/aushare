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
import re



def getAllASXListCode():
    
    url = ct.ASXLIST_FILE
    if os.path.isfile(ct.ASXLIST_FILE_NAME):
        dataFile = ct.ASXLIST_FILE_NAME
    else:
        data = urllib.request.urlopen(url).read().decode('ascii','ignore')
        dataFile = StringIO(data)
    df =pd.read_csv(dataFile,header=1)
    return df['ASX code']
    
    
def getASXListName(code=None):
    
    url = ct.ASXLIST_FILE
    if os.path.isfile(ct.ASXLIST_FILE_NAME):
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
    if os.path.isfile(ct.ASXLIST_FILE_NAME):
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
    if os.path.isfile(ct.ASXLIST_FILE_NAME):
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
    
    file_name = ct.REVENUE_FILE%code
    try:
        if os.path.isfile(file_name):
            df = pd.read_csv(file_name,header=0, index_col =0)
        else:
            urlbase = ct.INCOME_ANNUAL_REPORT
            url = urlbase%(code,code)
            print(url)
            response = urllib.request.urlopen(url).read().decode('utf-8')
            soup = BeautifulSoup(response, "lxml")
            #tb = soup.find("table",attrs = {"data-reactid":"29"})
            tb = soup.find("table")
            df1 = pd.read_html(str(tb),header=0,index_col=0)
            df =df1[0].T
        df2 = pd.to_numeric(df["Total Revenue"],downcast='float')
    
        df3 = pd.DataFrame(data=df2.pct_change(periods=-1)).reset_index()
        df3.columns=['date','difference']
    except:
        print('No revenue report found for the code %s'%code)
        df3 =None
    return df3

def getRevenue(code='APT'):
    file_name = ct.REVENUE_FILE%code
    try:
        if os.path.isfile(file_name):
            df = pd.read_csv(file_name,header=0, index_col =0)
        else:
            urlbase = ct.INCOME_ANNUAL_REPORT
            url = urlbase%(code,code)
            print(url)
            response = urllib.request.urlopen(url).read().decode('utf-8')
            soup = BeautifulSoup(response, "lxml")
            #tb = soup.find("table",attrs = {"data-reactid":"29"})
            tb = soup.find("table")
            df1 = pd.read_html(str(tb),header=0,index_col=0)
            df =df1[0].T
    except:
        print('No revenue report found for the code %s'%code)
        df =None
        
    print(df)
    return df


def getWeeklyPrice(code='APT',Year='2016'):
    file_name = ct.WEEKLY_PRICE_FILE%code
    if os.path.isfile(file_name):
            df = pd.read_csv(file_name,header=0, index_col =0,date_parser=_parser,skipfooter =1,engine='python')
            df.reset_index(inplace =True)
            df1 = df[df['Date'].dt.year ==int(Year)]
            # df1 = df[df['Date'].str[:4] == Year]
            # if df1.empty or df1 is None:
            #     print('empty')
            #     df2 = df[df['Date'].str[-4:] == Year]
            #     return df2
            # else:
            #     return df1
            return df1
            
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
    if df1 is None or df1.empty:
        return None
    try:
        meanprice_year1 = df1['Adj. close**'].mean()
    except:
        meanprice_year1 = df1['Adj Close'].mean()
    print(meanprice_year1)
    
    df2 = getWeeklyPrice(code,endYear) 
    if df2.empty:
        return None
    
    try:
        meanprice_year2 = df2['Adj. close**'].mean()
    except:
        meanprice_year2 = df1['Adj Close'].mean()
    print(meanprice_year2)
    return 0 if meanprice_year1==0 else round(meanprice_year2-meanprice_year1,4)*100/meanprice_year1


#get mean price of certain year

def getYearMeanPrice(code,Year):
    df1 = getWeeklyPrice(code,Year) 
    if df1.empty:
        return None
    try:
        meanprice_year1 = df1['Adj. close**'].mean()
    except:
        meanprice_year1 = df1['Adj Close'].mean()
    print(meanprice_year1)
    
    return round(meanprice_year1,2)

#get balance sheet from annual report in yahoo finance

def getBalanceSheet(code='APT'):
    file_name = ct.BALANCE_SHEET_FILE%code
    if os.path.isfile(file_name):
            df = pd.read_csv(file_name,header=0, index_col =0)
            return df

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
    file_name = ct.CASHFLOW_FILE%code
    if os.path.isfile(file_name):
            df = pd.read_csv(file_name,header=0, index_col =0)
            return df
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

def getPerShareInfo(code = 'APT'):

    urlbase = ct.PERSHARE_FINANCIAL_INFO
    company_name = getASXListName(code).iloc[0].strip('.').replace(' ','-')
    try:
        url = urlbase%(code,company_name)
        print(url)
        response = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(response, "lxml")
        keyword = re.compile(code+' '+'Per Share',re.I)
        tb = soup.find(text=keyword).parent.parent.find("table")

        df1 = pd.read_html(str(tb),header=0,index_col=0)
        df =df1[0]
        df.fillna('0',inplace=True)
        #df['Sales']=df['Sales'].str.replace('$', '')
        print(df['Sales'])
        df['Sales']=df['Sales'].str.extract('(-?\d+\.*\d+)').astype(float)
        df['Cashflow']=df['Cashflow'].str.extract('(^-?\d+\.*\d+)').astype(float)/100
        df['Earnings']=df['Earnings'].str.extract('(^-?\d+\.*\d+)').astype(float)/100
        df['Dividends']=df['Dividends'].str.extract('(^-?\d+\.*\d+)').astype(float)/100
        df['Book Value']=df['Book Value'].str.extract('(^-?\d+\.*\d+)').astype(float)/100
    except:
        print('cannot find per share info')
        df =None

    print(df)
    return df

def getStatistics(code = 'APT'):
    urlbase = ct.STATISTICS_INFO
    url = urlbase%(code,code)
    print(url)
    try:
        response = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(response, "lxml")
        #keyword = re.compile(code+' '+'Per Share',re.I)
        keyword ='Valuation measures'
        tb = soup.find(text=keyword).parent.parent.next_sibling()[0].find_all("table")
        df1 = pd.read_html(str(tb),index_col=0)
        df =df1[0].T
        df.fillna('0',inplace=True)
        print (df['Market cap (intra-day) 5'].iloc[0])
        return (df)
    except:
        print('cannot find STATISTICS_INFO for symbol %s'%code)
        return None


def _parser(date):
    try:  
        return pd.datetime.strptime(date, '%d %b %Y')
    except:  
        try:
            return pd.datetime.strptime(date, '%d/%m/%Y')
        except:
            return pd.datetime.strptime(date, '%d %b. %Y')

def getHisWeeklyPrice(code='APT',datefrom='18/05/2018', dateto='18/09/2018'):
    file_name = ct.WEEKLY_PRICE_FILE%code
    if os.path.isfile(file_name):
            df = pd.read_csv(file_name,header=0, index_col =0,date_parser=_parser,skipfooter =1,engine='python')
            df.reset_index(inplace =True)
            datefrom = datetime.strptime(datefrom,'%d/%m/%Y')
            dateto = datetime.strptime(dateto,'%d/%m/%Y')
            df = df[(df['Date'] > datefrom) & (df['Date'] <= dateto)]
            return df

    try:
        urlbase = ct.WEEKLY_PRICE
        s = datefrom
        period1= int(time.mktime(datetime.strptime(s, "%d/%m/%Y").timetuple()))
        s = dateto
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


def getHisDailyPrice(code='APT',datefrom='18/05/2018', dateto='18/09/2018'):
    file_name = ct.DAILY_PRICE_FILE%code
    if os.path.isfile(file_name):
            df = pd.read_csv(file_name,header=0, index_col =0,date_parser=_parser,skipfooter =1,engine='python')
            df.reset_index(inplace =True)
            # datefrom = datetime.strptime(datefrom,'%d/%m/%Y')
            # dateto = datetime.strptime(dateto,'%d/%m/%Y')
            df = df[(df['Date'] > datefrom) & (df['Date'] <= dateto)]
            return df

    try:
        urlbase = ct.WEEKLY_PRICE
        s = datefrom
        period1= int(time.mktime(datetime.strptime(s, "%d/%m/%Y").timetuple()))
        s = dateto
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



