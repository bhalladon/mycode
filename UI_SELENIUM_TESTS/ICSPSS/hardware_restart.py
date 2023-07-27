import unittest, pprint, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from settings import *

def do_logout(self):
    self.driver.get(nnp_ip+'logout')

def do_login(self):
    self.driver.get(nnp_ip)
    
    self.driver.maximize_window()
    b=self.driver
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.NAME, "username"))
        )
    except:
        print "Checkpoint 1: [FAILED] Unable to open the login page. Field 'User Name' not found."
        print self.fail("Test case Failed.")
        return 0
    print "Checkpoint 1: [PASSED] Login page appeared successfully."
    username = b.find_element_by_name("username")
    username.clear()
    username.send_keys("admin")
    password = b.find_element_by_name("password")
    password.clear()
    password.send_keys("norman")
    print "test1"
    b.find_element_by_class_name("btn-primary").click()
    print "test2"
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "scada_current_timespan"))
        )
    except:
        print "Checkpoint 2: [FAILED] Page not loaded after successfull login."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 2: [PASSED] User successfully logs in."
    b.find_element_by_link_text("System").click()
    b.find_element_by_link_text("Hardware Restart").click()

    

class hardwarerestart(unittest.TestCase):
    
    def setUp(self):
        self.driver=webdriver.Firefox()
        
    def test_a_hardwarerestart(self):
        print "\n##### TC1 - Hardware restart"
        do_login(self)
        b=self.driver
        time.sleep(2)
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME,"confirm"))
            )
        except:
            print "Checkpoint 3: [FAILED] Confirmation pop-up to do a hardware restart not displayed."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 3: [PASSED] Confirmation pop-up to do a hardware restart displayed successfully."
        print '### Clicking on "No" button.'
        b.find_element_by_name("cancel").click()
        try:
            element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "scada_current_timespan"))
            )
        except:
            print 'Checkpoint 4: [FAILED] On clicking "No" button it does not return to previous screen.'
            print self.fail("Case Status: FAILED.")
            return 0
        print 'Checkpoint 4: [PASSED] On clicking "No" button screen returns to previous screen successfully.'
        print '\n### Restarting the hardware..'
        time.sleep(2)
        b.find_element_by_link_text("System").click()
        b.find_element_by_link_text("Hardware Restart").click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME,"confirm"))
            )
        except:
            print "Checkpoint 5: [FAILED] Confirmation pop-up to do a hardware restart not displayed."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 5: [PASSED] Confirmation pop-up to do a hardware restart displayed successfully."
        time.sleep(2)
        b.find_element_by_name("confirm").click()
        try:
            element = WebDriverWait(b,20).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="connection_lost"]/div[2]/div[1]/p[1]'))
            )
        except:
            print "Checkpoint 6: [FAILED] Alert message after a hardware reboot not displayed."
            print self.fail("Case Status: FAILED")
            return 0
        print "Checkpoint 6: [PASSED] Alert message displayed successfully after initiating a hardware reboot."
        #b.delete_cookie("NNP_SESSION")
        print "Waiting for one minute to get the system restarted."
        for i in xrange(60,0,-1):
            time.sleep(1)
            sys.stdout.write(str(i)+' ')
            sys.stdout.flush()
        
        print "hello"   
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID, "scada_current_timespan"))
            )
        except:
            print "Checkpoint 7: [FAILED] System not come back after a hardware restart."
            print self.fail("Case Status: FAILED")
            return 0 
        print "Checkpoint 7: [PASSED] UI loaded successfully after a hardware reboot."
        
    def tearDown(self):
        do_logout(self)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
