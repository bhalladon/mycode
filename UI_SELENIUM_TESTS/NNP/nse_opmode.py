import unittest,time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def do_logout(self):
    self.driver.get(self.nnp_ip+'logout')

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
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Network"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Network' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Network").click() ## Click on "Network"
    
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Scanner Engine"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Scanner Engine' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Scanner Engine").click() ## CLick on "Network Threat Discovery"
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
        )
    except:
        print "Checkpoint 3: [FAILED] Scanner Engine page not loaded."
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 3: [PASSED] Navigated to 'Scanner Engine' page successfully."
    b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[1]/a').click()
    
    
class OperationMode(unittest.TestCase):
    nnp_ip="https://192.168.3.241/"
    
    def setUp(self):
        self.driver=webdriver.Firefox()
     
    def test_A_opmode(self):
        print "\n>> #### TC1 - To set the different operation modes."
        do_login(self)
        b=self.driver
        
        log_only = b.find_element_by_xpath('//*[@id="operation_mode"]/div/div/div/span[1]/input')
        if (log_only.is_selected() == "True"):
            pass
        else:
            log_only.click()
        b.find_element_by_xpath('//*[@id="operation_mode"]/div/div/button').click() ## Save Configuration
        
        if (log_only.is_selected() == True):
            print "Checkpoint 4: [PASSED] Operation mode successfully set to Log Only."
        else:
            print "Checkpoint 4: [FAILED] Operation mode not set to Log Only."
            print self.fail("Test Case Failed.")
            return 0
        
        ################################################
        bypass = b.find_element_by_xpath('//*[@id="operation_mode"]/div/div/div/span[2]/input')
        bypass.click()
        b.find_element_by_xpath('//*[@id="operation_mode"]/div/div/button').click() ## Save Configuration
        
        if (bypass.is_selected() == True):
            print "Checkpoint 5: [PASSED] Operation mode successfully set to Bypass."
        else:
            print "Checkpoint 5: [FAILED] Operation mode not set to Bypass."
            print self.fail("Test Case Failed.")
            return 0
                
        ################################################
        scan = b.find_element_by_xpath('//*[@id="operation_mode"]/div/div/div/span[4]/input')
        scan.click()
        b.find_element_by_xpath('//*[@id="operation_mode"]/div/div/button').click() ## Save Configuration
        
        if (scan.is_selected() == True):
            print "Checkpoint 6: [PASSED] Operation mode successfully set to Scan."
        else:
            print "Checkpoint 6: [FAILED] Operation mode not set to Scan."
            print self.fail("Test Case Failed.")
            return 0
        
        
#         self.goto_fragment("Network", "Traffic Scanning")
#         
#         print "\n->> Setting operation mode to Log Only"
#         self.find_element_by_sizzle("#operation_mode input[value='3']").click()
#         self.find_element_by_sizzle("#operation_mode .save_configuration").click()
#         print "->> Operation mode successfully saved to Log Only"
#         time.sleep(2)
#         
#         print "\n->> Setting operation mode to BYPASS"
#         self.find_element_by_sizzle("#operation_mode input[value='0']").click()
#         self.find_element_by_sizzle("#operation_mode .save_configuration").click()
#         print "->> Operation mode successfully saved to BYPASS"
#         time.sleep(2)
#         
#         print "\n->> Setting operation mode to SCAN"
#         self.find_element_by_sizzle("#operation_mode input[value='2']").click()
#         self.find_element_by_sizzle("#operation_mode .save_configuration").click()
#         print "->> Operation mode successfully saved to SCAN"
#         
#         #time.sleep(4)
#         #self.find_element_by_sizzle("#operation_mode input[value='1']").click()
#         #self.find_element_by_sizzle("#operation_mode .save_configuration").click()
#         time.sleep(2)

    def tearDown(self):
        do_logout(self)
        self.driver.close()
