import unittest, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


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
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID, "uptime"))
        )
    except:
        print "Checkpoint 2: [FAILED] Page not loaded after successful login."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 2: [PASSED] User successfully logs in."
    
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Blocking"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Blocking' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Blocking").click()
    
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "HTTP block customization"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'HTTP block customization' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("HTTP block customization").click()
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"block_page")))
    except:
        print "Checkpoint 3: [FAILED] HTTP block customization page not loaded."
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 3: [PASSED] Navigated to 'HTTP block customization' page successfully."

class httpblockcustomization(unittest.TestCase):
    nnp_ip="https://192.168.3.241/"
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_A_malwaredetection(self):
        print "\n>> #### TC1 - Configure block options for malware detection."
        do_login(self)
        b=self.driver
        malware_option = b.find_element_by_xpath('//*[@id="bp_malware_option"]/option[2]') ## Choose Display a page option
        malware_option.click()
          
        ### Verify if Display a page option is selected than Redirect URL text input box should be disabled.
          
        if (b.find_element_by_id("bp_malware_redirect").get_attribute("disabled") == "true"):
            print "Checkpoint 4: [PASSED] Text input box for re-direct URL is disabled when display a page option is selected."
        else:
            print "Checkpoint 4: [FAILED] Text input box for re-direct URL is not disabled when display a page option is selected."
            print self.fail("Test case Failed.")
            return 0
         
        user_def_msg = b.find_element_by_id("bp_malware_message")
        user_def_msg.clear()
        user_def_msg.send_keys("Please contact Mr. Bhalla")
          
        ###save config
        b.find_element_by_id("customize_block_pages_save").click()
        time.sleep(2)
          
        if (malware_option.text == "Display a page"):
            print "Checkpoint 5: [PASSED] Malware block option successfully saved as 'Display a page'."
        else:
            print "Checkpoint 5: [FAILED] Malware block option not saved as 'Display a page'."
            print self.fail("Test case Failed.")
            return 0
         
        if (user_def_msg.get_attribute("value") == "Please contact Mr. Bhalla"):
            print "Checkpoint 6: [PASSED] User defined message saved as expected."
        else:
            print "Checkpoint 6: [FAILED] Expected user defined message not saved."
            print self.fail("Test case Failed.")
            return 0
         
        #### Choose malware block option as Redirect to another URL
        malware_option = b.find_element_by_xpath('//*[@id="bp_malware_option"]/option[1]')
        malware_option.click()
         
        redirect_url = b.find_element_by_id("bp_malware_redirect")
        redirect_url.clear()
        redirect_url.send_keys("www.google.co.in")
         
        #### Verify user defined message is disabled.
        if (user_def_msg.is_enabled() == False):
            print "Checkpoint 7: [PASSED] User defined message text input box disabled when redirect to another URL is selected."
        else:
            print "Checkpoint 7: [FAILED] User defined message text input box not disabled when redirect to another URL is selected."
            print self.fail("Test case Failed.")
            return 0
         
        ### save config
        b.find_element_by_id("customize_block_pages_save").click()
        time.sleep(2)
         
        #### Verify config
        if (malware_option.text == "Redirect to another URL"):
            print "Checkpoint 8: [PASSED] Malware block option successfully saved as 'Redirect to another URL'."
        else:
            print "Checkpoint 8: [FAILED] Malware block option not saved as 'Display a page'."
            print self.fail("Test case Failed.")
            return 0
         
        if (redirect_url.get_attribute("value") == "www.google.co.in"):
            print "Checkpoint 9: [PASSED] Redirect URL saved with expected value."
        else:
            print "Checkpoint 9: [FAILED] Redirect URL not saved with expected value."
            print self.fail("Test case Failed.")
            return 0

    def test_B_blocklist(self):
        print "\n>> #### TC2 - Configure block options for block list."
        do_login(self)
        b=self.driver
        blocklist = b.find_element_by_xpath('//*[@id="bp_list_option"]/option[2]') ## Choose Display a page option
        blocklist.click()
         
        ### Verify if Display a page option is selected than Redirect URL text input box should be disabled.
         
        if (b.find_element_by_id("bp_list_redirect").get_attribute("disabled") == "true"):
            print "Checkpoint 4: [PASSED] Text input box for re-direct URL is disabled when display a page option is selected."
        else:
            print "Checkpoint 4: [FAILED] Text input box for re-direct URL is not disabled when display a page option is selected."
            print self.fail("Test case Failed.")
            return 0
        
        user_def_msg = b.find_element_by_id("bp_list_message")
        user_def_msg.clear()
        user_def_msg.send_keys("Please contact Mr. Bhalla")
         
        ###save config
        b.find_element_by_id("customize_block_pages_save").click()
        time.sleep(2)
         
        if (blocklist.text == "Display a page"):
            print "Checkpoint 5: [PASSED] Block option for block list successfully saved as 'Display a page'."
        else:
            print "Checkpoint 5: [FAILED] Block option for block list not saved as 'Display a page'."
            print self.fail("Test case Failed.")
            return 0
        
        if (user_def_msg.get_attribute("value") == "Please contact Mr. Bhalla"):
            print "Checkpoint 6: [PASSED] User defined message saved as expected."
        else:
            print "Checkpoint 6: [FAILED] Expected user defined message not saved."
            print self.fail("Test case Failed.")
            return 0
        
        #### Choose malware block option as Redirect to another URL
        blocklist = b.find_element_by_xpath('//*[@id="bp_list_option"]/option[1]')
        blocklist.click()
        
        redirect_url = b.find_element_by_id("bp_list_redirect")
        redirect_url.clear()
        redirect_url.send_keys("www.google.co.in")
        
        #### Verify user defined message is disabled.
        if (user_def_msg.is_enabled() == False):
            print "Checkpoint 7: [PASSED] User defined message text input box disabled when redirect to another URL is selected."
        else:
            print "Checkpoint 7: [FAILED] User defined message text input box not disabled when redirect to another URL is selected."
            print self.fail("Test case Failed.")
            return 0
        
        ### save config
        b.find_element_by_id("customize_block_pages_save").click()
        time.sleep(2)
        
        #### Verify config
        if (blocklist.text == "Redirect to another URL"):
            print "Checkpoint 8: [PASSED] Block option for block list successfully saved as 'Redirect to another URL'."
        else:
            print "Checkpoint 8: [FAILED] Block option for block list not saved as 'Display a page'."
            print self.fail("Test case Failed.")
            return 0
        
        if (redirect_url.get_attribute("value") == "www.google.co.in"):
            print "Checkpoint 9: [PASSED] Redirect URL saved with expected value."
        else:
            print "Checkpoint 9: [FAILED] Redirect URL not saved with expected value."
            print self.fail("Test case Failed.")
            return 0
        
    def test_C_filesize(self):
        print "\n>> #### TC3 - Configure block options for exceeded file size."
        do_login(self)
        b=self.driver
        blocklist = b.find_element_by_xpath('//*[@id="bp_size_option"]/option[2]') ## Choose Display a page option
        blocklist.click()
         
        ### Verify if Display a page option is selected than Redirect URL text input box should be disabled.
         
        if (b.find_element_by_id("bp_size_redirect").get_attribute("disabled") == "true"):
            print "Checkpoint 4: [PASSED] Text input box for re-direct URL is disabled when display a page option is selected."
        else:
            print "Checkpoint 4: [FAILED] Text input box for re-direct URL is not disabled when display a page option is selected."
            print self.fail("Test case Failed.")
            return 0
        
        user_def_msg = b.find_element_by_id("bp_size_message")
        user_def_msg.clear()
        user_def_msg.send_keys("Please contact Mr. Bhalla")
         
        ###save config
        b.find_element_by_id("customize_block_pages_save").click()
        time.sleep(2)
         
        if (blocklist.text == "Display a page"):
            print "Checkpoint 5: [PASSED] Block option for exceeded file size successfully saved as 'Display a page'."
        else:
            print "Checkpoint 5: [FAILED] Block option for exceeded file size not saved as 'Display a page'."
            print self.fail("Test case Failed.")
            return 0
        
        if (user_def_msg.get_attribute("value") == "Please contact Mr. Bhalla"):
            print "Checkpoint 6: [PASSED] User defined message saved as expected."
        else:
            print "Checkpoint 6: [FAILED] Expected user defined message not saved."
            print self.fail("Test case Failed.")
            return 0
        
        #### Choose malware block option as Redirect to another URL
        blocklist = b.find_element_by_xpath('//*[@id="bp_size_option"]/option[1]')
        blocklist.click()
        
        redirect_url = b.find_element_by_id("bp_size_redirect")
        redirect_url.clear()
        redirect_url.send_keys("www.google.co.in")
        
        #### Verify user defined message is disabled.
        if (user_def_msg.is_enabled() == False):
            print "Checkpoint 7: [PASSED] User defined message text input box disabled when redirect to another URL is selected."
        else:
            print "Checkpoint 7: [FAILED] User defined message text input box not disabled when redirect to another URL is selected."
            print self.fail("Test case Failed.")
            return 0
        
        ### save config
        b.find_element_by_id("customize_block_pages_save").click()
        time.sleep(2)
        
        #### Verify config
        if (blocklist.text == "Redirect to another URL"):
            print "Checkpoint 8: [PASSED] Block option for exceeded file size successfully saved as 'Redirect to another URL'."
        else:
            print "Checkpoint 8: [FAILED] Block option for exceeded file size not saved as 'Display a page'."
            print self.fail("Test case Failed.")
            return 0
        
        if (redirect_url.get_attribute("value") == "www.google.co.in"):
            print "Checkpoint 9: [PASSED] Redirect URL saved with expected value."
        else:
            print "Checkpoint 9: [FAILED] Redirect URL not saved with expected value."
            print self.fail("Test case Failed.")
            return 0
        
    def tearDown(self):
        do_logout(self)
        self.driver.close()
        