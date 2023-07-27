import unittest, pprint, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from settings import *
#from selenium.webdriver.support.ui import Select

def do_logout(self):
    self.driver.get(nnp_ip+'logout')
    #self.driver.find_element_by_id("userbtn").click()
    #self.driver.find_element_by_link_text("Logout").click()

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
    time.sleep(2)
    username = b.find_element_by_name("username")
    username.clear()
    username.send_keys("admin")
    password = b.find_element_by_name("password")
    password.clear()
    password.send_keys("norman")
    b.find_element_by_class_name("btn-primary").click()
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID, "nnp_version_header"))
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
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 3: [PASSED] Navigated to 'Notifications' page successfully."

class Notifications(unittest.TestCase):
    #nnp_ip = "https://192.168.157.130/"
    
    def setUp(self):
        self.driver = webdriver.Firefox()
         
    
    def test_A_email(self):
        print "\n\n##### TC1 - Verify email notification."
        do_login(self)
        b=self.driver
        enable_email = b.find_element_by_xpath('//*[@id="email_part"]/div[1]/span[1]/input')
        if (enable_email.is_selected() == True):
            enable_email.click()
        enable_email.click()
        messages_to_send = b.find_element_by_xpath('//*[@id="email_part"]/div[1]/span[2]/select/option[1]').click()
        smtp_address = b.find_element_by_xpath('//*[@id="email_part"]/div[3]/span[1]/input')
        smtp_address.clear()
        smtp_address.send_keys("192.168.3.22")
        #b.find_element_by_xpath('//*[@rpcid="port"]').clear()
        #time.sleep(2)
        #print str(b.find_element_by_xpath('//*[@rpcid="port"]').get_attribute("value"))
        #b.find_element_by_xpath('//*[@rpcid="port"]').clear()
        #port = b.find_element_by_xpath('//input[@rpcid="port"]')
        #port.clear()
        #port.send_keys("67")
        #b.execute_script("document.getElementById('//id of element').setAttribute('attr', '10')")
        #b.execute_script("document.getElementsByTagName('input')[0].setAttribute('value','44')")
        #time.sleep(10)
        #port = b.find_element_by_xpath('//*[@id="email_part"]/div[3]/span[2]/input')
        #port.send_keys("28")
        #time.sleep(4)
           
        reply_to_add = b.find_element_by_xpath('//*[@id="email_part"]/div[3]/span[3]/input')
        reply_to_add.clear()
        reply_to_add.send_keys("replyto@test.local")
        subject = b.find_element_by_xpath('//*[@id="email_part"]/div[4]/span[1]/input')
        subject.clear()
        subject.send_keys("SMTP Notifications")
        append_text = b.find_element_by_xpath('//*[@id="email_part"]/div[4]/span[2]/input')
        append_text.clear()
        append_text.send_keys("www.test.local")
        user_auth = b.find_element_by_xpath('//*[@id="email_part"]/div[5]/span[1]/input')
        if (user_auth.is_selected()== True):
            user_auth.click()
               
        user_auth.click()
        username = b.find_element_by_xpath('//*[@id="email_part"]/div[5]/span[2]/input')
        username.clear()
        username.send_keys("user1")
        password = b.find_element_by_xpath('//*[@id="email_part"]/div[5]/span[3]/input')
        password.clear()
        password.send_keys("norman")
        use_ssl = b.find_element_by_xpath('//*[@id="email_part"]/div[5]/span[4]/input')
        if (use_ssl.is_selected() == True):
            use_ssl.click()
           
        use_ssl.click()
        validate_ssl_cert = b.find_element_by_xpath('//*[@id="email_part"]/div[5]/span[5]/input')
        if (validate_ssl_cert.is_selected() == True):
            validate_ssl_cert.click()
           
        validate_ssl_cert.click()
        b.find_element_by_id("save_email_settings").click()
        if (enable_email.is_selected() == True):
            print "Checkpoint 4: [PASSED] Email Notifications enabled successfully."
        else:
            print "Checkpoint 4: [FAILED] Email notifications not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        messages_to_send = b.find_element_by_xpath('//*[@id="email_part"]/div[1]/span[2]/select/option[1]').get_attribute("text")
        if (messages_to_send == "Alarm messages only"):
            print 'Checkpoint 5: [PASSED] Messages to send successfully set to "Alarm messages only"'
        else:
            print 'Checkpoint 5: [FAILED] Failed to set messages to send as "Alarm messages only"'
            print self.fail("Case Status: FAILED.")
            return 0
        smtp_address = b.find_element_by_xpath('//*[@id="email_part"]/div[3]/span[1]/input').get_attribute("value")
        if (smtp_address == "192.168.3.22"):
            print 'Checkpoint 6: [PASSED] SMTP address successfully set to "192.168.3.22"'
        else:
            print 'Checkpoint 6: [FAILED] SMTP address not as "192.168.3.22"'
            print self.fail("Case Status: FAILED.")
            return 0
        port = b.find_element_by_xpath('//*[@id="email_part"]/div[3]/span[2]/input').get_attribute("value")
        if (port == "25"):
            print 'Checkpoint 7: [PASSED] Port number successfully set to "25"'
        else:
            print 'Checkpoint 7: [FAILED] Port number failed to set as "25"'
            print self.fail("Case Status: FAILED.")
            return 0
        reply_to_add = b.find_element_by_xpath('//*[@id="email_part"]/div[3]/span[3]/input').get_attribute("value")
        if (reply_to_add == "replyto@test.local"):
            print 'Checkpoint 8: [PASSED] Reply to address successfully set as "replyto@test.local"'
        else:
            print 'Checkpoint 8: [FAILED] Reply to address not set as "replyto@test.local"'
            print self.fail("Case Status: FAILED.")
            return 0
           
        subject = b.find_element_by_xpath('//*[@id="email_part"]/div[4]/span[1]/input').get_attribute("value")
        if (subject == "SMTP Notifications"):
            print 'Checkpoint 9: [PASSED] Subject successfully set as "SMTP Notifications"'
        else:
            print 'Checkpoint 9: [FAILED] Subject not set as "SMTP Notifications"'
            print self.fail("Case Status: FAILED.")
            return 0
        if (user_auth.is_selected() == True):
            print "Checkpoint 10: [PASSED] User Authentication enabled successfully."
        else:
            print "Checkpoint 10: [FAILED] User Authentication not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        username = b.find_element_by_xpath('//*[@id="email_part"]/div[5]/span[2]/input').get_attribute("value")
        if (username == "user1"):
            print 'Checkpoint 11: [PASSED] Username successfully set to "user1"'
        else:
            print 'Checkpoint 11: [FAILED] Username not set as "user1"'
            print self.fail("Case Status: FAILED.")
            return 0
        password = b.find_element_by_xpath('//*[@id="email_part"]/div[5]/span[3]/input').get_attribute("value")
        if (password == "norman"):
            print 'Checkpoint 12: [PASSED] Password successfully set to "norman"'
        else:
            print 'Checkpoint 12: [FAILED] Password not set as "norman"'
            print self.fail("Case Status: FAILED.")
            return 0
        if (use_ssl.is_selected() == True):
            print "Checkpoint 13: [PASSED] SSL enabled successfully."
        else:
            print "Checkpoint 13: [FAILED] SSL not enabled."
            print self.fail("Case Status: FAILED.")
            return 0
        if (validate_ssl_cert.is_selected() == True):
            print "Checkpoint 14: [PASSED] SSL certificate validation enabled successfully."
        else:
            print "Checkpoint 14: [FAILED] SSL certificate validation not enabled."
            print self.fail("Case Status: FAILED.")
            return 0

    def test_b_set_msg_to_send(self):
        print "\n\n##### TC2 - Set messages to send"
        do_login(self)
        b=self.driver                
        messages_to_send = b.find_element_by_xpath('//*[@id="email_part"]/div[1]/span[2]/select/option[1]').click()
        b.find_element_by_id("save_email_settings").click()
        messages_to_send = b.find_element_by_xpath('//*[@id="email_part"]/div[1]/span[2]/select/option[1]').get_attribute("text")
        if (messages_to_send == "Alarm messages only"):
            print 'Checkpoint 4: [PASSED] Messages to send successfully set to "Alarm messages only"'
        else:
            print 'Checkpoint 4: [FAILED] Failed to set messages to send as "Alarm messages only"'
            print self.fail("Case Status: FAILED.")
            return 0
          
        messages_to_send = b.find_element_by_xpath('//*[@id="email_part"]/div[1]/span[2]/select/option[2]').click()
        b.find_element_by_id("save_email_settings").click()
        messages_to_send = b.find_element_by_xpath('//*[@id="email_part"]/div[1]/span[2]/select/option[2]').get_attribute("text")
        if (messages_to_send == "Messages of high priority"):
            print 'Checkpoint 5: [PASSED] Messages to send successfully set to "Messages of high priority"'
        else:
            print 'Checkpoint 5: [FAILED] Failed to set messages to send as "Messages of high priority"'
            print self.fail("Case Status: FAILED.")
            return 0
            
        messages_to_send = b.find_element_by_xpath('//*[@id="email_part"]/div[1]/span[2]/select/option[3]').click()
        b.find_element_by_id("save_email_settings").click()
        messages_to_send = b.find_element_by_xpath('//*[@id="email_part"]/div[1]/span[2]/select/option[3]').get_attribute("text")
        if (messages_to_send == "All messages"):
            print 'Checkpoint 6: [PASSED] Messages to send successfully set to "All messages"'
        else:
            print 'Checkpoint 6: [FAILED] Failed to set messages to send as "All messages"'
            print self.fail("Case Status: FAILED.")
            return 0
            
    def test_c_add_del_emailrecipients(self):
        print "\n\n##### TC3 - Add and Delete a single email recipient"
        do_login(self)
        b=self.driver
        email_recipient = b.find_element_by_xpath('//*[@id="email_recipient"]/form/fieldset/div/input')
        email_recipient.clear()
        email_recipient.send_keys("u1@test.local")
        time.sleep(1)
        b.find_element_by_css_selector("#email_recipient > form.form-inline > fieldset > div.control-group > button[name=\"add\"]").click()
        time.sleep(1)
        email_recipient = b.find_element_by_xpath('//*[@id="mail_recipients"]/tbody/tr/td')
           
        if (email_recipient.text == "u1@test.local"):
            print 'Checkpoint 4: [PASSED] Email recipient "u1@test.local" successfully added.'
        else:
            print 'Checkpoint 4: [FAILED] Email recipient "u1@test.local" not added.'
            print self.fail("Case Status: FAILED.")
            return 0
        print "\n### Deleting the above added recipient."
        b.find_element_by_xpath('//*[@id="mail_recipients"]/tbody/tr/td').click()
        b.find_element_by_xpath('//*[@id="email_recipient"]/form/fieldset/div/button[2]').click()
        #b.find_element_by_name("rem_entry").click()
        time.sleep(1)
        email_recipient = b.find_element_by_xpath('//*[@id="mail_recipients"]/tbody/tr/td')
           
        if (email_recipient.text == "u1@test.local"):
            print 'Checkpoint 5: [FAILED] Email recipient "u1@test.local" not deleted.'
            print self.fail("Case Status: FAILED.")
            return 0
        else:
            print 'Checkpoint 5: [PASSED] Email recipient "u1@test.local" successfully deleted.'
             
         
    def test_d_add_multiple_recipients(self):
        ## ADD Multiple Recipients - Total 11 recipients ####
        print "\n\n##### TC4 - Adding, searching, Deletion of email recipients"
        do_login(self)
        b=self.driver
        print "##### Adding 10 email recipients"
        for x in range (1,11):
            email_recipient = b.find_element_by_xpath('//*[@id="email_recipient"]/form/fieldset/div/input')
            email_recipient.clear()
            email_recipient.send_keys("u%d@test.local" %(x))
            time.sleep(1)
            b.find_element_by_css_selector("#email_recipient > form.form-inline > fieldset > div.control-group > button[name=\"add\"]").click()
            time.sleep(1)
        print "Following recipients added:"
        for x in range (1,11):
            email_recipient = b.find_element_by_xpath('//*[@id="mail_recipients"]/tbody/tr[%d]/td' % (x))
            #print email_recipient.text
            a = str(email_recipient.text)
            print a
        if "u9@test.local" in a:
            print "Checkpoint 4: [PASSED] Email recipients added successfully."
        else:
            print "Checkpoint 4: [FAILED] Email recipients not added successfully."
            print self.fail("Case Status: FAILED.")
            return 0
              
        ##### Search Email recipients #### 
        print "\n\n##### TC5 - Searching of Email recipients"
        b.find_element_by_css_selector("#mail_recipients_filter > label > input").clear()
        b.find_element_by_css_selector("#mail_recipients_filter > label > input").send_keys("u7")
        time.sleep(1)
        search_result = b.find_element_by_xpath('//*[@id="mail_recipients"]/tbody/tr/td')
        if (search_result.text == "u7@test.local"):
            print "Checkpoint 5: [PASSED] Searching working fine on email recipients."
        else:
            print "Checkpoint 5: [FAILED] Searching not working on email recipients."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_css_selector("#mail_recipients_filter > label > input").clear()
          
        ### Test Paging ####
        print "\n\n##### TC6 - Test Paging."
        email_recipient = b.find_element_by_xpath('//*[@id="email_recipient"]/form/fieldset/div/input')
        email_recipient.clear()
        email_recipient.send_keys("u11@test.local")
        time.sleep(1)
        b.find_element_by_css_selector("#email_recipient > form.form-inline > fieldset > div.control-group > button[name=\"add\"]").click()
        #email_recipient = b.find_element_by_xpath('//*[@id="mail_recipients"]/tbody/tr/td')
        b.refresh()
        time.sleep(1)
        mail_recipient_info = b.find_element_by_id("mail_recipients_info")
        time.sleep(1)
        if "Showing 1 to 10 of 11 entries" in mail_recipient_info.text:
            print "Checkpoint 6: [PASSED] One more email recipient added and a second page is created."
        else:
            print "Checkpoint 6: [FAILED] Email recipient not added for generating a second page to test the paging."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Clicking on Next (icon) to test the paging."
        b.find_element_by_id("mail_recipients_next").click()
        time.sleep(1)
              
        next_page = b.find_element_by_xpath('//*[@id="mail_recipients"]/tbody/tr/td')
        if (next_page.text == "u9@test.local"):
            print "Checkpoint 7: [PASSED] Paging working fine on email recipients."
        else:
            print "Checkpoint 7: [FAILED] Paging not working on email recipients."
            print self.fail("Case Status: FAILED.")
            return 0
          
        ##### Verify number of recipients to be shown per page #####
        b.refresh()
        time.sleep(2)
        print "\n\n##### TC 7 - Verify number of email recipients to be shown per page."
        print 'Selecting "25" entries to be shown per page'
        b.find_element_by_xpath('//*[@id="mail_recipients_length"]/label/select/option[2]').click()
        time.sleep(1)
        num_of_entries = b.find_element_by_xpath('//*[@id="mail_recipients_length"]/label/select/option[2]').text
          
        if "25" in num_of_entries:
            print 'Checkpoint 8: [PASSED] "25" selected successfully.'
        else:
            print 'Checkpoint 8: [FAILED] Failed to select "25".'
            print self.fail("Case Status: FAILED.")
            return 0
        #### Adding 20 more recipients #####
        print "\n##### Adding 20 more recipients"
        for x in range (15,35):
            email_recipient = b.find_element_by_xpath('//*[@id="email_recipient"]/form/fieldset/div/input')
            email_recipient.clear()
            email_recipient.send_keys("u%d@test.local" %(x))
            #time.sleep(1)
            b.find_element_by_css_selector("#email_recipient > form.form-inline > fieldset > div.control-group > button[name=\"add\"]").click()
            time.sleep(1)
          
        mail_recipient_info = b.find_element_by_id("mail_recipients_info")
        time.sleep(1)
        if "Showing 1 to 25" in mail_recipient_info.text:
            print "Checkpoint 9: [PASSED] 25 entries per page shown successfully."
        else:
            print "Checkpoint 9: [FAILED] 25 entries per page not shown."
            print self.fail("Case Status: FAILED.")
            return 0
         
        print 'Selecting "50" entries to be shown per page'
        b.find_element_by_xpath('//*[@id="mail_recipients_length"]/label/select/option[3]').click()
        time.sleep(1)
        num_of_entries = b.find_element_by_xpath('//*[@id="mail_recipients_length"]/label/select/option[3]').text
          
        if "50" in num_of_entries:
            print 'Checkpoint 10: [PASSED] "50" selected successfully.'
        else:
            print 'Checkpoint 10: [FAILED] Failed to select "50".'
            print self.fail("Case Status: FAILED.")
            return 0
        print "\n##### Adding 20 more recipients"
        for x in range (35,55):
            email_recipient = b.find_element_by_xpath('//*[@id="email_recipient"]/form/fieldset/div/input')
            email_recipient.clear()
            email_recipient.send_keys("u%d@test.local" %(x))
            #time.sleep(1)
            b.find_element_by_css_selector("#email_recipient > form.form-inline > fieldset > div.control-group > button[name=\"add\"]").click()
            time.sleep(1)
        mail_recipient_info = b.find_element_by_id("mail_recipients_info")
        time.sleep(1)
        if "Showing 1 to 50" in mail_recipient_info.text:
            print "Checkpoint 11: [PASSED] 50 entries per page shown successfully."
        else:
            print "Checkpoint 11: [FAILED] 50 entries per page not shown."
            print self.fail("Case Status: FAILED.")
            return 0
          
        ##### Testing 100 entries per page
        print 'Selecting "100" entries to be shown per page'
        b.find_element_by_xpath('//*[@id="mail_recipients_length"]/label/select/option[4]').click()
        time.sleep(1)
        num_of_entries = b.find_element_by_xpath('//*[@id="mail_recipients_length"]/label/select/option[4]').text
          
        if "100" in num_of_entries:
            print 'Checkpoint 12: [PASSED] "100" selected successfully.'
        else:
            print 'Checkpoint 12: [FAILED] Failed to select "100".'
            print self.fail("Case Status: FAILED.")
            return 0
        print "\n##### Adding 50 more recipients"
        for x in range (55,105):
            email_recipient = b.find_element_by_xpath('//*[@id="email_recipient"]/form/fieldset/div/input')
            email_recipient.clear()
            email_recipient.send_keys("u%d@test.local" %(x))
            #time.sleep(1)
            b.find_element_by_css_selector("#email_recipient > form.form-inline > fieldset > div.control-group > button[name=\"add\"]").click()
            time.sleep(1)
        mail_recipient_info = b.find_element_by_id("mail_recipients_info")
        time.sleep(1)
        if "Showing 1 to 100" in mail_recipient_info.text:
            print "Checkpoint 13: [PASSED] 100 entries per page shown successfully."
        else:
            print "Checkpoint 13: [FAILED] 100 entries per page not shown."
            print self.fail("Case Status: FAILED.")
            return 0
         
        ##### Delete all email recipients using "Select all and Remove #####
        print '\n\n##### TC8 - Deleting all recipients using Action button "Select all" and "Remove"'
        #b.refresh()
        for x in range(1,3):
            b.find_element_by_xpath('//*[@id="email_recipient"]/form/fieldset/div/div/a').click()
            time.sleep(1)
            b.find_element_by_xpath('//*[@id="email_recipient"]/form/fieldset/div/div/ul/li[1]/a').click()
            b.find_element_by_xpath('//*[@id="email_recipient"]/form/fieldset/div/button[2]').click()
         
        mail_recipient_info = b.find_element_by_id("mail_recipients_info")
        print mail_recipient_info.text
        if "Showing 0 to 0 of 0 entries" in mail_recipient_info.text:
            print "Checkpoint 14: [PASSED] All email recipients deleted successfully."
        else:
            print "Checkpoint 14: [FAILED] Failed to delete all email recipients."
            print self.fail("Case Status: FAILED.")
            return 0
        
        #### Disable email Notification
        enable_email = b.find_element_by_xpath('//*[@id="email_part"]/div[1]/span[1]/input')
        if (enable_email.is_selected() == True):
            enable_email.click()
            b.find_element_by_id("save_email_settings").click()
            
    def tearDown(self):
        do_logout(self)
        self.driver.close()
        

if __name__ == '__main__':
    unittest.main()
            
