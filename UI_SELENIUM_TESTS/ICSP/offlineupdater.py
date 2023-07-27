import unittest, sys, os, time
# from selenium import webdriver
# from selenium.webdriver.common import keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait

class pdf(unittest.TestCase):
    nnp_ip = "https://192.168.3.141"
    md5sum = "caaf31973f72d6545259be0a61c590a1" ## md5sum of ICSPUpdater.exe
    
    def test_a_test(self):
        os.system ('rm /tmp/ICSPUpdater.exe 2> /dev/null')
        os.system('curl -k -X POST --data "username=admin&password=norman" -c /tmp/nnp.cookie '+self.nnp_ip+'/auth')
        os.system('curl -k -o /tmp/ICSPUpdater.exe -b /tmp/nnp.cookie '+self.nnp_ip+'/download/ICSPUpdater.exe')
    
        time.sleep(2)
        if (os.path.isfile("/tmp/ICSPUpdater.exe") == True):
            if str(os.system("md5sum /tmp/ICSPUpdater.exe") == self.md5sum):
                print "Checkpoint 1: [PASSED] File downloaded successfully."
            else:
                print "Checkpoint 1: [FAILED] File not downloaded."
                print self.fail("Case Status: FAILED.")
                return 0
        else:
            print "Checkpoint 1: [FAILED] File not downloaded."
            print self.fail("Case Status: FAILED.")
            return 0
    
        os.system("rm /tmp/ICSPUpdater.exe /tmp/nnp.cookie")
        
if __name__ == '__main__':
    unittest.main()