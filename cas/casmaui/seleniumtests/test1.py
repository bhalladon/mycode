from __init__ import *
from casmaui.__init__ import *
from lib2to3.tests.support import driver

class test_systeminfo(unittest.TestCase):

    def setUp(self):
        print "hello"
        global a1
        a1 = uitest()
           
    
    def test_a_addbaseimage(self):
        a1.login("admin", "admin123")
        a1.navigate_primary("Services")
        print "Checkpoint 3: [Passed] Services page appeared successfully."
        a1.navigate_secondary("Sandboxing")
        print "Checkpoint 4: [Passed] Sandboxing page appeared successfully."
        '''upload base image using url'''
        a1.upload_baseimage_url(baseimage_url, baseimage_key)
        
        print "yes"
        
        
if __name__ == '__main__':
    unittest.main()