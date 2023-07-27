import unittest, selenium
from selenium import webdriver

class test(unittest.TestCase):
    
    def setUp(self):
        self.driver=webdriver.Firefox()
        
    def test_a_test(self):
        b=self.driver
        b.get("http://10.138.128.2")
        print b.title
        assert "Malware Analysis Appliance" in b.title
        print "hello"
        
    
    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()