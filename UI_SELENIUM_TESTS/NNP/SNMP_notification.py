import unittest, pprint, time, sys
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
    time.sleep(2)
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
    
    print "Clicking on SNMP"
    b.find_element_by_xpath('//*[@id="message_handling"]/div/div/ul/li[2]/a').click()
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="snmp_part"]/div[1]/span[1]/input'))
        )
    except:
        print "Checkpoint 4: [FAILED] SNMP page not loaded."
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 4: [PASSED] SNMP page appeared successfully."
    

class snmpnotification(unittest.TestCase):
    nnp_ip = "https://192.168.3.241/"
    
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_A_(self):
        print "\n\n##### TC1 - Verify SNMP notification."
        do_login(self)
        b=self.driver
        time.sleep(2)
        enable_snmp = b.find_element_by_xpath('//*[@id="snmp_part"]/div[1]/span[1]/input')
        if (enable_snmp.is_selected() == True):
            enable_snmp.click()
        enable_snmp.click()
        messages_to_send = b.find_element_by_xpath('//*[@id="snmp_part"]/div[1]/span[2]/select/option[1]').click()
        community = b.find_element_by_xpath('//*[@id="snmp_part"]/div[2]/span[1]/input')
        community.clear()
        community.send_keys("bhallacommunity")
        user_msg = b.find_element_by_xpath('//*[@id="snmp_part"]/div[2]/span[2]/input')
        user_msg.clear()
        user_msg.send_keys("bhallatrap")
        b.find_element_by_id("save_snmp_settings").click()
        time.sleep(2)
            
        if (enable_snmp.is_selected() == True):
            print "Checkpoint 5: [PASSED] SNMP notifications enabled successfully."
        else:
            print "Checkpoint 5: [FAILED] SNMP notifications not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        messages_to_send = b.find_element_by_xpath('//*[@id="snmp_part"]/div[1]/span[2]/select/option[1]').get_attribute("text")
            
        if (messages_to_send == "Alarm messages only"):
            print 'Checkpoint 6: [PASSED] Messages to send successfully set as "Alarm messages only.'
        else:
            print 'Checkpoint 6: [FAILED] Failed to set messages to send as "Alarm messages only.'
            
        if (community.get_attribute("value") == "bhallacommunity"):
            print 'Checkpoint 7: [PASSED] Community set to "bhallacommunity'
        else:
            print 'Checkpoint 7: [PASSED] Failed to set a community.'
            print self.fail("Case Status: FAILED")
            return 0
            
        if (user_msg.get_attribute("value") == "bhallatrap"):
            print 'Checkpoint 8: [PASSED] User message set to "bhallacommunity'
        else:
            print 'Checkpoint 8: [FAILED] Failed to set a User message.'
            print self.fail("Case Status: FAILED")
            return 0
        
    def test_b_set_msg_to_send(self):
        print "\n\n##### TC2 - Set messages to send"
        do_login(self)
        b=self.driver
        time.sleep(2)                
        messages_to_send = b.find_element_by_xpath('//*[@id="snmp_part"]/div[1]/span[2]/select/option[1]').click()
        b.find_element_by_id("save_snmp_settings").click()
        time.sleep(1)
        messages_to_send = b.find_element_by_xpath('//*[@id="snmp_part"]/div[1]/span[2]/select/option[1]').get_attribute("text")
        if (messages_to_send == "Alarm messages only"):
            print 'Checkpoint 5: [PASSED] Messages to send successfully set to "Alarm messages only"'
        else:
            print 'Checkpoint 5: [FAILED] Failed to set messages to send as "Alarm messages only"'
            print self.fail("Case Status: FAILED.")
            return 0
              
        messages_to_send = b.find_element_by_xpath('//*[@id="snmp_part"]/div[1]/span[2]/select/option[2]').click()
        b.find_element_by_id("save_snmp_settings").click()
        time.sleep(1)
        messages_to_send = b.find_element_by_xpath('//*[@id="snmp_part"]/div[1]/span[2]/select/option[2]').get_attribute("text")
        if (messages_to_send == "Messages of high priority"):
            print 'Checkpoint 6: [PASSED] Messages to send successfully set to "Messages of high priority"'
        else:
            print 'Checkpoint 6: [FAILED] Failed to set messages to send as "Messages of high priority"'
            print self.fail("Case Status: FAILED.")
            return 0
                
        messages_to_send = b.find_element_by_xpath('//*[@id="snmp_part"]/div[1]/span[2]/select/option[3]').click()
        b.find_element_by_id("save_snmp_settings").click()
        time.sleep(1)
        messages_to_send = b.find_element_by_xpath('//*[@id="snmp_part"]/div[1]/span[2]/select/option[3]').get_attribute("text")
        if (messages_to_send == "All messages"):
            print 'Checkpoint 7: [PASSED] Messages to send successfully set to "All messages"'
        else:
            print 'Checkpoint 7: [FAILED] Failed to set messages to send as "All messages"'
            print self.fail("Case Status: FAILED.")
            return 0
                
    def test_c_add_del_snmprecipient(self):
        print "\n\n##### TC3 - Add and Delete a snmp recipient."
        b=self.driver
        do_login(self)
        print "### Adding a single snmp recipient."
        snmp_recipient = b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/input')
        snmp_recipient.clear()
        snmp_recipient.send_keys("192.168.4.1")
        b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/button[1]').click()
        time.sleep(1)
        snmp_recipient_added = b.find_element_by_xpath('//*[@id="snmp_recipients"]/tbody/tr/td')
        if (snmp_recipient_added.text == "192.168.4.1"):
            print 'Checkpoint 5: [PASSED] SNMP recipient "192.168.4.1" added successfully.'
        else:
            print 'Checkpoint 5: [FAILED] SNMP recipient "192.168.4.1" not added.'
            print self.fail("Case Status: FAILED.")
            return 0
        print "### Deleting the recipient added above."
        snmp_recipient_added.click()
        b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/button[2]').click()
        time.sleep(1)
        snmp_recipient_added = b.find_element_by_xpath('//*[@id="snmp_recipients"]/tbody/tr/td')
        if (snmp_recipient_added.text == "192.168.4.1"):
            print 'Checkpoint 6: [FAILED] SNMP recipient "192.168.4.1" not deleted.'
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print 'Checkpoint 6: [PASSED] SNMP recipient deleted successfully'
               
    def test_d_add_search_delete_multiple_recipients(self):
        ##ADD Multiple Recipients - Total 10 recipients ####
        print "\n\n##### TC4 - Adding, searching, Deletion of multiple snmp recipients"
        do_login(self)
        b=self.driver
        print "##### Adding 10 snmp recipients"
        for x in range (1,11):
            snmp_recipient = b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/input')
            snmp_recipient.clear()
            snmp_recipient.send_keys("192.168.4.%d" %(x))
            time.sleep(1)
            b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/button[1]').click()
            time.sleep(1)
        print "Following recipients added:"
        for x in range (1,11):
            snmp_recipient = b.find_element_by_xpath('//*[@id="snmp_recipients"]/tbody/tr[%d]/td' % (x))
            #print snmp_recipient.text
            a = str(snmp_recipient.text)
            print a
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="snmp_recipients"]/tbody/tr[10]/td'))
            )
        except:
            print "Checkpoint 5: [FAILED] SNMP recipients not added successfully."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 5: [PASSED] SNMP recipients added successfully."
           
        ### Searching snmp recipients #####
        print "\n\n##### Searching of Email recipients"
        search_input = b.find_element_by_xpath('//*[@id="snmp_recipients_filter"]/label/input')
        search_input.clear()
        search_input.send_keys("4.9")
        time.sleep(1)
        search_result = b.find_element_by_xpath('//*[@id="snmp_recipients"]/tbody/tr/td')
        if (search_result.text == "192.168.4.9"):
            print "Checkpoint 6: [PASSED] Searching working fine on snmp recipients."
        else:
            print "Checkpoint 6: [FAILED] Searching not working on snmp recipients."
            print self.fail("Case Status: FAILED.")
            return 0
        search_input.send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE)
            
        #### Test Paging #####
        print "\n\n##### TC6 - Test Paging."
        print "#### Adding one more recipient to create a second page #####"
        snmp_recipient = b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/input') ### Search input box
        snmp_recipient.clear()
        snmp_recipient.send_keys("192.168.4.11")
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/button[1]').click()
        time.sleep(1)
        snmp_recipient_info = b.find_element_by_id("snmp_recipients_info")
          
        if "Showing 1 to 10 of 11 entries" in snmp_recipient_info.text:
            print "Checkpoint 7: [PASSED] One more snmp recipient added and a second page is created."
        else:
            print "Checkpoint 7: [FAILED] SNMP recipient not added for generating a second page to test the paging."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Clicking on Next (icon) to test the paging."
        b.find_element_by_id("snmp_recipients_next").click()
        time.sleep(2)
                
        next_page = b.find_element_by_xpath('//*[@id="snmp_recipients"]/tbody/tr/td')
        if (next_page.text == "192.168.4.9"):
            print "Checkpoint 8: [PASSED] Paging working fine on snmp recipients."
        else:
            print "Checkpoint 8: [FAILED] Paging not working on snmp recipients."
            print self.fail("Case Status: FAILED.")
            return 0
          
    #################################################################################
    ### Verify number of recipients to be shown per page #####
          
        time.sleep(1)
        print "\n\n##### TC 7 - Verify number of snmp recipients to be shown per page."
        print 'Selecting "25" entries to be shown per page'
        b.find_element_by_xpath('//*[@id="snmp_recipients_length"]/label/select/option[2]').click()
        time.sleep(1)
        num_of_entries = b.find_element_by_xpath('//*[@id="snmp_recipients_length"]/label/select/option[2]').text
        print num_of_entries
             
        if "25" in num_of_entries:
            print 'Checkpoint 9: [PASSED] "25" selected successfully.'
        else:
            print 'Checkpoint 9: [FAILED] Failed to select "25".'
            print self.fail("Case Status: FAILED.")
            return 0
        ### Adding 20 more recipients #####
        print "\n##### Adding 20 more recipients"
        for x in range (15,35):
            snmp_recipient = b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/input')
            snmp_recipient.clear()
            snmp_recipient.send_keys("192.168.4.%d" %(x))
            time.sleep(1)
            b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/button[1]').click()
            time.sleep(1)
             
        snmp_recipient_info = b.find_element_by_id("snmp_recipients_info")
        time.sleep(1)
        if "Showing 1 to 25" in snmp_recipient_info.text:
            print "Checkpoint 10: [PASSED] 25 entries per page shown successfully."
        else:
            print "Checkpoint 10: [FAILED] 25 entries per page not shown."
            print self.fail("Case Status: FAILED.")
            return 0
            
        print 'Selecting "50" entries to be shown per page'
        b.find_element_by_xpath('//*[@id="snmp_recipients_length"]/label/select/option[3]').click()
        time.sleep(1)
        num_of_entries = b.find_element_by_xpath('//*[@id="snmp_recipients_length"]/label/select/option[3]').text
             
        if "50" in num_of_entries:
            print 'Checkpoint 11: [PASSED] "50" selected successfully.'
        else:
            print 'Checkpoint 11: [FAILED] Failed to select "50".'
            print self.fail("Case Status: FAILED.")
            return 0
        print "\n##### Adding 20 more recipients"
        for x in range (35,55):
            email_recipient = b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/input')
            email_recipient.clear()
            email_recipient.send_keys("192.168.4.%d" %(x))
            time.sleep(1)
            b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/button[1]').click()
            time.sleep(1)
        snmp_recipient_info = b.find_element_by_id("snmp_recipients_info")
        time.sleep(1)
        if "Showing 1 to 50" in snmp_recipient_info.text:
            print "Checkpoint 12: [PASSED] 50 entries per page shown successfully."
        else:
            print "Checkpoint 12: [FAILED] 50 entries per page not shown."
            print self.fail("Case Status: FAILED.")
            return 0
             
        #### Testing 100 entries per page
        print 'Selecting "100" entries to be shown per page'
        b.find_element_by_xpath('//*[@id="snmp_recipients_length"]/label/select/option[4]').click()
        time.sleep(1)
        num_of_entries = b.find_element_by_xpath('//*[@id="snmp_recipients_length"]/label/select/option[4]').text
             
        if "100" in num_of_entries:
            print 'Checkpoint 13: [PASSED] "100" selected successfully.'
        else:
            print 'Checkpoint 13: [FAILED] Failed to select "100".'
            print self.fail("Case Status: FAILED.")
            return 0
        print "\n##### Adding 50 more recipients"
        for x in range (55,105):
            email_recipient = b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/input')
            email_recipient.clear()
            email_recipient.send_keys("192.168.4.%d" %(x))
            time.sleep(1)
            b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/button[1]').click()
            time.sleep(1)
        snmp_recipient_info = b.find_element_by_id("snmp_recipients_info")
        time.sleep(1)
        if "Showing 1 to 100" in snmp_recipient_info.text:
            print "Checkpoint 14: [PASSED] 100 entries per page shown successfully."
        else:
            print "Checkpoint 14: [FAILED] 100 entries per page not shown."
            print self.fail("Case Status: FAILED.")
            return 0
           
        ### Delete all snmp recipients using "Select all and Remove #####
         
        print '\n\n##### TC8 - Deleting all recipients using Action button "Select all" and "Remove"'
        time.sleep(15)
         
        for x in range(1,3):
            b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/div/a').click() ### Clicking Action
            time.sleep(1)
            b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/div/ul/li[1]/a').click() ### Clicking Select All
            b.find_element_by_xpath('//*[@id="snmp_recipients"]/form/fieldset/div/button[2]').click() ### Clicking Remove button
           
        snmp_recipient_info = b.find_element_by_id("snmp_recipients_info")
          
        if "Showing 0 to 0 of 0 entries" in snmp_recipient_info.text:
            print "Checkpoint 15: [PASSED] All snmp recipients deleted successfully."
        else:
            print "Checkpoint 15: [FAILED] Failed to delete all email recipients."
            print self.fail("Case Status: FAILED.")
            return 0
          
        ### Disable SNMP Notification
        time.sleep(1)
        enable_snmp = b.find_element_by_xpath('//*[@id="snmp_part"]/div[1]/span[1]/input')
        if (enable_snmp.is_selected() == True):
            enable_snmp.click()
            b.find_element_by_id("save_snmp_settings").click()    
        
        
    def tearDown(self):
        do_logout(self)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
