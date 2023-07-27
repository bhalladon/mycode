import unittest, sys, os, time
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

def do_login(self,driver,webuser, webpassword):
    self.driver.get('http://192.168.3.241')
    
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
        print "Checkpoint 2: [FAILED] Page not loaded after successful login."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 2: [PASSED] User successfully logs in."
    
class loginpage(unittest.TestCase):
    
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_A_test(self):
        b=self.driver
        do_login(self,b,"admin","norman")
        time.sleep(2)

    def tearDown(self):
        self.driver.close()
        
if __name__ == '__main__':
    unittest.main() 