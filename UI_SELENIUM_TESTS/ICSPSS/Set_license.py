#!/usr/bin/python

import unittest, pprint, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from settings import *

def do_login(self):
    self.driver.get(nnp_ip)
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
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "nnp_version_header"))
        )
    except:
        print "Checkpoint 2: [FAILED] Page not loaded after successfull login."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 2: [PASSED] User logged in successfully."
    
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "System"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'System' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("System").click()
    
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Software License"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Software License' link not found."
        print self.fail("Test Case Failed.")
        return 0
    
    b.find_element_by_link_text("Software License").click()
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"set_license_key")))
    except:
        print "Checkpoint 3: [FAILED] Software License page not loaded."
        return 0
    print "Checkpoint 3: [PASSED] Navigated to page 'Software License' successfully."

def do_logout(self):
    self.driver.get(nnp_ip+'logout')
    
class set_license(unittest.TestCase):
    
    def setUp(self):
        self.driver=webdriver.Firefox()
        
    def test_A_setlicensekey(self):
        print "\n##### TC1 - Set license key."
        print "\n## Saving the empty license"
        do_login(self)
        b=self.driver
        license_key = b.find_element_by_id("license_key")
        license_key.clear()
        b.find_element_by_id("set_license_key").click() ## save license key
        time.sleep(1)
        if "Invalid" in str(b.find_element_by_id("set_license_key").text):
            print "Checkpoint 4: [PASSED] Empty value not accepted as license key."
        else:
            print "Checkpoint 4: [FAILED] Empty value accepted as license key."
            print self.fail("Case Status: FAILED.")
            
        print "\n## Saving a valid license key"
        license_key.send_keys("cxj4t-dmndc-d2tve-yvs57-2paxi")
        b.find_element_by_id("set_license_key").click() ## save license key
        time.sleep(1)
        if "Key set" in str(b.find_element_by_id("set_license_key").text):
            print "Checkpoint 5: [PASSED] Valid license key accepted successfully."
        else:
            print "Checkpoint 5: [FAILED] Valid license key not accepted."
            print self.fail("Case Status: FAILED.")
            

    def tearDown(self):
        do_logout(self)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
