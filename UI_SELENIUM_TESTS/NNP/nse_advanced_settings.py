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
    
    b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[3]/a').click() ## Clicking on Advanced Settings
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME,"filesize"))
        )
    except:
        print "Checkpoint 4: [FAILED] Advanced Settings page not loaded."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 4: [PASSED] Navigated to Advanced Settings page."
      
class OperationMode(unittest.TestCase):
     
    nnp_ip = "https://192.168.3.241" 
    def setUp(self):
        self.driver=webdriver.Firefox()
        
    def test_A_config_advancesettings(self):
        print "\n>> #### TC1 - Configure Advanced Scanner Engine settings."
        do_login(self)
        b=self.driver
        ########## 
        stop_mal_code = b.find_element_by_name("cifs_behavior_blocking").get_attribute("checked")
        if (stop_mal_code):
            b.find_element_by_name("cifs_behavior_blocking").click()
        else:
            pass
        b.find_element_by_name("cifs_behavior_blocking").click() ## Enabling "Stop malicious code"
        ########### 
        use_cached_objects = b.find_element_by_name("scan_cache").get_attribute("checked")
        if (use_cached_objects):
            b.find_element_by_name("scan_cache").click()
        else:
            pass
        b.find_element_by_name("scan_cache").click() ## Enabling Use cached objects
        ############# 
        block_files = b.find_element_by_name("block_large_files").get_attribute("checked")
        if (block_files):
            b.find_element_by_name("block_large_files").click()
        else:
            pass
        b.find_element_by_name("block_large_files").click() ## Enabling Block large files
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/button').click() ## Save Configuration
        ############## 
        if (b.find_element_by_name("cifs_behavior_blocking").get_attribute("Checked") == "true"):
            print "Checkpoint 5: [PASSED] Stop malicious code check-box enabled successfully."
        else:
            print "Checkpoint 5: [FAILED] Stop malicious code check-box not enabled."
            print self.fail("Test case Failed.")
            return 0
        ##########
        if (b.find_element_by_name("scan_cache").get_attribute("Checked") == "true"):
            print "Checkpoint 6: [PASSED] Use Cached Objects check-box enabled successfully."
        else:
            print "Checkpoint 6: [FAILED] Use Cached Objects check-box not enabled."
            print self.fail("Test case Failed.")
            return 0
        #############  
        if (b.find_element_by_name("block_large_files").get_attribute("Checked") == "true"):
            print "Checkpoint 7: [PASSED] Block large files check-box enabled successfully."
        else:
            print "Checkpoint 7: [FAILED] Block large files check-box not enabled."
            print self.fail("Test case Failed.")
            return 0
        
    def test_B_maximumfilesize(self):
        print "\n>> #### TC2 - Configure Maximum file size"
        do_login(self)
        b=self.driver
        ############################
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[1]').click() ## 512 KiB
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/button').click() ## Save Configuration
        
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[1]').is_selected() == True):
            if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[1]').get_attribute("value") == "512"):
                print "Checkpoint 5:[PASSED] Maximum file size successfully set to 512 KiB."
            else:
                print "Checkpoint 5: [FAILED] Maximum file size not set to 512 KiB."
                print self.fail("Test case Failed.")
                return 0
        else:
            
            print "Checkpoint 5: [FAILED] Maximum file size not set to 512 KiB."
            print self.fail("Test case Failed.")
            return 0
        ######################
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[2]').click() ## 1 MiB
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/button').click() ## Save Configuration
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[2]').is_selected() == True):
            if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[2]').get_attribute("value") == "1024"):
                print "Checkpoint 6:[PASSED] Maximum file size successfully set to 1 MiB."
            else:
                print "Checkpoint 6: [FAILED] Maximum file size not set to 1 MiB."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 6: [FAILED] Maximum file size not set to 1 MiB."
            print self.fail("Test case Failed.")
            return 0
        ######################
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[3]').click() ## 2 MiB
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/button').click() ## Save Configuration
        time.sleep(1)   
        if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[3]').is_selected() == True):
            if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[3]').get_attribute("value") == "2048"):
                print "Checkpoint 7:[PASSED] Maximum file size successfully set to 1 MiB."
            else:
                print "Checkpoint 7: [FAILED] Maximum file size not set to 2 MiB."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 7: [FAILED] Maximum file size not set to 2 MiB."
            print self.fail("Test case Failed.")
            return 0
        ######################
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[4]').click() ## 4 MiB
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/button').click() ## Save Configuration
        time.sleep(1)    
        if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[4]').is_selected() == True):
            if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[4]').get_attribute("value") == "4096"):
                print "Checkpoint 8:[PASSED] Maximum file size successfully set to 4 MiB."
            else:
                print "Checkpoint 8: [FAILED] Maximum file size not set to 4 MiB."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 8: [FAILED] Maximum file size not set to 4 MiB."
            print self.fail("Test case Failed.")
            return 0 
        ######################
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[5]').click() ## 8 MiB
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/button').click() ## Save Configuration
        time.sleep(1)    
        if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[5]').is_selected() == True):
            if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[5]').get_attribute("value") == "8192"):
                print "Checkpoint 9:[PASSED] Maximum file size successfully set to 8 MiB."
            else:
                print "Checkpoint 9: [FAILED] Maximum file size not set to 8 MiB."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 9: [FAILED] Maximum file size not set to 8 MiB."
            print self.fail("Test case Failed.")
            return 0
        ######################
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[6]').click() ## 16 MiB
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/button').click() ## Save Configuration
        time.sleep(1)    
        if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[6]').is_selected() == True):
            if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[6]').get_attribute("value") == "16384"):
                print "Checkpoint 10:[PASSED] Maximum file size successfully set to 16 MiB."
            else:
                print "Checkpoint 10: [FAILED] Maximum file size not set to 16 MiB."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 10: [FAILED] Maximum file size not set to 16 MiB."
            print self.fail("Test case Failed.")
            return 0
        ######################
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[7]').click() ## 32 MiB
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/button').click() ## Save Configuration
        time.sleep(1)    
        if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[7]').is_selected() == True):
            if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[7]').get_attribute("value") == "32768"):
                print "Checkpoint 11:[PASSED] Maximum file size successfully set to 32 MiB."
            else:
                print "Checkpoint 11: [FAILED] Maximum file size not set to 32 MiB."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 11: [FAILED] Maximum file size not set to 32 MiB."
            print self.fail("Test case Failed.")
            return 0
        ######################
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[8]').click() ## 64 MiB
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/button').click() ## Save Configuration
        time.sleep(1)    
        if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[8]').is_selected() == True):
            if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[8]').get_attribute("value") == "65536"):
                print "Checkpoint 12:[PASSED] Maximum file size successfully set to 64 MiB."
            else:
                print "Checkpoint 12: [FAILED] Maximum file size not set to 64 MiB."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 12: [FAILED] Maximum file size not set to 64 MiB."
            print self.fail("Test case Failed.")
            return 0
        ######################
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[9]').click() ## 128 MiB
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/button').click() ## Save Configuration
        time.sleep(1)    
        if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[9]').is_selected() == True):
            if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[9]').get_attribute("value") == "131072"):
                print "Checkpoint 13:[PASSED] Maximum file size successfully set to 128 MiB."
            else:
                print "Checkpoint 13: [FAILED] Maximum file size not set to 128 MiB."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 13: [FAILED] Maximum file size not set to 128 MiB."
            print self.fail("Test case Failed.")
            return 0
        ######################
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[10]').click() ## 256 MiB
        b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/button').click() ## Save Configuration
        time.sleep(1)    
        if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[10]').is_selected() == True):
            if (b.find_element_by_xpath('//*[@id="advanced_scanner_settings"]/div/span[3]/select/option[10]').get_attribute("value") == "262144"):
                print "Checkpoint 14:[PASSED] Maximum file size successfully set to 256 MiB."
            else:
                print "Checkpoint 14: [FAILED] Maximum file size not set to 256 MiB."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 14: [FAILED] Maximum file size not set to 256 MiB."
            print self.fail("Test case Failed.")
            return 0
              
    def tearDown(self):
        do_logout(self)
        self.driver.close()