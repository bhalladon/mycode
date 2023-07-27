import unittest, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

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
    print "Checkpoint 2: [PASSED] User logged in successfully."
    
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "USB"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'USB' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("USB").click()
    
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Scanner station options"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Scanner station options' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Scanner station options").click()
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.CLASS_NAME,"hostnameinput")))
    except:
        print "Checkpoint 3: [FAILED] USB settings page not loaded."
        return 0
    print "Checkpoint 3: [PASSED] Navigated to page 'Scanner Station Options' successfully."

def do_logout(self):
    self.driver.get(self.nnp_ip+'logout')


class USB_Settings(unittest.TestCase):
    nnp_ip = "https://192.168.3.242/"
    def setUp(self):
        self.sizzle_injected = False
        self.driver=webdriver.Firefox()
        
    def test_A_USBSettings(self):
        print "\n##### TC1 - To verify USB settings."
        b=self.driver
        do_login(self)
        ## Set the action taken when a malware is found
        time.sleep(1)
        #### Set to Do not clean #####
        b.find_element_by_css_selector("#scada_options > div > span:nth-child(1) > select > option:nth-child(1)").click()
        b.find_element_by_class_name("save_configuration").click()
            
        a = b.find_element_by_css_selector("#scada_options > div > span:nth-child(1) > select > option:nth-child(1)")
        if (a.text == "Do not clean"):
            print 'Checkpoint 4: [PASSED] Malware action successfully set to "Do not clean"'
        else:
            print 'Checkpoint 4: [FAILED] Malware action failed to set as "Do not clean"'
            print self.fail("Case Status: [FAILED]")
            return 0
        ##### Set to Try to clean #####
        time.sleep(1)
        a = b.find_element_by_css_selector("#scada_options > div > span:nth-child(1) > select > option:nth-child(2)")
        a.click()
        b.find_element_by_class_name("save_configuration").click()
        if (a.text == "Try to clean"):
            print 'Checkpoint 5: [PASSED] Malware action successfully set to "Try to clean"'
        else:
            print 'Checkpoint 5: [FAILED] Malware action failed to set as "Try to clean"'
            print self.fail("Case Status: [FAILED]")
            return 0
        ##### Set to Delete file #####
        time.sleep(1)
        a = b.find_element_by_css_selector("#scada_options > div > span:nth-child(1) > select > option:nth-child(3)")
        a.click()
        b.find_element_by_class_name("save_configuration").click()
        if (a.text == "Delete file"):
            print 'Checkpoint 6: [PASSED] Malware action successfully set to "Delete file"'
        else:
            print 'Checkpoint 6: [FAILED] Malware action failed to set as "Delete file"'
            print self.fail("Case Status: [FAILED]")
            return 0
      
        ###### Enable Driver monitor and Driver monitor address #######
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[2]/input')
        if (a.is_selected() == True):
            print "Checkpoint 7: Driver monitor is already enabled."
        else:
            a.click()
        driver_monitor_address = b.find_element_by_class_name("hostnameinput")
        driver_monitor_address.clear()
        driver_monitor_address.send_keys("192.168.3.202")
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[2]/input')
        driver_monitor_val = driver_monitor_address.get_attribute("value")
        if (a.is_selected() == True):
            print "Checkpoint 7: [PASSED] Driver monitor check-box enabled successfully."
        else:
            print "Checkpoint 7: [FAILED] Driver monitor check-box failed to get enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        if (driver_monitor_val == "192.168.3.202"):
            print "Checkpoint 8: [PASSED] Driver monitor address updated successfully."
        else:
            print "Checkpoint 8: [FAILED] Driver monitor address not updated."
            print self.fail("Case Status: FAILED.")
            return 0
          
            
        ####### Enable Folder Scan and Folder name #######
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[5]/input')
        if (a.is_selected() == True):
            a.click()
            #print "Checkpoint 9: Folder Scan is already enabled."
        a.click()
        folder_name = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[6]/input')
        folder_name.clear()
        folder_name.send_keys("hello")
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[5]/input')
        folder_name = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[6]/input').get_attribute("value")
        if (a.is_selected() == True):
            print "Checkpoint 9: [PASSED] Folder Scan check-box enabled successfully."
        else:
            print "Checkpoint 9: [FAILED] Folder Scan check-box failed to get enabled."
            print self.fail("Case Stauts: FAILED.")
            return 0
        if (folder_name == "hello"):
            print "Checkpoint 10: [PASSED] Folder name updated successfully."
        else:
            print "Checkpoint 10: [FAILED] Folder scan name not updated."
            print self.fail("Case Stauts: FAILED.")
            return 0
          
          
        ##### Enable encrypted USB Support #####
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[7]/input')
        if (a.is_selected() == True):
            print "Support for encrypted USB memory sticks already enabled."
        else:
            a.click()
            b.find_element_by_class_name("save_configuration").click()
            a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[7]/input')
            if (a.is_selected() == True):
                print "Checkpoint 11: [PASSED] Support for encrypyed USB memory sticks enabled successfully."
            else:
                print "Checkpoint 11: [FAILED] Support for encrypyed USB memory sticks not enabled."
                print self.fail("Case Status: FAILED.")
                return 0
          
        ##### verify all the available option for USB stick to be valid saved or not #####
        b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[1]').click()
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[1]')
        if (a.text == "Never expire"):
            print 'Checkpoint 12: [PASSED] USB stick validation set to "Never Expire".'
        else:
            print 'Checkpoint 12: [FAILED] USB stick validation failed to set as "Never Expire".'
         
        b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[2]').click()
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[2]')
        if (a.text == "6 hours"):
            print 'Checkpoint 13: [PASSED] USB stick validation set to "6 hours".'
        else:
            print 'Checkpoint 13: [FAILED] USB stick validation failed to set as "6 hours".'
         
        b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[3]').click()
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[3]')
        if (a.text == "12 hours"):
            print 'Checkpoint 14: [PASSED] USB stick validation set to "12 hours".'
        else:
            print 'Checkpoint 14: [FAILED] USB stick validation failed to set as "12 hours".'
             
        b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[4]').click()
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[4]')
        if (a.text == "1 day"):
            print 'Checkpoint 15: [PASSED] USB stick validation set to "1 day".'
        else:
            print 'Checkpoint 15: [FAILED] USB stick validation failed to set as "1 day".'
         
        b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[5]').click()
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[5]')
        if (a.text == "3 days"):
            print 'Checkpoint 16: [PASSED] USB stick validation set to "3 days".'
        else:
            print 'Checkpoint 16: [FAILED] USB stick validation failed to set as "3 days".' 
         
        b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[6]').click()
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[6]')
        if (a.text == "1 week"):
            print 'Checkpoint 17: [PASSED] USB stick validation set to "1 week".'
        else:
            print 'Checkpoint 17: [FAILED] USB stick validation failed to set as "1 week".'
         
        b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[7]').click()
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[7]')
        if (a.text == "1 month"):
            print 'Checkpoint 18: [PASSED] USB stick validation set to "1 month".'
        else:
            print 'Checkpoint 18: [FAILED] USB stick validation failed to set as "1 month".'
         
        b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[8]').click()
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[8]')
        if (a.text == "6 months"):
            print 'Checkpoint 19: [PASSED] USB stick validation set to "6 months".'
        else:
            print 'Checkpoint 19: [FAILED] USB stick validation failed to set as "6 months".'
         
        b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[9]').click()
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[4]/select/option[9]')
        if (a.text == "1 year"):
            print 'Checkpoint 20: [PASSED] USB stick validation set to "1 year".'
        else:
            print 'Checkpoint 20: [FAILED] USB stick validation failed to set as "1 year".'
            
        
        ##### Verify invalid values for driver monitor address ######
        b.refresh()
        time.sleep(1)
        print "\n\n##### TC2 - Verifying invalid values for driver monitor address field. For this first we need to enable the driver monitor option."
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[2]/input')
        if (a.is_selected() == True):
            print "Driver monitor is already enabled."
        else:
            a.click()
        driver_monitor_address = b.find_element_by_class_name("hostnameinput")
        driver_monitor_address.clear()
        driver_monitor_address.send_keys("") ### Empty value
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_class_name("alert-danger")
         
        if "Please enter a driver monitor address" not in a.text:
            print "Checkpoint 21: [FAILED] empty value saved successfully as driver monitor address."
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print "Checkpoint 21: [PASSED] empty value not saved as driver monitor address."
        b.refresh()
      
            
        ##### Verify invalid values for folder scan name ######
        time.sleep(1)
        
        print "\n\n##### TC3 - Verifying invalid values for folder scan address field. For this first we need to enable the driver monitor option."
        a = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[5]/input')
        if (a.is_selected() == True):
            print "Folder scan is already enabled."
        else:
            a.click()
        folder_name = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[6]/input')
        folder_name.clear()
        folder_name.send_keys("") #### Empty value
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_class_name("alert-danger")
       
        if "Please enter a folder name" not in a.text:
            print "Checkpoint 22: [FAILED] empty value saved successfully as folder scan name."
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print "Checkpoint 22: [PASSED] empty value not saved as folder scan name."
        
        b.refresh()
        time.sleep(1)
        folder_name = b.find_element_by_xpath('//*[@id="scada_options"]/div/span[6]/input')
        folder_name.clear()
        folder_name.send_keys("   ") #### Enter White-spaces
        b.find_element_by_class_name("save_configuration").click()
        a = b.find_element_by_class_name("alert-danger")
       
        if "Please enter a folder name" not in a.text:
            print "Checkpoint 23: [FAILED] White-spaces saved successfully as folder scan name."
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print "Checkpoint 23: [PASSED] White-spaces not saved as folder scan name."
        
    def tearDown(self):
        do_logout(self)
        self.driver.close()
     
if __name__ == '__main__':
    unittest.main()    
            
