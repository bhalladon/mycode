import unittest, pprint, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def do_logout(self):
    self.driver.get(self.nnp_ip+'logout')
    #self.driver.find_element_by_id("userbtn").click()
    #self.driver.find_element_by_link_text("Logout").click()

def do_login(self):
    self.driver.get(self.nnp_ip)
    
    #self.driver.maximize_window()
    b=self.driver
    b.set_window_size(1280, 900)
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
    b.find_element_by_class_name("btn-primary").click()
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "uptime"))
        )
    except:
        print "Checkpoint 2: [FAILED] Page not loaded after successful login."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 2: [PASSED] User successfully logs in."
    
class login(unittest.TestCase):
    
    nnp_ip="https://192.168.3.141/"
    
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_A_login(self):
        print "\n##### TC1 - To verify that user can login or not."
        b=self.driver
        do_login(self)
        time.sleep(1)
        print "\n### Logging out from the web console."
#         do_logout(self)

    
    def tearDown(self):
        do_logout(self)
        b=self.driver
        try:
            element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.NAME, "username"))
            )
        except:
            print "Checkpoint 3: [FAILED] failed to logged out successfully."
            print self.fail("Test case Failed.")
            return 0
        print "Checkpoint 3: [PASSED] Logged out successfully."
        self.driver.close()

if __name__ == '__main__':
    unittest.main()