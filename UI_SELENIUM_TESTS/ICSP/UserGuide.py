import unittest, sys, os, time
# from selenium import webdriver
# from selenium.webdriver.common import keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait

class pdf(unittest.TestCase):
    nnp_ip = "https://192.168.3.242/"
    def test_a_test(self):
        os.system ('rm ICSPUpdater.exe 2> /dev/null')
        os.system('curl -k -X POST --data "username=admin&password=norman" -c nnp.cookie '+self.nnp_ip+'auth')
        os.system('curl -k -O -b nnp.cookie '+self.nnp_ip+'docs/ICSP_UserGuide.pdf')
    
        time.sleep(2)
        if os.path.isfile("ICSP_UserGuide.pdf") == True:
            if str(os.system("md5sum ICSP_UserGuide.pdf") == "ed56d2c958f1599075d6ca2437ae3c98"):
                print "Checkpoint 1: [PASSED] User guide downloaded successfully."
            else:
                print "Checkpoint 1: [FAILED] User guide not downloaded."
                print self.fail("Case Status: FAILED.")
                return 0
    
        os.system("rm ICSP_UserGuide.pdf nnp.cookie")
 
if __name__ == '__main__':
    unittest.main()