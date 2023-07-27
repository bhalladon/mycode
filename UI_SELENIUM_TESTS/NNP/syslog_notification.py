import unittest, pprint, time, sys
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
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "uptime"))
        )
    except:
        print "Checkpoint 2: [FAILED] Page not loaded after successful login."
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
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Notifications"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Notifications' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Notifications").click()
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"message_handling")))
    except:
        print "Checkpoint 3: [FAILED] Notifications page not loaded."
        return 0
    print "Checkpoint 3: [PASSED] Navigated to 'Notifications' page successfully."
    print "Clicking on SYSLOG"
    b.find_element_by_xpath('//*[@id="message_handling"]/div/div/ul/li[3]/a').click()
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="syslog_part"]/div[1]/span[1]/input'))
        )
    except:
        print "Checkpoint 4: [FAILED] Syslog page not loaded."
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 4: [PASSED] Syslog page appeared successfully."
    

class syslognotification(unittest.TestCase):
    
    nnp_ip = "https://192.168.3.241/"
    
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_A_syslognotification(self):
        print "\n##### TC1 - verify syslog UI"
        do_login(self)
        b=self.driver
        time.sleep(2)
        enable_syslog = b.find_element_by_xpath('//*[@id="syslog_part"]/div[1]/span[1]/input')
        if (enable_syslog.is_selected() == True):
            #print "SNMP is already enabled."
            enable_syslog.click()
        enable_syslog.click()
        messages_to_send = b.find_element_by_xpath('//*[@id="syslog_part"]/div[1]/span[2]/select/option[1]').click()
        hostname = b.find_element_by_xpath('//*[@id="syslog_part"]/div[2]/span[1]/input')
        hostname.clear()
        hostname.send_keys("192.168.3.50")
        #port = b.find_element_by_xpath('//input[@type="number"])[2]')
        
        #port.clear()
        #port.send_keys("98")
        use_tcp = b.find_element_by_xpath('//*[@id="syslog_part"]/div[2]/span[3]/input')
        if (use_tcp.is_selected() == True):
            #print "TCP usage already enabled."
            use_tcp.click()
        use_tcp.click()
        b.find_element_by_id("save_syslog_settings").click()
        time.sleep(1)
         
        enable_syslog = b.find_element_by_xpath('//*[@id="syslog_part"]/div[1]/span[1]/input')
        if (enable_syslog.is_selected() == True):
            print "Checkpoint 5: [PASSED] Syslog notification enabled successfully."
        else:
            print "Checkpoint 5: [FAILED] Syslog notifications not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        messages_to_send = b.find_element_by_xpath('//*[@id="syslog_part"]/div[1]/span[2]/select/option[1]').get_attribute("text")
        if (messages_to_send == "Alarm messages only"):
            print 'Checkpoint 6: [PASSED] Messages to send successfully set to "Alarm messages only"'
        else:
            print 'Checkpoint 6: [FAILED] Failed to set messages to send as "Alarm messages only"'
            print self.fail("Case Status: FAILED.")
            return 0 
        hostname = b.find_element_by_xpath('//*[@id="syslog_part"]/div[2]/span[1]/input').get_attribute("value")
        if (hostname == "192.168.3.50"):
            print 'Checkpoint 7: [PASSED] Hostname successfully set to "192.168.3.50".'
        else:
            print 'Checkpoint 7: [FAILED] Hostname not set as "192.168.3.50".'
            print self.fail("Case Status: FAILED.")
            return 0
         
        use_tcp = b.find_element_by_xpath('//*[@id="syslog_part"]/div[2]/span[3]/input')
        if (use_tcp.is_selected() == True):
            print "Checkpoint 8: [PASSED] TCP usage enabled successfully."
        else:
            print "Checkpoint 8: [FAILED] TCP usage option not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        
    def test_B_set_msgtosend(self):
        print "\n\n ##### TC2 - Set Messages to send"
        do_login(self)
        b = self.driver
        
        time.sleep(2)
        messages_to_send = b.find_element_by_xpath('//*[@id="syslog_part"]/div[1]/span[2]/select/option[1]').click()
        b.find_element_by_id("save_syslog_settings").click()
        messages_to_send = b.find_element_by_xpath('//*[@id="syslog_part"]/div[1]/span[2]/select/option[1]').get_attribute("text")
        if (messages_to_send == "Alarm messages only"):
            print 'Checkpoint 5: [PASSED] Messages to send successfully set to "Alarm messages only"'
        else:
            print 'Checkpoint 5: [FAILED] Failed to set messages to send as "Alarm messages only"'
            print self.fail("Case Status: FAILED.")
            return 0
            
        time.sleep(2)
        messages_to_send = b.find_element_by_xpath('//*[@id="syslog_part"]/div[1]/span[2]/select/option[2]').click()
        b.find_element_by_id("save_syslog_settings").click()
        messages_to_send = b.find_element_by_xpath('//*[@id="syslog_part"]/div[1]/span[2]/select/option[2]').get_attribute("text")
        if (messages_to_send == "Messages of high priority"):
            print 'Checkpoint 6: [PASSED] Messages to send successfully set to "Messages of high priority"'
        else:
            print 'Checkpoint 6: [FAILED] Failed to set messages to send as "Messages of high priority"'
            print self.fail("Case Status: FAILED.")
            return 0
        
        time.sleep(2)
        messages_to_send = b.find_element_by_xpath('//*[@id="syslog_part"]/div[1]/span[2]/select/option[3]').click()
        b.find_element_by_id("save_syslog_settings").click()
        time.sleep(1)
        #messages_to_send = b.find_element_by_css_selector('#syslog_part > div:nth-child(1) > span:nth-child(2) > select > option:nth-child(3)').get_attribute("text")
        messages_to_send = b.find_element_by_xpath('//*[@id="syslog_part"]/div[1]/span[2]/select/option[3]').get_attribute("text")
        
        if (messages_to_send == "All messages"):
            print 'Checkpoint 7: [PASSED] Messages to send successfully set to "All messages"'
        else:
            print 'Checkpoint 7: [FAILED] Failed to set messages to send as "All messages"'
            print self.fail("Case Status: FAILED.")
            return 0
          
        #Disable syslog notifications
          
        enable_syslog = b.find_element_by_xpath('//*[@id="syslog_part"]/div[1]/span[1]/input')
        if (enable_syslog.is_selected() == True):
            enable_syslog.click()
            b.find_element_by_id("save_syslog_settings").click()

                
    def tearDown(self):
        do_logout(self)
        self.driver.close()
        
if __name__ == '__main__':
    unittest.main()
    
