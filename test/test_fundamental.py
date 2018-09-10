# -*- coding:utf-8 -*- 
'''
Created on 2018/9/10
@author: Hao Chen
'''
import unittest
import aushare.stock.fundamental as fd

class TestFundamental(unittest.TestCase):

    def setUp(self):
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
            print(fd.getWeeklyPrice(code))
            print (fd.getWeeklyPrice(code,self.thisyear+2))
    
    def getMeanPriceDiffPercentage(self):
        code = ['APT','123']
        startyear = [self.thisyear, self.thisyear+1]
        for code, startyear in zip(code,startyear):
            print(fd.getMeanPriceDiffPercentage())           

        
if __name__ == "__main__":
    unittest.main()
    
#     suite = unittest.TestSuite()  
#     suite.addTest(Test('test_getRevenueDiff'))  
#     unittest.TextTestRunner(verbosity=2).run(suite)
