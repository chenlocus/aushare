
# coding: utf-8

# In[ ]:


# Flask
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr
from flask import Flask, request, g
from flask import render_template,jsonify
import urllib.request
import pandas as pd
import flask_monitoringdashboard as dashboard

# gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
# gevent end

import aushare.stock.fundamental as td
from aushare.stock import cons as ct
import os
from flask import send_file
from flask import abort

import time

app = Flask(__name__)
dashboard.config.init_from(file='dashboard.cfg')
dashboard.bind(app)
limiter = Limiter(
    app,
    key_func=get_ipaddr,
    #default_limits=["300 per day","2 per minute", "1 per second"],
    default_limits=["200 per day"],
)

MAX_SYMBOLS = 6

shared_limiter = limiter.shared_limit(limit_value="300 per day", key_func=get_ipaddr,scope="aaa")

my_ip_set = set()

@limiter.request_filter
def filter_func():
 
    if 'api_key' in request.args:
        api_key = request.args['api_key']
        print('api_key=',api_key)
    print('return false')
    return False


app.config.update(DEBUG=True)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("200 per day")
def homepage():

    return render_template("index.html")

@app.route('/api/v1/asx/snapshot/', methods=['GET'])
@shared_limiter
def getRealtimePrice():
    print("There is a request for realtime market snapshot.")
    print(request.args)
    print(get_ipaddr())
    my_ip_set.add(get_ipaddr())
    symbol = request.args['symbol']
    symbolist = symbol.split(',')
    
    symbollen = min(len(symbolist), MAX_SYMBOLS)
    print(symbollen)
    symbolist = symbolist[:symbollen]
    print(symbolist)
    
    dflist = []
    
    for symbol in symbolist:
        url = "https://www.asx.com.au/asx/1/share/%s"%symbol
        print(url)
        df = pd.read_json(url,orient='columns',typ='series')
        df = df[['code','bid_price','offer_price','open_price','last_price','change_in_percent',
                  'change_price','day_high_price','day_low_price','average_daily_volume','volume',
                   'previous_close_price','previous_day_percentage_change','eps','pe','annual_dividend_yield',
                   'market_cap','number_of_shares','year_change_in_percentage','year_change_price','year_high_date',
                  'year_high_price','year_low_date','year_low_price','year_open_date','year_open_price']]
        df_T = pd.DataFrame(df).transpose()
        dflist.append(df_T)
    result = pd.concat(dflist)
    result.set_index(['code'],inplace =True)

    print(result)
    return result.to_json(orient='index'),200


@app.route('/api/v1/asx/history/year/', methods=['GET'])
@shared_limiter
def getHistroyYearlyPrice():
    print("There is a request for histroical price yearly price.")
    print(request.args)
    my_ip_set.add(get_ipaddr())
    symbol = request.args['symbol']
    frequency = request.args['frequency']
    year = request.args['year']
    if frequency =='weekly':
        df = td.getWeeklyPrice(symbol,year).set_index('Date')
        df.rename(columns={"Close*": "Close", "Adj. close**": "Adjust Close"},inplace=True)
        try:
            df = df[df.Open.str.contains("Dividend") == False]
        except:
            print('this is not downloaded file')
        df.index = df.index.strftime('%Y-%m-%d')
        return (df.to_json(orient='index',date_format='iso',date_unit='s')),200

    return 'false request'


@app.route('/api/v1/asx/history/price/', methods=['GET'])
@shared_limiter
def getHistroyPrice():
    print("There is a request for histroical price within a range.")
    print(request.args)
    my_ip_set.add(get_ipaddr())
    symbol = request.args['symbol']
    frequency = request.args['frequency']
    datefrom = request.args['datefrom']
    dateto = request.args['dateto']
    
    if frequency =='weekly':
        df = td.getHisWeeklyPrice(symbol,datefrom,dateto).set_index('Date')
        df.rename(columns={"Close*": "Close", "Adj. close**": "Adjust Close"},inplace=True)
        df.index = df.index.strftime('%Y-%m-%d')
        return (df.to_json(orient='index',date_format='iso',date_unit='s')),200
    if frequency =='daily':
        df = td.getHisDailyPrice(symbol,datefrom,dateto).set_index('Date')
        df.rename(columns={"Close*": "Close", "Adj. close**": "Adjust Close"},inplace=True)
        try:
            df = df[df.Open.str.contains("Dividend") == False]
        except:
            print('this is not downloaded file')
        df.index = df.index.strftime('%Y-%m-%d')
        return (df.to_json(orient='index',date_format='iso',date_unit='s')),200

    return 'false request'


@app.route('/api/v1/asx/financial/balancesheet/', methods=['GET'])
@shared_limiter
def getBalanceSheet():
    print("There is a request for balance sheet in a year.")
    my_ip_set.add(get_ipaddr())
    symbol = request.args['symbol']
    year = request.args['year']
    df = td.getBalanceSheet(symbol)
    df = df[df.index.str[-4:] == year]
    df.rename(columns={"Total assets": "totalasset", "Total liabilities": "totaldebt","Net receivables":"receivable",
                   "Accounts payable":"payable","Total current assets":"currentassets",
                   "Total current liabilities":"currentdebts","Cash and cash equivalents":"totalcash","Net tangible assets":"nettangibleassets"},
                      inplace=True)
    df = df[["totalasset","totaldebt","receivable","payable","currentassets","currentdebts","totalcash","nettangibleassets"]]
    df.index = pd.to_datetime(df.index)
    df.index = df.index.strftime('%Y-%m-%d')
    return df.to_json(orient='index'),200

@app.route('/api/v1/asx/financial/cashflow/', methods=['GET'])
@shared_limiter
def getCashflow():
    print("There is a request for cash flow in a year.")
    my_ip_set.add(get_ipaddr())
    symbol = request.args['symbol']
    year = request.args['year']
    df = td.getCashflow(symbol)
    df = df[df.index.str[-4:] == year]
    df.rename(columns={"Total cash flow from operating activities":"cashfromoperating",
         "Capital expenditure":"capitalexpenditure",
          "Total cash flow from investment activities":"cashfrominvestment",
          "Total cash flow from financing activities":"cashfromfinancing",
          "Change in cash and cash equivalents":"changeincash"},
          inplace=True)
    df = df[["cashfromoperating",
            "capitalexpenditure",
            "cashfrominvestment",
            "cashfromfinancing",
            "changeincash"]]
    df.index = pd.to_datetime(df.index)
    df.index = df.index.strftime('%Y-%m-%d')
    return df.to_json(orient='index'),200


@app.route('/api/v1/asx/financial/revenue/', methods=['GET'])
@shared_limiter
def getRevenue():
    print("There is a request for revenue in a year.")
    my_ip_set.add(get_ipaddr())
    symbol = request.args['symbol']
    year = request.args['year']
    df = td.getRevenue(symbol)
    df = df[df.index.str[-4:] == year]
    df.rename(columns={"Total Revenue":"totalrevenue",
      "Cost of Revenue":"costofrevenue",
      "Gross Profit":"grossprofit",
      "Total Operating Expenses":"totalopexpense",
      "Earnings Before Interest and Taxes":"EBIT",
      "Income Before Tax":"incomebeforetax",
      "Net Income Applicable To Common Shares":"netincome"},
          inplace=True)
    df = df[["totalrevenue",
          "costofrevenue",
          "grossprofit",
          "totalopexpense",
          "EBIT",
          "incomebeforetax",
          "netincome"]]
    df.index = pd.to_datetime(df.index)
    df.index = df.index.strftime('%Y-%m-%d')
    return df.to_json(orient='index'),200

@app.route('/api/v1/asx/financial/valuation/', methods=['GET'])
@shared_limiter
def getValuation():
    print("There is a request for valuation of certain symbol.")
    my_ip_set.add(get_ipaddr())
    symbol = request.args['symbol']
    df = td.getStatistics(symbol)
    df.rename(columns={"Market cap (intra-day) 5":"marketcap",
      "Enterprise value 3":"enterprisevalue",
      "Trailing P/E":"PE",
      "Forward P/E 1":"anticipatedPE",
      "PEG ratio (5-yr expected) 1":"PEG",
      "Price/sales (ttm)":"PS",
      "Price/book (mrq)":"PB",
      "Enterprise value/revenue 3": "enterprisevalue2revenue",
      "Enterprise value/EBITDA 6":"enterprisevalue2EBITDA"},
          inplace=True)
    df['symbol'] = symbol
    df.set_index(['symbol'],inplace =True)
    print(df)


    return df.to_json(orient='index'),200

@app.route("/api/v1/asx/history/download/", methods=['GET'])
@shared_limiter
def DownloadFile ():
    my_ip_set.add(get_ipaddr())
    symbol = request.args['symbol']
    file_name = ct.DAILY_PRICE_FILE%symbol
    print(file_name)
    print('try to download')
    if os.path.isfile(file_name):
        try:
            return send_file(file_name, as_attachment=True),200
        except:
            abort(500)
    else:
        abort(404)
        

@app.route('/my_ip_set', methods=['GET', 'POST'])
def show_ip_set():
    newly_add_ip_len = len(my_ip_set)
    print ('newly add ip',my_ip_set)
    with open('listfile.txt', 'r') as filehandle:   
        existing_ips = filehandle.read().splitlines()
        print('existing ip',existing_ips)
        for existing_ip in existing_ips:
            my_ip_set.add(existing_ip)
        print('whole ip set',my_ip_set)

    with open('listfile.txt', 'w') as filehandle: 
        for listitem in my_ip_set:
          filehandle.write('%s\n' % listitem)
    total_ip_len = len(my_ip_set)
    my_ip_set.clear()

    return 'All IP addresses: %d，newly added IP: %d'%(total_ip_len, newly_add_ip_len)

    

if __name__ == "__main__":
    #app.run()
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    

