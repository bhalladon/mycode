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
    b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
        )
    except:
        print "Checkpoint 4: [FAILED] Protocol Settings page not loaded."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 4: [PASSED] Navigated to Protocol Settings page."
     
class Protocolsettings(unittest.TestCase):
    
    nnp_ip = "https://192.168.3.241/"
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_A_http(self):
        print "\n>> #### TC1 - Configure HTTP"
        do_login(self)
        b=self.driver
        #### Setting to full scan mode #####
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]')
        fullscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 5: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 5: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]')
        
        if (fullscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 5: [PASSED] HTTP Protocol successfully set to Full Scan mode."
        else:
            print "Checkpoint 5: [FAILED] HTTP protocol not set to Full Scan mode."
            print self.fail("Test Case Failed.")
            return 0
        
        #### Setting HTTP to Quick scan mode #####
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[3]')
        quickscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 6: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 6: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[3]')
        
        if (quickscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 6: [PASSED] HTTP Protocol successfully set to Quick Scan mode."
        else:
            print "Checkpoint 6: [FAILED] HTTP protocol not set to Quick Scan mode."
            print self.fail("Test Case Failed.")
            return 0
    
        #### Setting HTTP to Block scan mode #####
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[2]')
        blockscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 7: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 7: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[2]')
        
        if (blockscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 7: [PASSED] HTTP Protocol successfully set to Block mode."
        else:
            print "Checkpoint 7: [FAILED] HTTP protocol not set to Block mode."
            print self.fail("Test Case Failed.")
            return 0

        #### Setting HTTP to Bypass mode #####
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[1]')
        bypass.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 8: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 8: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[1]')
        
        if (bypass.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 8: [PASSED] HTTP Protocol successfully set to Bypass mode."
        else:
            print "Checkpoint 8: [FAILED] HTTP protocol not set to Bypass mode."
            print self.fail("Test Case Failed.")
            return 0
        
    def test_B_IMAP4(self):
        print "\n>> #### TC2 - Configure IMAP4"
        do_login(self)
        b=self.driver
        #### Setting to full scan mode #####
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[3]/td[2]/div/button[4]')
        fullscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 5: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 5: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[3]/td[2]/div/button[4]')
        
        if (fullscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 5: [PASSED] IMAP4 Protocol successfully set to Full Scan mode."
        else:
            print "Checkpoint 5: [FAILED] IMAP4 protocol not set to Full Scan mode."
            print self.fail("Test Case Failed.")
            return 0
        
        #### Setting HTTP to Quick scan mode #####
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[3]/td[2]/div/button[3]')
        quickscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 6: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 6: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[3]/td[2]/div/button[3]')
        
        if (quickscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 6: [PASSED] IMAP4 Protocol successfully set to Quick Scan mode."
        else:
            print "Checkpoint 6: [FAILED] IMAP4 protocol not set to Quick Scan mode."
            print self.fail("Test Case Failed.")
            return 0
    
        #### Setting HTTP to Block scan mode #####
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[3]/td[2]/div/button[2]')
        blockscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 7: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 7: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[3]/td[2]/div/button[2]')
        
        if (blockscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 7: [PASSED] IMAP4 Protocol successfully set to Block mode."
        else:
            print "Checkpoint 7: [FAILED] IMAP4 protocol not set to Block mode."
            print self.fail("Test Case Failed.")
            return 0

        #### Setting HTTP to Bypass mode #####
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[3]/td[2]/div/button[1]')
        bypass.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 8: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 8: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[3]/td[2]/div/button[1]')
        
        if (bypass.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 8: [PASSED] IMAP4 Protocol successfully set to Bypass mode."
        else:
            print "Checkpoint 8: [FAILED] IMAP4 protocol not set to Bypass mode."
            print self.fail("Test Case Failed.")
            return 0

    def test_C_TFTP(self):
        print "\n>> #### TC3 - Configure TFTP"
        do_login(self)
        b=self.driver
        #### Setting to full scan mode #####
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[4]/td[2]/div/button[4]')
        fullscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 5: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 5: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[4]/td[2]/div/button[4]')
        
        if (fullscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 5: [PASSED] TFTP Protocol successfully set to Full Scan mode."
        else:
            print "Checkpoint 5: [FAILED] TFTP protocol not set to Full Scan mode."
            print self.fail("Test Case Failed.")
            return 0
        
        #### Setting HTTP to Quick scan mode #####
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[4]/td[2]/div/button[3]')
        quickscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 6: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 6: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[4]/td[2]/div/button[3]')
        
        if (quickscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 6: [PASSED] TFTP Protocol successfully set to Quick Scan mode."
        else:
            print "Checkpoint 6: [FAILED] TFTP protocol not set to Quick Scan mode."
            print self.fail("Test Case Failed.")
            return 0
    
        #### Setting HTTP to Block scan mode #####
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[4]/td[2]/div/button[2]')
        blockscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 7: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 7: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[4]/td[2]/div/button[2]')
        
        if (blockscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 7: [PASSED] TFTP Protocol successfully set to Block mode."
        else:
            print "Checkpoint 7: [FAILED] TFTP protocol not set to Block mode."
            print self.fail("Test Case Failed.")
            return 0

        #### Setting HTTP to Bypass mode #####
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[4]/td[2]/div/button[1]')
        bypass.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 8: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 8: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[4]/td[2]/div/button[1]')
        
        if (bypass.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 8: [PASSED] TFTP Protocol successfully set to Bypass mode."
        else:
            print "Checkpoint 8: [FAILED] TFTP protocol not set to Bypass mode."
            print self.fail("Test Case Failed.")
            return 0

    def test_D_SMTP(self):
        print "\n>> #### TC4 - Configure SMTP"
        do_login(self)
        b=self.driver
        #### Setting to full scan mode #####
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[5]/td[2]/div/button[4]')
        fullscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 5: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 5: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[5]/td[2]/div/button[4]')
        
        if (fullscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 5: [PASSED] SMTP Protocol successfully set to Full Scan mode."
        else:
            print "Checkpoint 5: [FAILED] SMTP protocol not set to Full Scan mode."
            print self.fail("Test Case Failed.")
            return 0
        
        #### Setting HTTP to Quick scan mode #####
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[5]/td[2]/div/button[3]')
        quickscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 6: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 6: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[5]/td[2]/div/button[3]')
        
        if (quickscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 6: [PASSED] SMTP Protocol successfully set to Quick Scan mode."
        else:
            print "Checkpoint 6: [FAILED] SMTP protocol not set to Quick Scan mode."
            print self.fail("Test Case Failed.")
            return 0
    
        #### Setting HTTP to Block scan mode #####
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[5]/td[2]/div/button[2]')
        blockscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 7: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 7: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[5]/td[2]/div/button[2]')
        
        if (blockscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 7: [PASSED] SMTP Protocol successfully set to Block mode."
        else:
            print "Checkpoint 7: [FAILED] SMTP protocol not set to Block mode."
            print self.fail("Test Case Failed.")
            return 0

        #### Setting HTTP to Bypass mode #####
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[5]/td[2]/div/button[1]')
        bypass.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 8: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 8: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[5]/td[2]/div/button[1]')
        
        if (bypass.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 8: [PASSED] SMTP Protocol successfully set to Bypass mode."
        else:
            print "Checkpoint 8: [FAILED] SMTP protocol not set to Bypass mode."
            print self.fail("Test Case Failed.")
            return 0

    def test_E_POP3(self):
        print "\n>> #### TC5 - Configure POP3"
        do_login(self)
        b=self.driver
        #### Setting to full scan mode #####
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[6]/td[2]/div/button[4]')
        fullscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 5: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 5: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[6]/td[2]/div/button[4]')
        
        if (fullscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 5: [PASSED] POP3 Protocol successfully set to Full Scan mode."
        else:
            print "Checkpoint 5: [FAILED] POP3 protocol not set to Full Scan mode."
            print self.fail("Test Case Failed.")
            return 0
        
        #### Setting HTTP to Quick scan mode #####
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[6]/td[2]/div/button[3]')
        quickscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 6: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 6: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[6]/td[2]/div/button[3]')
        
        if (quickscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 6: [PASSED] POP3 Protocol successfully set to Quick Scan mode."
        else:
            print "Checkpoint 6: [FAILED] POP3 protocol not set to Quick Scan mode."
            print self.fail("Test Case Failed.")
            return 0
    
        #### Setting HTTP to Block scan mode #####
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[6]/td[2]/div/button[2]')
        blockscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 7: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 7: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[6]/td[2]/div/button[2]')
        
        if (blockscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 7: [PASSED] POP3 Protocol successfully set to Block mode."
        else:
            print "Checkpoint 7: [FAILED] POP3 protocol not set to Block mode."
            print self.fail("Test Case Failed.")
            return 0

        #### Setting HTTP to Bypass mode #####
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[6]/td[2]/div/button[1]')
        bypass.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 8: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 8: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[6]/td[2]/div/button[1]')
        
        if (bypass.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 8: [PASSED] POP3 Protocol successfully set to Bypass mode."
        else:
            print "Checkpoint 8: [FAILED] POP3 protocol not set to Bypass mode."
            print self.fail("Test Case Failed.")
            return 0
    def test_F_FTP(self):
        print "\n>> #### TC6 - Configure FTP"
        do_login(self)
        b=self.driver
        #### Setting to full scan mode #####
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[7]/td[2]/div/button[4]')
        fullscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 5: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 5: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[7]/td[2]/div/button[4]')
        
        if (fullscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 5: [PASSED] FTP Protocol successfully set to Full Scan mode."
        else:
            print "Checkpoint 5: [FAILED] FTP protocol not set to Full Scan mode."
            print self.fail("Test Case Failed.")
            return 0
        
        #### Setting HTTP to Quick scan mode #####
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[7]/td[2]/div/button[3]')
        quickscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 6: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 6: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[7]/td[2]/div/button[3]')
        
        if (quickscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 6: [PASSED] FTP Protocol successfully set to Quick Scan mode."
        else:
            print "Checkpoint 6: [FAILED] FTP protocol not set to Quick Scan mode."
            print self.fail("Test Case Failed.")
            return 0
    
        #### Setting HTTP to Block scan mode #####
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[7]/td[2]/div/button[2]')
        blockscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 7: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 7: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[7]/td[2]/div/button[2]')
        
        if (blockscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 7: [PASSED] FTP Protocol successfully set to Block mode."
        else:
            print "Checkpoint 7: [FAILED] FTP protocol not set to Block mode."
            print self.fail("Test Case Failed.")
            return 0

        #### Setting HTTP to Bypass mode #####
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[7]/td[2]/div/button[1]')
        bypass.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 8: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 8: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[7]/td[2]/div/button[1]')
        
        if (bypass.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 8: [PASSED] FTP Protocol successfully set to Bypass mode."
        else:
            print "Checkpoint 8: [FAILED] FTP protocol not set to Bypass mode."
            print self.fail("Test Case Failed.")
            return 0
        
    def test_G_TFTP(self):
        print "\n>> #### TC7 - Configure TFTP"
        do_login(self)
        b=self.driver
        #### Setting to full scan mode #####
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[8]/td[2]/div/button[4]')
        fullscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 5: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 5: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        fullscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[8]/td[2]/div/button[4]')
        
        if (fullscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 5: [PASSED] TFTP Protocol successfully set to Full Scan mode."
        else:
            print "Checkpoint 5: [FAILED] TFTP protocol not set to Full Scan mode."
            print self.fail("Test Case Failed.")
            return 0
        
        #### Setting HTTP to Quick scan mode #####
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[8]/td[2]/div/button[3]')
        quickscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 6: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 6: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        quickscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[8]/td[2]/div/button[3]')
        
        if (quickscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 6: [PASSED] TFTP Protocol successfully set to Quick Scan mode."
        else:
            print "Checkpoint 6: [FAILED] TFTP protocol not set to Quick Scan mode."
            print self.fail("Test Case Failed.")
            return 0
    
        #### Setting HTTP to Block scan mode #####
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[8]/td[2]/div/button[2]')
        blockscan.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 7: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 7: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        blockscan = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[8]/td[2]/div/button[2]')
        
        if (blockscan.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 7: [PASSED] TFTP Protocol successfully set to Block mode."
        else:
            print "Checkpoint 7: [FAILED] TFTP protocol not set to Block mode."
            print self.fail("Test Case Failed.")
            return 0

        #### Setting HTTP to Bypass mode #####
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[8]/td[2]/div/button[1]')
        bypass.click()
        b.find_element_by_xpath('//*[@id="protocol_settings"]/div/button').click() ## Save Configuration
        b.get(self.nnp_ip+'#nse')
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME, "operation_mode"))
            )
        except:
            print "Checkpoint 8: [FAILED] Scanner Engine page not loaded after reloading the page."
            print self.fail("Case Status: FAILED.")
            return 0
        b.find_element_by_xpath('//*[@id="nse"]/div[1]/div/ul/li[2]/a').click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="protocol_settings_protocols"]/table/tbody/tr[2]/td[2]/div/button[4]'))
            )
        except:
            print "Checkpoint 8: [FAILED] Protocol Settings page not loaded after reloading."
            print self.fail("Test Case Failed.")
            return 0
        bypass = b.find_element_by_xpath('//*[@id="protocol_settings_protocols"]/table/tbody/tr[8]/td[2]/div/button[1]')
        
        if (bypass.get_attribute("class") == "btn btn-primary"):
            print "Checkpoint 8: [PASSED] TFTP Protocol successfully set to Bypass mode."
        else:
            print "Checkpoint 8: [FAILED] TFTP protocol not set to Bypass mode."
            print self.fail("Test Case Failed.")
            return 0

    def tearDown(self):
        do_logout(self)
        self.driver.close()