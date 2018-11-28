# -*- coding:utf-8 -*-
'''
Created on 2018/09/07
@author: Hao Chen
@contact: chenlocus@hotmail.com
'''

VERSION = '1.0'
ASXLIST_FILE_NAME = './data/ASXlistcodes.csv'
ASXLIST_FILE = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
INCOME_ANNUAL_REPORT = 'https://finance.yahoo.com/quote/%s.AX/financials?p=%s.AX'
BALANCE_SHEET_ANNUAL_REPORT = 'https://au.finance.yahoo.com/quote/%s.AX/balance-sheet?p=%s.AX'
CASH_FLOW_ANNUAL_REPORT = 'https://au.finance.yahoo.com/quote/%s.AX/cash-flow?p=%s.AX'
WEEKLY_PRICE ='https://au.finance.yahoo.com/quote/%s.AX/history?period1=%d&period2=%d&interval=1wk&filter=history&frequency=1wk'
PERSHARE_FINANCIAL_INFO ='https://www.investsmart.com.au/shares/asx-%s/%s/financials'
STATISTICS_INFO = 'https://au.finance.yahoo.com/quote/%s.AX/key-statistics?p=%s.AX'

BALANCE_SHEET_FILE = 'data/financial/%s_balance.csv'
REVENUE_FILE = 'data/financial/%s_revenue.csv'
CASHFLOW_FILE = 'data/financial/%s_cashflow.csv'
DELIST_FILE = 'data/ASXDelistcodes.csv'
WEEKLY_PRICE_FILE = 'data/weekly/%s_price.csv'
DAILY_PRICE_FILE = 'data/daily/%s_price.csv'



