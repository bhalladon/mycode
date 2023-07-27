import unittest, sys, os, time
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.remote.webelement import WebElement

def do_logout(self):
    self.driver.get(self.nnp_ip+'logout')
    #self.driver.find_element_by_id("userbtn").click()
    #self.driver.find_element_by_link_text("Logout").click()

def do_login(self,driver,webuser,webpassword):
    self.driver.get(self.nnp_ip)
    
    #self.driver.maximize_window()
    b=self.driver
    b.set_window_size(1280,900)
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
    username.send_keys(webuser)
    password = b.find_element_by_name("password")
    password.clear()
    password.send_keys(webpassword)
    b.find_element_by_class_name("btn-primary").click()
     
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "uptime"))
        )
    except:
        print "Checkpoint 2: [FAILED] User not logged in."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 2: [PASSED] User successfully logs in."
 
class api(unittest.TestCase):
    
    nnp_ip = "https://192.168.3.241/"
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_a_apidocs(self):
        print "\n##### To verify that API Docs link opens in new window."
        b=self.driver
        do_login(self,b,"admin","norman")
        time.sleep(1)
        #b.find_element_by_link_text("API Docs").click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located,((By.LINK_TEXT,"API Docs"))
            )
        except:
            print "Checkpoint 3: [FAILED] API Docs link not found."
            print self.fail("Case Status: FAILED")
            return 0
        print "Checkpoint 3: [PASSED] API Docs link found."
        api_link = b.find_element_by_link_text("API Docs").get_attribute("target")
        print api_link
#         if (api_link == "_blank"):
#             print "Checkpoint 4: [PASSED] API Docs opens up in new page."
#         else:
#             print "Checkpoint 4: [FAILED] API Docs opens up in same window."
#             print self.fail("Case Status: FAILED.")
#             return 0
        
    def tearDown(self):
        do_logout(self)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()