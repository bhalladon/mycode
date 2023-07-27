
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
    b.find_element_by_link_text("Network").click()
    
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Mail Scanning"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Mail Scanning' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Mail Scanning").click()
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"mail_scanning")))
    except:
        print "Checkpoint 3: [FAILED] Mail scanning page not loaded."
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 3: [PASSED] Navigated to 'Mail Scanning' page successfully."

class Mailscanning(unittest.TestCase):
    
    nnp_ip = "https://192.168.3.241/"
    def setUp(self):
        self.driver = webdriver.Firefox()
    
    def test_A_basicconfig(self):
        do_login(self)
        b=self.driver
        print "\n>> #### TC1 - To verify that if mail scanning is not enabled then rest of the options are grayed out"
          
        a = b.find_element_by_name("enable_mail_scanning").get_attribute("checked")
        if (a):
            b.find_element_by_name("enable_mail_scanning").click()
        else:
            pass
              
        scan_engine = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[2]/input').is_enabled()
        if (scan_engine == False):
            print "Checkpoint 4: [PASSED] Scanning with engine option is disabled as expected."
        else:
            print "Checkpoint 4: [FAILED] Scanning with engine option not grayed out when mail scanning is disabled."
            print self.fail("Test case Failed.")
            return 0
          
        scan_ma = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[3]/input').is_enabled()
        if (scan_ma == False):
            print "Checkpoint 5: [PASSED] Scanning with MA option is disabled as expected."
        else:
            print "Checkpoint 5: [FAILED] Scanning with MA option not grayed out when mail scanning is disabled."
            print self.fail("Test case Failed.")
            return 0
          
        relay_dest_ip = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[4]/input').is_enabled()
        if (relay_dest_ip == False):
            print "Checkpoint 6: [PASSED] Text input box for Relay Destination IP is disabled as expected."
        else:
            print "Checkpoint 6: [FAILED] Text input box for Relay Destination IP not grayed out when mail scanning is disabled."
            print self.fail("Test case Failed.")
            return 0
          
        fwd_qtn_mail = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[5]/input').is_enabled()
        if (relay_dest_ip == False):
            print "Checkpoint 7: [PASSED] Text input box for Relay Destination IP is disabled as expected."
        else:
            print "Checkpoint 7: [FAILED] Text input box for Relay Destination IP not grayed out when mail scanning is disabled."
            print self.fail("Test case Failed.")
            return 0
          
        my_networks = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[6]/input').is_enabled()
        if (my_networks == False):
            print "Checkpoint 8: [PASSED] Text input box for My networks is disabled as expected."
        else:
            print "Checkpoint 8: [FAILED] Text input box for My networks not grayed out when mail scanning is disabled."
            print self.fail("Test case Failed.")
            return 0
          
        ############################################################################################
          
        print "\n>> #### TC2 - To verify that if mail scanning check-box is selected then rest of the options are not grayed out"
          
        a = b.find_element_by_name("enable_mail_scanning").get_attribute("checked")
        if (a):
            pass
        else:
            b.find_element_by_name("enable_mail_scanning").click()
              
        scan_engine = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[2]/input').is_enabled()
        if (scan_engine == True):
            print "Checkpoint 9: [PASSED] Scanning with engine option is enabled as expected."
        else:
            print "Checkpoint 9: [FAILED] Scanning with engine option grayed out when mail scanning is enabled."
            print self.fail("Test case Failed.")
            return 0
          
        relay_dest_ip = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[4]/input').is_enabled()
        if (relay_dest_ip == True):
            print "Checkpoint 10: [PASSED] Text input box for Relay Destination IP is enabled as expected."
        else:
            print "Checkpoint 10: [FAILED] Text input box for Relay Destination IP grayed out when mail scanning is enabled."
            print self.fail("Test case Failed.")
            return 0
          
        fwd_qtn_mail = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[5]/input').is_enabled()
        if (relay_dest_ip == True):
            print "Checkpoint 11: [PASSED] Text input box for Relay Destination IP is enabled as expected."
        else:
            print "Checkpoint 11: [FAILED] Text input box for Relay Destination IP grayed out when mail scanning is enabled."
            print self.fail("Test case Failed.")
            return 0
          
        my_networks = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[6]/input').is_enabled()
        if (my_networks == True):
            print "Checkpoint 12: [PASSED] Text input box for My networks is enabled as expected."
        else:
            print "Checkpoint 12: [FAILED] Text input box for My networks grayed out when mail scanning is enabled."
            print self.fail("Test case Failed.")
            return 0
          
        ##################################################################################################
          
        print "\n>> #### TC3 - To verify 'Scan mail with MA' enabled only if NTD is enabled."
        time.sleep(2)
        b.find_element_by_link_text("Network").click()
        try:
            element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Network Threat Discovery"))
            )
        except:
            print "Checkpoint 13: [FAILED] Network Threat Discovery link not found."
            print self.fail("Test case Failed.")
            return 0
          
        b.find_element_by_link_text("Network Threat Discovery").click()
          
        try:
            element = WebDriverWait (b,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mag2config_part"]/div/div/div/span[1]/input'))
            )
        except:
            print "Checkpoint 13: [FAILED] NTD page not loaded."
            print self.fail("Test case Failed.")
            return 0
        print "Checkpoint 13: [PASSED] Navigated to NTD page successfully."
        ntd_checkbox = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[1]/input').get_attribute("checked")
        if (ntd_checkbox):
            pass
        else:
            b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[1]/input').click()
            hostname = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[2]/input')
            hostname.clear()
            hostname.send_keys("192.168.3.39")
            owner = b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/div/span[4]/input')
            owner.clear()
            owner.send_keys("nnp")
            b.find_element_by_xpath('//*[@id="mag2config_part"]/div/div/button').click()
          
        time.sleep(2)
        b.find_element_by_link_text("Network").click()
        try:
            element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Mail Scanning"))
            )
        except:
            print "Checkpoint 13: [FAILED] Mail Scanning link not found."
            print self.fail("Test case Failed.")
            return 0
          
        b.find_element_by_link_text("Mail Scanning").click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"mail_scanning"))
            )
        except:
            print "Checkpoint 3: [FAILED] Mail scanning page not loaded."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 14: [PASSED] Navigated to 'Mail Scanning' page successfully."
          
        if (a):
            pass
        else:
            b.find_element_by_name("enable_mail_scanning").click()
          
        scan_ma = b.find_element_by_name("enable_mail_scanning").is_enabled()
        if (scan_ma == True):
            print "Checkpoint 15: [PASSED] Scanning with MA option is enabled as expected when mail scanning and NTD is enabled."
        else:
            print "Checkpoint 15: [FAILED] Scanning with MA option grayed out when mail scanning and NTD is enabled."
            print self.fail("Test case Failed.")
            return 0
          
        ######################################################################################
        print "\n>> #### TC4 - Configure Basic Configuration of Mail Scanning"
        time.sleep(2)
        a = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[1]/input').get_attribute("checked")
        if (a):
            pass
        else:
            b.find_element_by_name("enable_mail_scanning").click()
              
        time.sleep(1)
        scan_engine = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[2]/input').get_attribute("checked")
        if (scan_engine):
            pass
        else:
            b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[2]/input').click()
          
        time.sleep(1)
        scan_ma = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[3]/input').get_attribute("checked")
        if (scan_ma):
            pass
        else:
            b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[3]/input').click()
          
        relay_dest_ip = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[4]/input')
        relay_dest_ip.clear()
        relay_dest_ip.send_keys("192.168.3.18")
          
        fwd_qtn_mail = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[5]/input')
        fwd_qtn_mail.clear()
        fwd_qtn_mail.send_keys("u1@nnpint.local")
          
        my_networks = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[6]/input')
        my_networks.clear()
        my_networks.send_keys("192.0.0.0/8")
          
        b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/button').click()
          
        a = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[1]/input').get_attribute("checked")
        if (a):
            print "Checkpoint 16: [PASSED] Mail scanning check-box enabled successfully after saving configuration"
        else:
            print "Checkpoint 16: [FAILED] Mail scanning check-box remains disabled after saving configuration."
            print self.fail("Test Case Failed.")
            return 0
          
        scan_engine = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[2]/input').get_attribute("checked")
        if (scan_engine):
            print "Checkpoint 17: [PASSED] Scanning with scan engine check-box enabled successfully after saving configuration"
        else:
            print "Checkpoint 17: [FAILED] Scanning with scan engine check-box remains disabled after saving configuration."
            print self.fail("Test Case Failed.")
            return 0
          
        scan_ma = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[3]/input').get_attribute("checked")
        if (scan_ma):
            print "Checkpoint 18: [PASSED] Scanning with MA check-box enabled successfully after saving configuration"
        else:
            print "Checkpoint 18: [FAILED] Scanning with MA check-box remains disabled after saving configuration."
            print self.fail("Test Case Failed.")
            return 0
          
        relay_dest_ip = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[4]/input').get_attribute("value")
        if (relay_dest_ip == "192.168.3.18"):
            print "Checkpoint 19: [PASSED] Relay destination IP successfully saved with expected value."
        else:
            print "Checkpoint 19: [FAILED] Relay destination IP not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0
          
        fwd_qtn_mail = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[5]/input').get_attribute("value")
        if (fwd_qtn_mail == "u1@nnpint.local"):
            print "Checkpoint 20: [PASSED] Forward Quarantine mail successfully saved with expected value."
        else:
            print "Checkpoint 20: [FAILED] Forward Quarantine mail not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0
          
          
        my_networks = b.find_element_by_xpath('//*[@id="basic_configuration"]/div/div/div/div/span[6]/input').get_attribute("value")
        if (my_networks == "192.0.0.0/8"):
            print "Checkpoint 21: [PASSED] My networks successfully saved with expected value."
        else:
            print "Checkpoint 21: [FAILED] My networks destination IP not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0
        
    
    def test_B_EmailNotifications(self):
        print "\n>> #### TC5 - Configure Email Notifications of Mail Scanning."
        print ">> #### Verify email notifications enable check-box remains grayed out if Mail scanning is not enabled."
        do_login(self)
        b=self.driver
        
        
        a = b.find_element_by_name("enable_mail_scanning").get_attribute("checked")
        if (a):
            b.find_element_by_xpath('//*[@id="mail_scanning"]/div[1]/ul/li[2]/a').click()
        else:
            b.find_element_by_name("enable_mail_scanning").click()
            b.find_element_by_xpath('//*[@id="mail_scanning"]/div[1]/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email_notifications"]/div/div/div/div/span[1]/input'))
            )                                    
        except:
            print "Checkpoint 4: [FAILED] Email Notifications page not loaded."
            print self.fail("Test case Failed.")
            return 0    
        print "Checkpoint 4: [PASSED] Naivgated to Email notifications page successfully."
        
        enable_email_notifications = b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/div/span[1]/input').is_enabled()
        if (enable_email_notifications == True):
            print "Checkpoint 5: [PASSED] Enable Email Notifications check-box is editable when mail scanning is enabled."
        else:
            print "Checkpoint 5: [FAILED] Enable Email notifications check-box is grayed out when mail scanning is enabled."
            print self.fail("Test case Failed.")
            return 0
        
        print "\n>> #### TC6 - Configure Email Notifications"
        enable_email_notifications = b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/div/span[1]/input').get_attribute("checked")
        if (enable_email_notifications):
            pass
        else:
            b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/div/span[1]/input').click()
        time.sleep(1)
        
        subject_line_prepend = b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/div/span[2]/input')
        subject_line_prepend.clear()
        subject_line_prepend.send_keys("Blocked by NNP")
        
        msg_body_prepend = b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/div/span[3]/div/div/textarea')
        msg_body_prepend.clear()
        msg_body_prepend.send_keys("Email Blocked by NNP. Please contact Administrator.")
        

        sender_address = b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/div/span[4]/input')
        sender_address.clear()
        sender_address.send_keys("notifications@bluecoat.com")
        
        reply_to_address = b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/div/span[5]/input')
        reply_to_address.clear()
        reply_to_address.send_keys("replyto@bluecoat.com")
        
        additional_recipients = b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/div/span[6]/input')
        additional_recipients.clear()
        additional_recipients.send_keys("u1@bluecoat.com,u2@bluecoat.com")
        
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/button').click()
        
        if (subject_line_prepend.get_attribute("value") == "Blocked by NNP"):
            print "Checkpoint 6: [PASSED] Subject line prepend successfully saved with expected value."
        else:
            print "Checkpoint 6: [FAILED] Subject line prepend not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0
        
        if (msg_body_prepend.get_attribute("value") == "Email Blocked by NNP. Please contact Administrator."):
            print "Checkpoint 7: [PASSED] Message Body Prepend saved with expected value."
        else:
            print "Checkpoint 7: [FAILED] Message Body Prepend not saved with expected value."
            print self.fail("Test Case Failed")
            return 0
        
        if (sender_address.get_attribute("value") == "notifications@bluecoat.com"):
            print "Checkpoint 8: [PASSED] Sender Address successfully saved with expected value."
        else:
            print "Checkpoint 8: [FAILED] Sender Address not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0    
        
        if (reply_to_address.get_attribute("value") == "replyto@bluecoat.com"):
            print "Checkpoint 9: [PASSED] Reply-to Address successfully saved with expected value."
        else:
            print "Checkpoint 9: [FAILED] Reply-to Address not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0 
        
        if (additional_recipients.get_attribute("value") == "u1@bluecoat.com,u2@bluecoat.com"):
            print "Checkpoint 10: [PASSED] Additional Recipients successfully saved with expected value."
        else:
            print "Checkpoint 10: [FAILED] Additional Recipients not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0            
        
        print "\n>> #### TC7 - Additional recipient field cannot be empty if exclude original recipients option is enabled."
        exclude_original_recipients = b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/div/span[7]/input').get_attribute("checked")
        if (exclude_original_recipients):
            additional_recipients.clear()
            b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/button').click() ## Saving Configuration
        else:
            b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/div/span[7]/input').click()
            additional_recipients.clear()
            b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/button').click() ## Saving Configuration
        b.refresh()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"mail_scanning"))
            )
        except:
            print "Checkpoint 11: [FAILED] Mail scanning page not loaded."
            print self.fail("Case Status: FAILED.")
            return 0
    
        b.find_element_by_xpath('//*[@id="mail_scanning"]/div[1]/ul/li[2]/a').click()
        time.sleep(2)
        additional_recipients = b.find_element_by_xpath('//*[@id="email_notifications"]/div/div/div/div/span[6]/input')
        if (additional_recipients.get_attribute("value") == "u1@bluecoat.com,u2@bluecoat.com"):
            print "Checkpoint 11: [PASSED] Empty value not saved."
        elif (additional_recipients.get_attribute("value") == ""):
            print "Checkpoint 11: [FAILED] Empty value saved successfully."
            print self.fail("Test case Failed.")
            return 0
                   
#         #### Verify NTD is enabled or not
#           
#         mag2_scanning = self.find_element_by_sizzle("#basic_configuration input[rpcid='mag2_scanning']").get_attribute("checked")
#         if (mag2_scanning):
#             print "->> Mag2 Scanning is already enabled."
#         else:
#             self.find_element_by_sizzle("#basic_configuration input[rpcid='mag2_scanning']").click()
#                
#         relay_dest_ip = self.find_element_by_sizzle("#basic_configuration input[rpcid='relayhost']")
#         relay_dest_ip.clear()
#         relay_dest_ip.send_keys("192.168.0.13")
#            
#         fwd_qtn_mail = self.find_element_by_sizzle("#basic_configuration input[rpcid='quarantine_email']")
#         fwd_qtn_mail.clear()
#         fwd_qtn_mail.send_keys("qtn@test.local")
#            
#         my_networks = self.find_element_by_sizzle("#basic_configuration input[rpcid='my_networks']")
#         my_networks.clear()
#         my_networks.send_keys("192.0.0.0/8")
#            
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         print "->> Basic configuration saved successfully.\n"
#           
#         print "->> New Settings saved are:"
#         a = self.driver.find_element_by_name("enable_mail_scanning").is_selected()
#         b = self.find_element_by_sizzle("#basic_configuration input[rpcid='av_scanning']").is_selected()
#         c = self.find_element_by_sizzle("#basic_configuration input[rpcid='mag2_scanning']").is_selected()
#         d = self.find_element_by_sizzle("#basic_configuration input[rpcid='relayhost']").get_attribute("value")
#         e = self.find_element_by_sizzle("#basic_configuration input[rpcid='quarantine_email']").get_attribute("value")
#         f = self.find_element_by_sizzle("#basic_configuration input[rpcid='my_networks']").get_attribute("value")
#           
#         print "1) Mail Scanning: " + str(a)
#         print "2) AV scanning: " + str(b)
#         print "5) MAG2 scanning: " + str(c)
#         print "1) Relay Destination IP: " + d
#         print "2) Forward Quarantine Mail: " + e
#         print "3) My networks: " + f
         
        
# class B_MailScanning_editbasicconfig(unittest.TestCase):
#     def test_B_editconfig(self):
#         print "\n###### To test editing the Mail Scanning Configuration ######"
#         self.goto_fragment("Network", "Mail Scanning")
#          
#         self.find_element_by_sizzle("#mail_scanning a[tab='basic_configuration']").click()
#         self.find_element_by_sizzle("#basic_configuration input[rpcid='av_scanning']").click()
#         self.find_element_by_sizzle("#basic_configuration input[rpcid='mag2_scanning']").click()
#            
#         relay_dest_ip = self.find_element_by_sizzle("#basic_configuration input[rpcid='relayhost']")
#         relay_dest_ip.clear()
#         relay_dest_ip.send_keys("192.168.0.20")
#            
#         fwd_qtn_mail = self.find_element_by_sizzle("#basic_configuration input[rpcid='quarantine_email']")
#         fwd_qtn_mail.clear()
#         fwd_qtn_mail.send_keys("editqtn@test.local")
#            
#         my_networks = self.find_element_by_sizzle("#basic_configuration input[rpcid='my_networks']")
#         my_networks.clear()
#         my_networks.send_keys("10.0.0.0/8")
#            
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         print "->> Basic configuration edited and saved successfully.\n"
#          
#         print "->> Settings after editing are:"
#         b = self.find_element_by_sizzle("#basic_configuration input[rpcid='av_scanning']").is_selected()
#         c = self.find_element_by_sizzle("#basic_configuration input[rpcid='mag2_scanning']").is_selected()
#         d = self.find_element_by_sizzle("#basic_configuration input[rpcid='relayhost']").get_attribute("value")
#         e = self.find_element_by_sizzle("#basic_configuration input[rpcid='quarantine_email']").get_attribute("value")
#         f = self.find_element_by_sizzle("#basic_configuration input[rpcid='my_networks']").get_attribute("value")
#          
#         print "1) AV scanning: " + str(b)
#         print "2) MAG2 scanning: " + str(c)
#         print "3) Relay Destination IP: " + d
#         print "4) Forward Quarantine Mail: " + e
#         print "5) My networks: " + f
#    
# class C_MailScanning_invalidvalues(unittest.TestCase):
#     def test_C_invalidvalues(self):
#         print "\n###### To test the behavior by putting invalid values ######"
#         self.goto_fragment("Network", "Mail Scanning")
#         self.find_element_by_sizzle("#mail_scanning a[tab='basic_configuration']").click()
#            
#         ### Test invalid values for fiels "Relay Destination IP"
#         print "->>> TEST RELAY DESTINATION IP for invalid values"
#         relay_dest_ip = self.find_element_by_sizzle("#basic_configuration input[rpcid='relayhost']")
#            
#         relay_dest_ip.clear()
#         relay_dest_ip.send_keys("  ") # Enter White Space only
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#            
#         relay_dest_ip.clear()
#         relay_dest_ip.send_keys("") # Enter nothing
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#            
#         relay_dest_ip.clear()
#         relay_dest_ip.send_keys("256.567.345.123") # Enter an invalid IP address value
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#            
#         relay_dest_ip.clear()
#         relay_dest_ip.send_keys("1222.2334.5668.7890") # Enter an invalid IP address value
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#            
#         relay_dest_ip.clear()
#         relay_dest_ip.send_keys("  10.10.10.10  ") # Enter white spaces before and after a valid IP address
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#            
#         #### Test invalid values quarantined mail ####
#         fwd_qtn_mail = self.find_element_by_sizzle("#basic_configuration input[rpcid='quarantine_email']")
#            
#         fwd_qtn_mail.clear()
#         fwd_qtn_mail.send_keys("qtn") #### Enter an email address without mentioning its domain name.
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#            
#         fwd_qtn_mail.clear()
#         fwd_qtn_mail.send_keys("   whitespace@test.local   ") #### Enter a valid email adress with white-space present before and after.
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#            
#         ## Test invalid values for my networks #####
#         my_networks = self.find_element_by_sizzle("#basic_configuration input[rpcid='my_networks']")
#            
#         my_networks.clear()
#         my_networks.send_keys("") ### Enter nothing
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#            
#         my_networks.clear()
#         my_networks.send_keys("   ") ### Enter white-space only
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#            
#         my_networks.clear()
#         my_networks.send_keys("   192.168.0.0/8  ") ### Enter white-space before/after a valid value
#         self.find_element_by_sizzle("#basic_configuration button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#           
#          
#     ## TEST EMAIL CONFIGURATIONS ######
# class D_EmailNotifications(unittest.TestCase):
#     def test_A_emailnotificaton(self):
#         print "\n######  To test email Notification configuration ######"
#         self.goto_fragment("Network", "Mail Scanning")
#         self.find_element_by_sizzle("#mail_scanning a[tab='email_notifications']").click()
#           
#         email_notification = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_enabled']").get_attribute("checked")
#         if (email_notification):
#             print "->> Email notification already enabled."
#         else:
#             self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_enabled']").click()
#         time.sleep(1)
#           
#         sub_line_pre = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_subject_line']")
#         sub_line_pre.clear()
#         sub_line_pre.send_keys("Blocked by ICSP.")
#         time.sleep(1)
#           
#         msg_body_pre = self.find_element_by_sizzle("#email_notifications textarea[rpcid='user_notification_body']")
#         msg_body_pre.clear()
#         msg_body_pre.send_keys("Email Blocked by ICSP. Please contact your administrator.")
#         time.sleep(1)
#           
#         sender_address = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_sender_address']")
#         sender_address.clear()
#         sender_address.send_keys("notification@norman.com")
#         time.sleep(1)
#           
#         replyto_address = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_reply_to_address']")
#         replyto_address.clear()
#         replyto_address.send_keys("notification@norman.com")
#         time.sleep(1)
#           
#         additional_recipients = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_additional_recipients']")
#         additional_recipients.clear()
#         additional_recipients.send_keys("u1@test.local,u2@test.local,u3@test.local")
#         time.sleep(1)
#           
#         exclude_recipients = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_skip_original_recipients']").get_attribute("checked")
#         if (exclude_recipients):
#             print "->> Exclude Recipients option already enabled."
#         else:
#             self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_skip_original_recipients']").click()
#         time.sleep(1)
#           
#           
#         self.find_element_by_sizzle("#email_notifications button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#           
#         print "\n->> New Settings saved are:"
#         f = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_enabled']").is_selected()
#         a = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_subject_line']").get_attribute('value')
#         b = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_sender_address']").get_attribute('value')
#         c = self.find_element_by_sizzle("#email_notifications textarea[rpcid='user_notification_body']").get_attribute('value')
#         d = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_reply_to_address']").get_attribute('value')
#         e = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_additional_recipients']").get_attribute('value')
#           
#         print "1) Email Notifications enabled: " + str(f)
#         print "2) Subject Line Prepend: " + a
#         print "3) Sender Address: " + b
#         print "4) Message Body prepend: " + c
#         print "5) Reply to address: " + d
#         print "6) Additional Recipients: " + e
#       
#      ### Edit Email Configuration #####
#     def test_B_editconfig(self):
#         print "\n###### To test editing of saved configuration ######"
#         self.goto_fragment("Network", "Mail Scanning")
#         self.find_element_by_sizzle("#mail_scanning a[tab='email_notifications']").click()
#            
#         sub_line_pre = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_subject_line']")
#         sub_line_pre.clear()
#         sub_line_pre.send_keys("Edit Subject Line Prepend.")
#         time.sleep(1)
#            
#         msg_body_pre = self.find_element_by_sizzle("#email_notifications textarea[rpcid='user_notification_body']")
#         msg_body_pre.clear()
#         msg_body_pre.send_keys("Edit Email Blocked by ICSP. Please contact your administrator.")
#         time.sleep(1)
#            
#         sender_address = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_sender_address']")
#         sender_address.clear()
#         sender_address.send_keys("editnotification@norman.com")
#         time.sleep(1)
#            
#         replyto_address = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_reply_to_address']")
#         replyto_address.clear()
#         replyto_address.send_keys("editnotification@norman.com")
#         time.sleep(1)
#            
#         additional_recipients = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_additional_recipients']")
#         additional_recipients.clear()
#         additional_recipients.send_keys("editu1@test.local,editu2@test.local,editu3@test.local")
#         time.sleep(1)
#            
#         self.find_element_by_sizzle("#email_notifications button[class='btn btn-primary save_configuration']").click()
#         time.sleep(1)
#           
#         print "\n->> New Settings after editing are:"
#         a = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_subject_line']").get_attribute('value')
#         b = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_sender_address']").get_attribute('value')
#         c = self.find_element_by_sizzle("#email_notifications textarea[rpcid='user_notification_body']").get_attribute('value')
#         d = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_reply_to_address']").get_attribute('value')
#         e = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_additional_recipients']").get_attribute('value')
#           
#         print "1) Subject Line Prepend: " + a
#         print "2) Sender Address: " + b
#         print "3) Message Body prepend: " + c
#         print "4) Reply to address: " + d
#         print "5) Additional Recipients: " + e
#         
# #     def test_c_invalidvalues(self):
# #         print "\n###### To test invalid values ######"
# #         self.goto_fragment("Network", "Mail Scanning")
# #         self.find_element_by_sizzle("#mail_scanning a[tab='email_notifications']").click()
# #         
# #         sender_address = self.find_element_by_sizzle("#email_notifications input[rpcid='user_notification_sender_address']")
# #         sender_address.clear()
# #         sender_address.send_keys("") #### Do not put anything in sender address field
# #         self.find_element_by_sizzle("#email_notifications button[class='btn btn-primary save_configuration']").click()
# #         
# #         b = self.driver.find_element_by_class_name("notifications top-right top_add_margin")
# #         print b.text
        

    def tearDown(self):
        do_logout(self)
        self.driver.close()
# def usage():
#         print "NNP UI integration test"
#         print "These tests require a live NNP that has been installed. Without a completed wizard."
#         print "\tusage: ./remote_access.py [remote_ip]\n"
# 
# if __name__ == '__main__':
#     if len(sys.argv) == 1:
#         usage()
#         exit(1)
#     unittest.main(argv=[sys.argv[0]])
