import unittest, pprint, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

def do_logout(self):
    self.driver.get(self.nnp_ip+'logout')

def do_login(self):
    self.driver.get(self.nnp_ip)
    self.driver.maximize_window()
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
    b.find_element_by_link_text("Network").click()
    
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Network Threat Discovery"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Network Threat Discovery' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Network Threat Discovery").click()
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"mag2config_part")))
    except:
        print "Checkpoint 3: [FAILED] Network Threat Discovery page not loaded."
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 3: [PASSED] Navigated to 'Network Threat Discovery' page successfully."

class Mailscanning(unittest.TestCase):
    
    nnp_ip = "https://192.168.3.241/"
    def setUp(self):
        self.driver = webdriver.Firefox()
        
    def test_A_configntd(self):
        print "\n>> #### TC1 - Configure NTD."
        do_login(self)
        b=self.driver
        enable_ntd = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[1]/input')
        if (enable_ntd.get_attribute("checked")):
            pass
        else:
            enable_ntd.click()
              
        hostname = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[2]/input')
        hostname.clear()
        hostname.send_keys("192.168.3.39")
              
        load_balancing = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[3]/select/option[1]').click()
        owner = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[4]/input')
        owner.clear()
        owner.send_keys("nnp531")
              
        automatically_add_blocklist = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[6]/input')
        if (automatically_add_blocklist.get_attribute("checked")):
            pass
        else:
            automatically_add_blocklist.click()
           
        drop_new_files = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[11]/input')
        drop_new_files.clear()
        drop_new_files.send_keys("10000")
              
        b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click() ## Saving configuration
              
        if (enable_ntd.get_attribute("checked")):
            print "Checkpoint 4: [PASSED] NTD enabled successfully."
        else:
            print "Checkpoint 4: [FAILED] NTD not enabled."
            print self.fail("Test Case Failed.")
            return 0
          
        if (hostname.get_attribute("value") == "192.168.3.39"):
            print "Checkpoint 5: [PASSED] Hostname saved with expected value."
        else:
            print "Checkpoint 5: [FAILED] Hostname not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0
              
        if (owner.get_attribute("value") == "nnp531"):
            print "Checkpoint 6: [PASSED] Owner saved with expected value."
        else:
            print "Checkpoint 6: [FAILED] Owner not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0
       
        if (drop_new_files.get_attribute("value") == "10000"):
            print "Checkpoint 7: [PASSED] Drop new files on size saved with expected value."
        else:
            print "Checkpoint 7: [FAILED] Drop new files on size not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0
              
        ## Verify load balancing #####
        b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[3]/select/option[1]').click()
        b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click() ## Saving configuration
              
        if (b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[3]/select/option[1]').get_attribute("value") == "true"):
            print "Checkpoint 8: [PASSED] Load balancing successfully saved with expected value."
        else:
            print "Checkpoint 8: [FAILED] Load balancing not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0        
             
#         time.sleep(2)
#         hostname.clear()
#         hostname.send_keys("192.168.3.39,192.168.3.40")
#         b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[3]/select/option[2]').click()
#         b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click() ## Saving configuration
#                
#         if (b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[3]/select/option[2]').get_attribute("value") == "true"):
#             print "Checkpoint 9: [PASSED] Load balancing successfully saved with expected value (Fallback one)."
#         else:
#             print "Checkpoint 9: [FAILED] Load balancing not saved with expected value (Fallback one)."
#             print self.fail("Test Case Failed.")
#             return 0
           
        #### Verify all risk threshold value
        print "\n"
        for x in range (1,12):     
            risk_score = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[5]/select/option[%d]' % (x))
            risk_score.click()
            b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click() ## Saving configuration
            risk_score = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[5]/select/option[%d]' % (x)).is_selected()
            if (risk_score):
                risk_score = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[5]/select/option[%d]' % (x))       
                print "Risk score saved as:" + risk_score.get_attribute("value")
            else:
                print "Checkpoint 9: Expected risk score value not saved."
                print self.fail("Test Case Failed.")
                return 0
               
        ### Verify Low risk deletion delay
        print "\n"
        for x in range (1,11):
            low_risk_task = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[7]/select/option[%d]' % (x))
            low_risk_task.click()
            b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click() ## Saving configuration
                
            low_risk_task = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[7]/select/option[%d]' % (x)).is_selected()
                
            if (low_risk_task):
                low_risk_task = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[7]/select/option[%d]' % (x))
                if (low_risk_task.get_attribute("value") == "0"):
                    print "Low risk task deletion delay saved as: Immediately"
                          
                elif (low_risk_task.get_attribute("value") == "6"):
                    print "Low risk task deletion delay saved as: 6 hours"
                    
                elif (low_risk_task.get_attribute("value") == "12"):
                    print "Low risk task deletion delay saved as: 12 hours"
                    
                elif (low_risk_task.get_attribute("value") == "24"):
                    print "Low risk task deletion delay saved as: 1 day"
                    
                elif (low_risk_task.get_attribute("value") == "72"):
                    print "Low risk task deletion delay saved as: 3 days"
                    
                elif (low_risk_task.get_attribute("value") == "168"):
                    print "Low risk task deletion delay saved as: 1 week"
                    
                elif (low_risk_task.get_attribute("value") == "720"):
                    print "Low risk task deletion delay saved as: 1 month"
                    
                elif (low_risk_task.get_attribute("value") == "2160"):
                    print "Low risk task deletion delay saved as: 3 months"
                    
                elif (low_risk_task.get_attribute("value") == "4320"):
                    print "Low risk task deletion delay saved as: 6 months"
                    
                elif (low_risk_task.get_attribute("value") == "-1"):
                    print "Low risk task deletion delay saved as: Forever"
               
            else:
                print "Checkpoint 10: [FAILED] Not able to save Low risk task deletion delay."
                print self.fail("Test case Failed.")
                return 0                 
   
        ### Verify High Risk Deletetion delay
        print "\n"
        for x in range (1,11):
            high_risk_task = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[8]/select/option[%d]' % (x))
            high_risk_task.click()
            b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click() ## Saving configuration
                 
            high_risk_task = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[8]/select/option[%d]' % (x)).is_selected()
                 
            if (high_risk_task):
                high_risk_task = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[8]/select/option[%d]' % (x))
                if (high_risk_task.get_attribute("value") == "0"):
                    print "High risk task deletion delay saved as: Immediately"
                           
                elif (high_risk_task.get_attribute("value") == "6"):
                    print "High risk task deletion delay saved as: 6 hours"
                     
                elif (high_risk_task.get_attribute("value") == "12"):
                    print "High risk task deletion delay saved as: 12 hours"
                     
                elif (high_risk_task.get_attribute("value") == "24"):
                    print "High risk task deletion delay saved as: 1 day"
                     
                elif (high_risk_task.get_attribute("value") == "72"):
                    print "High risk task deletion delay saved as: 3 days"
                     
                elif (high_risk_task.get_attribute("value") == "168"):
                    print "High risk task deletion delay saved as: 1 week"
                     
                elif (high_risk_task.get_attribute("value") == "720"):
                    print "High risk task deletion delay saved as: 1 month"
                     
                elif (high_risk_task.get_attribute("value") == "2160"):
                    print "High risk task deletion delay saved as: 3 months"
                     
                elif (high_risk_task.get_attribute("value") == "4320"):
                    print "High risk task deletion delay saved as: 6 months"
                     
                elif (high_risk_task.get_attribute("value") == "-1"):
                    print "High risk task deletion delay saved as: Forever"
            else:
                print "Checkpoint 10: [FAILED] Nroutot able to save High risk task deletion delay."
                print self.fail("Test case Failed.")
                return 0 
                       
        ### Verify Local queue limits
        print "\n"
        for x in range(1,6):
            local_queue_limits = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[10]/select/option[%d]' % (x))
            local_queue_limits.click()
            b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click() ## Saving configuration
                 
            local_queue_limits = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[10]/select/option[%d]' % (x)).is_selected()
                 
            if (local_queue_limits):
                local_queue_limits = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[10]/select/option[%d]' % (x))
                if (local_queue_limits.get_attribute("value") == "-1"):
                    print "Local queue limits saved as: Unlimited"
                   
                else:
                    print "Local queue limit saved as:" + local_queue_limits.get_attribute("value")
            else:
                print "Checkpoint 10: [FAILED] Not able to save local queue limits."
                print self.fail("Test case Failed.")
                return 0
          
        ### Verify Queue Limit
        print "\n"
        for x in range(1,6):
            queue_limits = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[12]/select/option[%d]' % (x))
            queue_limits.click()
            b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click() ## Saving configuration
                
            queue_limits = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[12]/select/option[%d]' % (x)).is_selected()
                
            if (queue_limits):
                queue_limits = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[12]/select/option[%d]' % (x))
                if (queue_limits.get_attribute("value") == "-1"):
                    print "Queue limits saved as: Unlimited"
                  
                else:
                    print "Queue limit saved as:" + queue_limits.get_attribute("value")
            else:
                print "Checkpoint 10: [FAILED] Not able to save queue limits."
                print self.fail("Test case Failed.")
                return 0
        
#     def test_B_invalidvalues(self):
#         print "\n>> #### TC2 - Verify that blank values are not accepted."
#         do_login(self)
#         b=self.driver
#         time.sleep(2)
#         
#         hostname = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[2]/input')
#         hostname.clear()
#         b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click() ## Saving configuration
#         time.sleep(2)
#         
#         
#         if (hostname.get_attribute("value") == ""):
#             print "Checkpoint 4: [PASSED] As expected empty value for hostname is not saved."
#         else:
#             print "Checkpoint 4: [FAILED] Empty value saved for hostname."
#             print self.fail("Test Case Failed.")
#             return 0
#         #####################
#         owner = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[4]/input')
#         owner.clear()
#         b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click() ## Saving configuration
#         time.sleep(2)
#         
#         if (owner.get_attribute("value") == ""):
#             print "Checkpoint 5: [PASSED] As expected empty value for owner is not saved."
#         else:
#             print "Checkpoint 5: [FAILED] Empty value saved for owner."
#             print self.fail("Test Case Failed.")
#             return 0
#         #######################
#         dropnewfiles = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[11]/input')
#         dropnewfiles.clear()
#         b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click() ## Saving configuration
#         time.sleep(2)
#         
#         if (dropnewfiles.get_attribute("value") == ""):
#             print dropnewfiles.get_attribute("value")
#             print "Checkpoint 6: [PASSED] As expected empty value for drop new files on size is not saved."
#         else:
#             print "Checkpoint 6: [FAILED] Empty value saved drop new files on size."
#             print self.fail("Test Case Failed.")
#             return 0
            
    def tearDown(self):
        do_logout(self)
        self.driver.close()