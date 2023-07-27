import unittest, sys, os, time
from settings import *

class pdf(unittest.TestCase):
    
    #nnp_ip = "https://192.168.3.242/"
    md5sum = "84e586efdf1236feb3fa6fe63e305c00" ## md5sum of admin guide
    
    def test_a_test(self):
    
        os.system ('rm /tmp/ICSP_AdminGuide.pdf 2> /dev/null')
        os.system('curl -k -X POST --data "username=admin&password=norman" -c /tmp/nnp.cookie '+nnp_ip+'auth')
        os.system('curl -k -o /tmp/ICSP_AdminGuide.pdf -b /tmp/nnp.cookie '+nnp_ip+'docs/ICSP_AdminGuide.pdf')
    
        time.sleep(2)
        if os.path.isfile("/tmp/ICSP_AdminGuide.pdf") == True:
            if str(os.system("md5sum /tmp/ICSP_AdminGuide.pdf") == self.md5sum):
                print "Checkpoint 1: [PASSED] Admin guide downloaded successfully."
            else:
                print "Checkpoint 1: [FAILED] Admin guide not downloaded."
                print self.fail("Case Status: FAILED.")
                return 0
        else:
            print "Checkpoint 1: [FAILED] Admin guide not downloaded."
            print self.fail("Case Status: FAILED.")
            return 0
    
        os.system("rm /tmp/ICSP_AdminGuide.pdf /tmp/nnp.cookie")
 
if __name__ == '__main__':
    unittest.main()