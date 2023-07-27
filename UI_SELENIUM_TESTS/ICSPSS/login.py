import unittest, pprint, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from settings import *
#from common_functions_report import reporting_head
#from common_functions_report import reporting
#from common_functions_report import report_initialization
#from common_functions_report import set_value

def do_logout(self):
    self.driver.get(nnp_ip+'logout')
    #self.driver.find_element_by_id("userbtn").click()
    #self.driver.find_element_by_link_text("Logout").click()

def do_login(self):
    self.driver.get(nnp_ip)
    b=self.driver
    b.set_window_size(1280, 900)
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.NAME, "username"))
        )
    except:
        #reporting(self,b,"Checkpoint 1: [FAILED] Unable to open the login page. Field 'User Name' not found.")
        print "Checkpoint 1: [FAILED] Unable to open the login page. Field 'User Name' not found."
        print self.fail("Test case Failed.")
        #return 0
    #reporting(self,b,"Checkpoint 1: [PASSED] Login page appeared successfully.")
    print "Checkpoint 1: [PASSED] Login page appeared successfully."
    username = b.find_element_by_name("username")
    username.clear()
    username.send_keys("admin")
    password = b.find_element_by_name("password")
    password.clear()
    password.send_keys("norman")
    b.find_element_by_class_name("btn-primary").click()
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "nnp_version_header"))
        )
    except:
        #reporting(self,b,"Checkpoint 2: [FAILED] Page not loaded after successful login.")
        #print self.fail("Test Case Failed.")")
        print "Checkpoint 2: [FAILED] Page not loaded after successful login."
        print self.fail("Test Case Failed.")
        #return 0
    #reporting(self,b,"Checkpoint 2: [PASSED] User successfully logs in.")
    print "Checkpoint 2: [PASSED] User successfully logs in."
    
class login(unittest.TestCase):
    
    #nnp_ip="https://192.168.3.240/"
    #app_url="https://192.168.3.240/"
    #html_report = "all" #disable,failed,
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_A_login(self):
        #report_initialization(self)
        #set_value("html_report",self.html_report)
        #reporting_head("TC1 - To verify that user can login or not")
        print "\n##### TC1 - To verify that user can login or not."
        b=self.driver
        do_login(self)
        time.sleep(1)

    
    def tearDown(self):
        do_logout(self)
        b=self.driver
        try:
            element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.NAME, "username"))
            )
        except:
            #reporting(self,b,"Checkpoint 3: [FAILED] failed to logged out successfully.")
            print "Checkpoint 3: [FAILED] failed to logged out successfully."
            print self.fail("Test case Failed.")
            #return 0
        #reporting(self,b,"Checkpoint 3: [PASSED] Logged out successfully.")
        print "Checkpoint 3: [PASSED] Logged out successfully."
        b.close()
      


if __name__ == '__main__':
    unittest.main()