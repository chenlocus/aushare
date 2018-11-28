
# coding: utf-8

# In[6]:


#增量/全部获取股价日线价格
#selenium with headless browser phamtomJS daily
#from 0 to today
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import timedelta
import datetime
from aushare.stock import cons as ct


DAILY_PRICE_DELTA = "https://au.finance.yahoo.com/quote/%s.AX/history?period1=0&period2=%s&interval=1d&filter=history&frequency=1d"


ASXLIST_FILE_NAME = './data/ASXlistcodes.csv'

def _parser(date):
    try:  
        return pd.datetime.strptime(date, '%d %b %Y')
    except:  
        try:
            return pd.datetime.strptime(date, '%d/%m/%Y')
        except:
            return pd.datetime.strptime(date, '%d %b. %Y')


#if __name__ == "__main__":
df =pd.read_csv(ASXLIST_FILE_NAME,header=1)
codelist = df['ASX code'].values
#codelist =['Z1P']
for symbol in codelist:
    file_name = ct.DAILY_PRICE_FILE%symbol
    
    if os.path.isfile(file_name):
        df = pd.read_csv(file_name,header=0, index_col =0,date_parser=_parser,skipfooter =1,engine='python')
        if (df.empty):
            continue
        df.reset_index(inplace =True)
        earliest_date = df['Date'].min()
        print(earliest_date)
        s2 = earliest_date -timedelta(days=1)
        print(s2)
        period2= int(time.mktime(s2.timetuple()))
        
        
        url = DAILY_PRICE_DELTA%(symbol,period2)
        no_of_pagedowns = 50
    else:
        print('file does not exist')
    browser = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')                
    print(url)
    browser.get(url)
    time.sleep(1)
    elem = browser.find_element_by_tag_name("body")
    
    
    while no_of_pagedowns:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        no_of_pagedowns-=1
        
    source_data = browser.page_source
    
    try:
        soup = BeautifulSoup(source_data, "lxml")
        tb = soup.find("table",attrs = {"data-test":"historical-prices"})
        na_values = ['NaN', 'N/A', '-']
        df1 = pd.read_html(str(tb),header=0,index_col=0,na_values=na_values)
        if df1[0] is not None:
            if os.path.isfile(file_name):
                df2 = df1[0]
                print(df2)
                df = pd.read_csv(file_name,header=0, index_col =0)
                df=df[:-1]
                print(df)
                df3 = [df,df2]
                result = pd.concat(df3)
                print(result)
                result.drop_duplicates(inplace=True)
                print('okokok nearly ok')
                result.to_csv(file_name)
            else:
                print('file does not exist')
    except:
        print("The instrument may be delisted.")
        continue
    browser.close()
    browser.quit()

