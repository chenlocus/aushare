# -*- coding:utf-8 -*- 
'''
Created on 2018/9/10
@author: Hao Chen
'''
import unittest
import aushare.stock.fundamental as fd
import sys
from datetime import datetime

class TestFundamental(unittest.TestCase):

    def setUp(self):
        if sys.version_info[0] < 3:
            raise Exception("Must be using Python 3")
        self.thisyear = datetime.now().year
       
    def tearDown(self):
        pass

    def test_getASXListName(self):
        print(fd.getASXListName('IRE'))
        
    def test_getASXListIndustry(self):
        print(fd.getASXListIndustry())
        
    def test_getCompanyBasicInfo(self):
        code = 'APT'
        print(code)
        print(fd.getCompanyBasicInfo(code))
        
    def test_getRevenueDiff(self):
        for code in ['APT','123']:
            print(code)
            print(fd.getRevenueDiff(code))

        
    def test_getWeeklyPrice(self):
        for code in ['APT','123']:
            print(code)
            print(fd.getWeeklyPrice(code=code,Year=self.thisyear))
            print (fd.getWeeklyPrice(code=code,Year=self.thisyear+2))
    
    def test_getMeanPriceDiffPercentage(self):
        code = ['APT','123']
        startyear = [self.thisyear, self.thisyear+1]
        for code, startyear in zip(code,startyear):
            print(fd.getMeanPriceDiffPercentage(code,startyear,startyear+1))   

    def test_getBalanceSheet(self):
        for code in ['APT','123']:
            print(code)
            print(fd.getBalanceSheet(code))

    def test_getCashflow(self):
        for code in ['APT','123']:
            print(code)
            print(fd.getCashflow(code))


        
if __name__ == "__main__":
    unittest.main()
    
#     suite = unittest.TestSuite()  
#     suite.addTest(Test('test_getRevenueDiff'))  
#     unittest.TextTestRunner(verbosity=2).run(suite)
