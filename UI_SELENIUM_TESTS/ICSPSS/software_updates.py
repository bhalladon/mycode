import unittest, pprint, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


def do_logout(self):
    self.driver.get(self.nnp_ip+'logout')

def do_login(self):
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
    print "Checkpoint 2: [PASSED] User successfully logs in."
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "System"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'System' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("System").click()
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Software Updates"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Software Updates' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Software Updates").click()
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"update_configuration")))
    except:
        print "Checkpoint 3: [FAILED] Software updates page not loaded."
        return 0
    print 'Checkpoint 3: [PASSED] Navigated to "Software Updates" page successfully.'
    

class software_updates(unittest.TestCase):
    nnp_ip = "https://192.168.3.242/"
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_A_enable_critical_def_updates(self):
 
        print "\n##### TC1 - To enable critical and definition updates"
        do_login(self)
        b=self.driver
        print "\n### First we need to check whether USB updates are enabled or not. If enabled then we should disable it."
        usb_update = b.find_element_by_id("usb_auto_update")
        if (usb_update.is_selected() == True):
            print "\nCheckpoint 4: USB updates are enabled."
            print "Disabling USB updates."
            usb_update.click()
            b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
            time.sleep(1)
            if (usb_update.is_selected() == True):
                print "Checkpoint 5: [FAILED] Failed to disable USB updates."
                print self.fail("Case Status: FAILED.")
                return 0
            else:
                print "Checkpoint 5: [PASSED] USB updates disabled successfully."
        else:
            print "\nCheckpoint 4: USB updates are disabled."
        time.sleep(1)
        print "\n### Enabling critical updates"
        critical_updates = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[1]/input')
        if (critical_updates.is_selected() == True):
            print "\nCritical updates are already enabled."
            critical_updates.click()
        critical_updates.click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
        if (critical_updates.is_selected() == True):
            print "Checkpoint 5: [PASSED] Critical updates gets enabled successfully."
        else:
            print "Checkpoint 5: [FAILED] Failed to enable critical updates."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        print "\n### Enabling definition updates."      
        definition_updates = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[2]/input')
        if (definition_updates.is_selected() == True):
            print "\nDefinition updates are already enabled."
            definition_updates.click()
        definition_updates.click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
        if (definition_updates.is_selected() == True):
            print "Checkpoint 6: [PASSED] definition updates gets enabled successfully."
        else:
            print "Checkpoint 6: [FAILED] Failed to enable definition updates."
            print self.fail("Case Status: FAILED.")
            return 0    
        
    def test_b_set_updatefrequency(self):
        print "\n\n##### TC2 - Set update frequency."
        do_login(self)
        b=self.driver
        print "\n### Setting update frequency:"
         
        ## Set to 15
        update_freq = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[4]/select/option[1]').click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
        update_freq = b.find_element_by_name("filesize").get_attribute("value")
        if (update_freq == "15"):
            print 'Checkpoint 4: [PASSED] Update frequency successfully set as "15 minutes".'
        else:
            print 'Checkpoint 4: [FAILED] Failed to set update frequency as "15 minutes".'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
         
        ## Set to 30
        update_freq = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[4]/select/option[2]').click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
        update_freq = b.find_element_by_name("filesize").get_attribute("value")
        if (update_freq == "30"):
            print 'Checkpoint 5: [PASSED] Update frequency successfully set as "30 minutes".'
        else:
            print 'Checkpoint 5: [FAILED] Failed to set update frequency as "30 minutes".'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1) 
        ## Set to 60
        update_freq = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[4]/select/option[3]').click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
        update_freq = b.find_element_by_name("filesize").get_attribute("value")
        if (update_freq == "60"):
            print 'Checkpoint 6: [PASSED] Update frequency successfully set as "1 hour".'
        else:
            print 'Checkpoint 6: [FAILED] Failed to set update frequency as "1 hour".'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        ## Set to 120
        update_freq = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[4]/select/option[4]').click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
        update_freq = b.find_element_by_name("filesize").get_attribute("value")
        if (update_freq == "120"):
            print 'Checkpoint 7: [PASSED] Update frequency successfully set as "2 hours".'
        else:
            print 'Checkpoint 7: [FAILED] Failed to set update frequency as "2 hours".'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        ## Set to 240
        update_freq = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[4]/select/option[5]').click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
        update_freq = b.find_element_by_name("filesize").get_attribute("value")
        if (update_freq == "240"):
            print 'Checkpoint 8: [PASSED] Update frequency successfully set as "4 hours".'
        else:
            print 'Checkpoint 8: [FAILED] Failed to set update frequency as "4 hours".'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1) 
        ## Set to 480
        update_freq = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[4]/select/option[6]').click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
        update_freq = b.find_element_by_name("filesize").get_attribute("value")
        if (update_freq == "480"):
            print 'Checkpoint 9: [PASSED] Update frequency successfully set as "8 hours".'
        else:
            print 'Checkpoint 9: [FAILED] Failed to set update frequency as "8 hours".'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1) 
        ## Set to 720
        update_freq = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[4]/select/option[7]').click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
        update_freq = b.find_element_by_name("filesize").get_attribute("value")
        if (update_freq == "720"):
            print 'Checkpoint 10: [PASSED] Update frequency successfully set as "12 hours".'
        else:
            print 'Checkpoint 10: [FAILED] Failed to set update frequency as "12 hours".'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        ## Set to 1440
        update_freq = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[4]/select/option[8]').click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
        update_freq = b.find_element_by_name("filesize").get_attribute("value")
        if (update_freq == "1440"):
            print 'Checkpoint 11: [PASSED] Update frequency successfully set as "1 day".'
        else:
            print 'Checkpoint 11: [FAILED] Failed to set update frequency as "1 day".'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1) 
        ## Set to 2880
        update_freq = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[4]/select/option[9]').click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click()
        update_freq = b.find_element_by_name("filesize").get_attribute("value")
        if (update_freq == "2880"):
            print 'Checkpoint 12: [PASSED] Update frequency successfully set as "2 days".'
        else:
            print 'Checkpoint 12: [FAILED] Failed to set update frequency as "2 days".'
            print self.fail("Case Status: FAILED.")
            return 0

    def test_c_enable_usbupdates(self):
        print "\n##### TC3 - Enable USB Updates"
        do_login(self)
        b=self.driver
        usb_update = b.find_element_by_id("usb_auto_update")
        print "Enabling USB update"
        if (usb_update.is_selected() == True):
            usb_update.click()
        usb_update.click()
        time.sleep(1)
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME,"confirm"))
            )
        except:
            print "Checkpoint 4: [FAILED] Confirmation pop-up window not displayed."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 4: [PASSED] Confirmation pop-up window displayed successfully."
        time.sleep(1)
        b.find_element_by_name("confirm").click()
        time.sleep(1)
        if (usb_update.is_selected() == True):
            print "Checkpoint 5: [PASSED] USB updates enabled successfully."
        else:
            print "Checkpoint 5: [FAILED] Failed to enable USB updates."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        print "\n\n#### Now verify critical, definition updates and update frequency should be in disabled state."
        critical_updates = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[1]/input')
        if (critical_updates.is_enabled() == True):
            print "Checkpoint 6: [FAILED] After enabling USB updates, critical updates didn't get disabled."
        else:
            print "Checkpoint 6: [PASSED] Critical updates disabled successfully after enabling USB updates."
         
        definition_updates = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[2]/input')
        if (definition_updates.is_enabled() == True):
            print "Checkpoint 7: [FAILED] After enabling USB updates, definition updates didn't get disabled."
        else:
            print "Checkpoint 7: [PASSED] Definition updates disabled successfully after enabling USB updates."
         
        update_freq = b.find_element_by_name("filesize")
        if(update_freq.is_enabled() == True):
            print "Checkpoint 8: [FAILED] After enabling USB updates, frequency updates drop down list didn't get disabled."
        else:
            print "Checkpoint 8: [PASSED] Update frequency drop down list disabled successfully after enabling USB updates."
        
    def test_d_enableproxy(self):
        print "\n##### TC4 -  Enable proxy usage."
        do_login(self)
        b=self.driver
        print "\n### First we will verify when proxy usage is not enabled, then all other proxy options should be in disable state."
        use_proxy_server = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[5]/input')
        if (use_proxy_server.is_selected() == True):
            use_proxy_server.click()
        time.sleep(1)
        proxy_address = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[6]/input')
        if (proxy_address.is_enabled() == True):
            print "Checkpoint 4: [FAILED] Proxy address is editable when proxy server is not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print "Checkpoint 4: [PASSED] Proxy address is not editable when proxy server is not enabled."
        time.sleep(1)
        
        proxy_port = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[7]/input')
        if (proxy_port.is_enabled() == True):
            print "Checkpoint 5: [FAILED] Proxy port input box is editable when proxy server is not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print "Checkpoint 5: [PASSED] Proxy port is not editable when proxy server is not enabled."
        time.sleep(1)
        
        proxy_authentication = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[8]/input')
        if (proxy_authentication.is_enabled() == True):
            print "Checkpoint 6: [FAILED] Proxy authentication is editable when proxy server is not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print "Checkpoint 6: [PASSED] Proxy authentication is not editable when proxy server is not enabled."
        time.sleep(1)
        
        proxy_username = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[9]/input')
        if (proxy_username.is_enabled() == True):
            print "Checkpoint 7: [FAILED] Proxy username is editable when proxy server is not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print "Checkpoint 7: [PASSED] Proxy username is not editable when proxy server is not enabled."
        time.sleep(1)
        
        proxy_password = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[10]/input')
        if (proxy_password.is_enabled() == True):
            print "Checkpoint 8: [FAILED] Proxy password is editable when proxy server is not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print "Checkpoint 8: [PASSED] Proxy  password is not editable when proxy server is not enabled."
        time.sleep(1)
        
        windows_nt_domainname = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[11]/input')
        if (windows_nt_domainname.is_enabled() == True):
            print "Checkpoint 9: [FAILED] Proxy Windows NT Domain name is editable when proxy server is not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print "Checkpoint 9: [PASSED] Proxy Windows NT Domain name is not editable when proxy server is not enabled."
        time.sleep(1)
        
        ####################################################################################
        print "\n\n### Now verify when proxy server checkbox is selected, then all other proxy options becomes editable."
        #use_proxy_server = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[5]/input')
        use_proxy_server.click()
        if (use_proxy_server.is_selected() == True):
            print "Checkpoint 10: [PASSED] Proxy server check box is selected/enabled."
        else:
            print "Checkpoint 10: [FAILED] Proxy server check-box didn't get enabled."
            self.fail("Case Status: FAILED")
            return 0
        time.sleep(1)
        
        #proxy_address = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[6]/input')
        if (proxy_address.is_enabled() == True):
            print "Checkpoint 11: [PASSED] Proxy address is editable when proxy server is enabled."
        else:
            print "Checkpoint 11: [FAILED] Proxy address is not editable when proxy server is enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        #proxy_port = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[7]/input')
        if (proxy_port.is_enabled() == True):
            print "Checkpoint 12: [PASSED] Proxy port input box is editable when proxy server is enabled."
        else:
            print "Checkpoint 12: [FAILED] Proxy port is not editable when proxy server is enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        #proxy_authentication = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[8]/input')
        if (proxy_authentication.is_enabled() == True):
            print "Checkpoint 13: [PASSED] Proxy authentication is editable when proxy server is enabled."
        else:
            print "Checkpoint 13: [FAILED] Proxy authentication is not editable when proxy server is enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        #proxy_username = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[9]/input')
        if (proxy_username.is_enabled() == True):
            print "Checkpoint 14: [PASSED] Proxy username is editable when proxy server is enabled."
        else:
            print "Checkpoint 14: [FAILED] Proxy username is not editable when proxy server is enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        #proxy_password = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[10]/input')
        if (proxy_password.is_enabled() == True):
            print "Checkpoint 15: [PASSED] Proxy password is editable when proxy server is enabled."
        else:
            print "Checkpoint 15: [FAILED] Proxy  password is not editable when proxy server is enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        #windows_nt_domainname = b.find_element_by_xpath('//*[@id="update_configuration"]/div/span[11]/input')
        if (windows_nt_domainname.is_enabled() == True):
            print "Checkpoint 16: [PASSED] Proxy Windows NT Domain name is editable when proxy server is enabled."
        else:
            print "Checkpoint 16: [FAILED] Proxy Windows NT Domain name is not editable when proxy server is enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        print "\n\n#### Now enable proxy server and configure other proxy fields as well."
        proxy_address.clear()
        proxy_address.send_keys("192.168.4.67")
        if (proxy_authentication.is_selected() == True):
            proxy_authentication.click()
        proxy_authentication.click()
        proxy_username.clear()
        proxy_username.send_keys("admin")
        proxy_password.clear()
        proxy_password.send_keys("norman")
        windows_nt_domainname.clear()
        windows_nt_domainname.send_keys("domain")
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click() ### Save Settings
        time.sleep(1)
        if (use_proxy_server.is_selected() == True):
            print "Checkpoint 17: [PASSED] Proxy server check box is selected/enabled after saving the configuration."
        else:
            print "Checkpoint 17: [FAILED] Proxy server check-box didn't get enabled after saving the configuration."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        if (str(proxy_address.get_attribute("value")) == "192.168.4.67"):
            print 'Checkpoint 18: [PASSED] Proxy address successfully saved as "192.168.4.67" after saving configuration.'
        else:
            print 'Checkpoint 18: [FAILED] Proxy address not saved after saving configuration.'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        if (proxy_authentication.is_selected() == True):
            print "Checkpoint 19: [PASSED] Proxy authentication check box is selected/enabled after saving the configuration."
        else:
            print "Checkpoint 19: [FAILED] Proxy authentication check-box didn't get enabled after saving the configuration."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        if (str(proxy_username.get_attribute("value")) == "admin"):
            print 'Checkpoint 20: [PASSED] Proxy username successfully saved as "admin" after saving configuration.'
        else:
            print 'Checkpoint 20: [FAILED] Proxy username not saved after saving configuration.'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        if (str(proxy_password.get_attribute("value")) == "norman"):
            print 'Checkpoint 21: [PASSED] Proxy password successfully saved as "norman" after saving configuration.'
        else:
            print 'Checkpoint 21: [FAILED] Proxy password not saved after saving configuration.'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        if (str(windows_nt_domainname.get_attribute("value")) == "domain"):
            print 'Checkpoint 22: [PASSED] Windows NT Domain name successfully saved as "domain" after saving configuration.'
        else:
            print 'Checkpoint 22: [FAILED] Windows NT Domain name not saved after saving configuration.'
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        
        print "\n\n#### Verify that Proxy address and Proxy username cannot be saved without any valid value."
        proxy_address.clear()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click() ### Save Settings
        a = b.find_element_by_class_name("alert-danger")
         
        if "Please enter a valid proxy address" not in a.text:
            print "Checkpoint 23: [FAILED] empty value saved successfully as proxy address."
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print "Checkpoint 23: [PASSED] empty value not saved as proxy address."
        time.sleep(1)
        proxy_address.send_keys("192.168.4.67")
        time.sleep(7)
        
        proxy_username.clear()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click() ### Save Settings
        a = b.find_element_by_class_name("alert-danger")
        if "Please enter a valid proxy username" not in a.text:
            print "Checkpoint 24: [FAILED] empty value saved successfully as proxy username."
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print "Checkpoint 24: [PASSED] empty value not saved as proxy username."
        time.sleep(1)
        proxy_username.send_keys("admin")
                
        #### Disable Proxy Server ####
        use_proxy_server.click()
        b.find_element_by_xpath('//*[@id="update_configuration"]/div/button').click() ### Save Settings
        
    def tearDown(self):
        do_logout(self)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
    
