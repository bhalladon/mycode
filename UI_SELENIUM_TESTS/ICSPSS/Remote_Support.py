import unittest, sys, os, time
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from settings import *

def do_logout(self):
    self.driver.get(nnp_ip+'logout')
    #self.driver.find_element_by_id("userbtn").click()
    #self.driver.find_element_by_link_text("Logout").click()

def do_login(self,driver,webuser,webpassword):
    self.driver.get(nnp_ip)
    
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
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "nnp_version_header"))
        )
    except:
        print "Checkpoint 2: [FAILED] User not logged in."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 2: [PASSED] User successfully logs in."
    
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Support"))
        )
    except:
        print "Checkpoint 3: [FAILED] Support Link not found."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 3: [PASSED] Support link found."
    b.find_element_by_link_text("Support").click()
    
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Remote support"))
        )
    except:
        print "Checkpoint 4: [FAILED] Remote Support Link not found."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 4: [PASSED] Remote Support link found."
    b.find_element_by_link_text("Remote support").click()

class remotesupport(unittest.TestCase):
     
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_A_remotesupport(self):
        b=self.driver
        b.delete_all_cookies()
        do_login(self,b,"admin","norman")
        print "\n>> #### TC1 - To verify the remote support functionality (enabled and disabled)."
        
        #################################################################################################
        remote = b.find_element_by_id("switch_remote_support")
        try:
            element = WebDriverWait(b,5).until(EC.visibility_of_element_located((By.ID,"rs_port_info"))
            )
        except:
            print ">> #### Enabling the remote support."
            remote.click()
            try:
                element = WebDriverWait(b,120).until(EC.visibility_of_element_located((By.ID,"rs_port_info"))
                )
            except:
                print "Checkpoint 5: Failed to enable remote support."
                print self.fail("Test case Failed.")
                return 0
            time.sleep(2)
            port_num = b.find_element_by_id("rs_port")
            print "Remote support enabled successfully and the port number to provide Blue Coat Support is: " + port_num.text
            remote.click()
            return 0
        ##################################################################################################    
        print ">> #### Disabling and re-enabling the remote support."
        remote.click()
        time.sleep(4)
        try:
            element = WebDriverWait(b,5).until(EC.visibility_of_element_located((By.ID,"rs_port_info"))
            )
        except:
            remote.click()
            try:
                element = WebDriverWait(b,120).until(EC.visibility_of_element_located((By.ID,"rs_port_info"))
                )
            except:
                print "Checkpoint 5: Failed to enable remote support."
                print self.fail("Test case Failed.")
                return 0
            time.sleep(2)
            port_num = b.find_element_by_id("rs_port")
            print "Remote support enabled successfully and the port number to provide Blue Coat Support is: " + port_num.text
            remote.click()
            return 0
        print "Checkpoint 5: [FAILED] Not able to disable remote support."
        print self.fail("Test case Failed.")
        return 0 
        ##################################################################################################
        
    def tearDown(self):
        do_logout(self)
        self.driver.close()
            
if __name__ == '__main__':
    unittest.main()