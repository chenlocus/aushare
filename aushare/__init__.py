# -*- coding:utf-8 -*- 
import codecs
import os

__version__ = codecs.open(os.path.join(os.path.dirname(__file__), 'VERSION.txt')).read()
__author__ = 'Hao Chen'

"""
for ASX financial data
"""
from aushare.stock.fundamental import (getAllASXListCode,getASXListName,getASXListIndustry,
	                                   getCompanyBasicInfo,getRevenueDiff,getWeeklyPrice,
	                                   getMeanPriceDiffPercentage)
