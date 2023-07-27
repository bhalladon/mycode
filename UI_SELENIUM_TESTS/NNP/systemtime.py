from selenium import webdriver
import unittest, time, sys
#from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

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
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "System Time"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'System Time' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("System Time").click()
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"date")))
    except:
        print "Checkpoint 3: [FAILED] System Time page not loaded."
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 3: [PASSED] Navigated to 'System Time' page successfully."
    
class systemtime(unittest.TestCase):
    
    nnp_ip = "https://192.168.3.241/"
    
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_a_systemtime(self):
        print "\n##### TC1 - Verify system time settings."
        do_login(self)
        b=self.driver
        time.sleep(1)
        print "\n## Verify the presence of Clock."
        if (str(b.find_element_by_id("highcharts-10").is_displayed() == True)):
            print "Checkpoint 4: [PASSED] Clock displayed successfully."
        else:
            print "Checkpoint 4 [FAILED] Clock not displayed."
            print self.fail("Case Status: FAILED.")
            return 0
          
        time.sleep(1)
        print "\n## Setting time zone one from each continent"
        ### African Continent
        b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').send_keys(Keys.HOME)
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="system_time"]/div[2]/div/button').click()
        if (str(b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').get_attribute("value") == "Africa/Abidjan")):
            print 'Checkpoint 5: [PASSED] Timezone successfully set to "Africa/Abidjan"'
        else:
            print 'Checkpoint 5: [FAILED] Timezone not set as "Africa/Abidjan"'
            print self.fail("Case Status: FAILED")
            return 0
        time.sleep(1)
         
        ####Setting America - America/Adak
        b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').send_keys(Keys.PAGE_DOWN + Keys.PAGE_DOWN + Keys.PAGE_DOWN)
        time.sleep(1)
        element = b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select')
        select = Select(element)
        select.select_by_visible_text("America/Adak")
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="system_time"]/div[2]/div/button').click()
        if (str(b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').get_attribute("value") == "America/Adak")):
            print 'Checkpoint 6: [PASSED] Timezone successfully set to "America/Adak"'
        else:
            print 'Checkpoint 6: [FAILED] Timezone not set as "America/Adak"'
            print self.fail("Case Status: FAILED")
            return 0
        time.sleep(1)
         
        #### Setting Antartica/Casey
        b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').send_keys(Keys.PAGE_DOWN + Keys.PAGE_DOWN + Keys.PAGE_DOWN + Keys.PAGE_DOWN + Keys.PAGE_DOWN + Keys.PAGE_DOWN + Keys.PAGE_DOWN)
        time.sleep(1)
        element = b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select')
        select = Select(element)
        select.select_by_visible_text("Antarctica/Casey")
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="system_time"]/div[2]/div/button').click()
        if (str(b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').get_attribute("value") == "Antarctica/Casey")):
            print 'Checkpoint 7: [PASSED] Timezone successfully set to "Antarctica/Casey"'
        else:
            print 'Checkpoint 7: [FAILED] Timezone not set as "Antarctica/Casey"'
            print self.fail("Case Status: FAILED")
            return 0
        time.sleep(1)
          
        #### Setting Asia/Aden
        b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        element = b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select')
        select = Select(element)
        select.select_by_visible_text("Asia/Aden")
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="system_time"]/div[2]/div/button').click()
        if (str(b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').get_attribute("value") == "Asia/Aden")):
            print 'Checkpoint 8: [PASSED] Timezone successfully set to "Asia/Aden"'
        else:
            print 'Checkpoint 8: [FAILED] Timezone not set as "Asia/Aden"'
            print self.fail("Case Status: FAILED")
            return 0
        time.sleep(1)
            
        ### Setting Atlantic/Azores
        b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').send_keys(Keys.PAGE_DOWN + Keys.PAGE_DOWN + Keys.PAGE_DOWN + Keys.PAGE_DOWN)
        time.sleep(1)
        element = b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select')
        select = Select(element)
        select.select_by_visible_text("Atlantic/Azores")
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="system_time"]/div[2]/div/button').click()
        if (str(b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').get_attribute("value") == "Atlantic/Azores")):
            print 'Checkpoint 9: [PASSED] Timezone successfully set to "Atlantic/Azores"'
        else:
            print 'Checkpoint 9: [FAILED] Timezone not set as "Atlantic/Azores"'
            print self.fail("Case Status: FAILED")
            return 0
        time.sleep(1)
            
        ### Setting Australia/Adelaide
        b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        element = b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select')
        select = Select(element)
        select.select_by_visible_text("Australia/Adelaide")
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="system_time"]/div[2]/div/button').click()
        if (str(b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').get_attribute("value") == "Australia/Adelaide")):
            print 'Checkpoint 10: [PASSED] Timezone successfully set to "Australia/Adelaide"'
        else:
            print 'Checkpoint 10: [FAILED] Timezone not set as "Australia/Adelaide"'
            print self.fail("Case Status: FAILED")
            return 0
        time.sleep(1)
            
        ### Setting Europe/Amsterdam
        b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        element = b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select')
        select = Select(element)
        select.select_by_visible_text("Europe/Amsterdam")
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="system_time"]/div[2]/div/button').click()
        if (str(b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').get_attribute("value") == "Europe/Amsterdam")):
            print 'Checkpoint 11: [PASSED] Timezone successfully set to "Europe/Amsterdam"'
        else:
            print 'Checkpoint 11: [FAILED] Timezone not set as "Europe/Amsterdam"'
            print self.fail("Case Status: FAILED")
            return 0
        time.sleep(1)
            
        ### Setting Indian/Antananarivo
        b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').send_keys(Keys.PAGE_DOWN + Keys.PAGE_DOWN + Keys.PAGE_DOWN)
        time.sleep(1)
        element = b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select')
        select = Select(element)
        select.select_by_visible_text("Indian/Antananarivo")
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="system_time"]/div[2]/div/button').click()
        if (str(b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').get_attribute("value") == "Indian/Antananarivo")):
            print 'Checkpoint 12: [PASSED] Timezone successfully set to "Indian/Antananarivo"'
        else:
            print 'Checkpoint 12: [FAILED] Timezone not set as "Indian/Antananarivo"'
            print self.fail("Case Status: FAILED")
            return 0
        time.sleep(1)
            
        ### Setting Pacific/Apia
        b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        element = b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select')
        select = Select(element)
        select.select_by_visible_text("Pacific/Apia")
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="system_time"]/div[2]/div/button').click()
        if (str(b.find_element_by_xpath('//*[@id="system_time"]/div[1]/div/div/div/div[1]/span/select').get_attribute("value") == "Pacific/Apia")):
            print 'Checkpoint 13: [PASSED] Timezone successfully set to "Pacific/Apia"'
        else:
            print 'Checkpoint 13: [FAILED] Timezone not set as "Pacific/Apia"'
            print self.fail("Case Status: FAILED")
            return 0
        time.sleep(1)
        
        print "\n## Verify if NTP usage enabled then manually adjusting time should be disabled and NTP server input text box is also disabled."
        ntp = b.find_element_by_name("ntp_enabled")
        date = b.find_element_by_id("date")
        hour = b.find_element_by_id("hour")
        minute = b.find_element_by_id("minute")
        second = b.find_element_by_id("seconds")
        ntp_server = b.find_element_by_name("ntp_server")
        if (ntp.is_selected() == True):
            if (date.is_enabled() == False):
                print "Checkpoint 14: [PASSED] Date input text box is disabled when NTP is enabled."
            else:
                print "Checkpoint 14: [FAILED] Date input text box is enabled when NTP is enabled."
                print self.fail("Case Status: FAILED.")
                return 0
            time.sleep(1)
            if (hour.is_enabled() == False):
                print "Checkpoint 15: [PASSED] Hour input text box is disabled when NTP is enabled."
            else:
                print "Checkpoint 15: [FAILED] Hour input text box is enabled when NTP is enabled."
                print self.fail("Case Status: FAILED.")
                return 0
            time.sleep(1)
            if (minute.is_enabled() == False):
                print "Checkpoint 16: [PASSED] Minute input text box is disabled when NTP is enabled."
            else:
                print "Checkpoint 16: [FAILED] Minute input text box is enabled when NTP is enabled."
                print self.fail("Case Status: FAILED.")
                return 0
            time.sleep(1)
            if (second.is_enabled() == False):
                print "Checkpoint 17: [PASSED] Seconds input text box is disabled when NTP is enabled."
            else:
                print "Checkpoint 17: [FAILED] Seconds input text box is enabled when NTP is enabled."
                print self.fail("Case Status: FAILED.")
                return 0
            time.sleep(1)
            if (ntp_server.is_enabled() == False):
                print "Checkpoint 18: [PASSED] NTP Server input text box is disabled when NTP is enabled."
            else:
                print "Checkpoint 18: [FAILED] NTP Server input text box is enabled when NTP is enabled."
                print self.fail("Case Status: FAILED.")
                return 0
        
        else:
            ntp.click()
            if (date.is_enabled() == False):
                print "Checkpoint 14: [PASSED] Date input text box is disabled when NTP is enabled."
            else:
                print "Checkpoint 14: [FAILED] Date input text box is enabled when NTP is enabled."
                print self.fail("Case Status: FAILED.")
                return 0
            time.sleep(1)
            if (hour.is_enabled() == False):
                print "Checkpoint 15: [PASSED] Hour input text box is disabled when NTP is enabled."
            else:
                print "Checkpoint 15: [FAILED] Hour input text box is enabled when NTP is enabled."
                print self.fail("Case Status: FAILED.")
                return 0
            time.sleep(1)
            if (minute.is_enabled() == False):
                print "Checkpoint 16: [PASSED] Minute input text box is disabled when NTP is enabled."
            else:
                print "Checkpoint 16: [FAILED] Minute input text box is enabled when NTP is enabled."
                print self.fail("Case Status: FAILED.")
                return 0
            time.sleep(1)
            if (second.is_enabled() == False):
                print "Checkpoint 17: [PASSED] Seconds input text box is disabled when NTP is enabled."
            else:
                print "Checkpoint 17: [FAILED] Seconds input text box is enabled when NTP is enabled."
                print self.fail("Case Status: FAILED.")
                return 0
            time.sleep(1)
            if (ntp_server.is_enabled() == False):
                print "Checkpoint 18: [PASSED] NTP Server input text box is disabled when NTP is enabled."
            else:
                print "Checkpoint 18: [FAILED] NTP Server input text box is enabled when NTP is enabled."
                print self.fail("Case Status: FAILED.")
                return 0
        
        print "\n### Enable NTP"
        print "## Input NTP server as 'NULL' to check if it gets saved or not."
        if (ntp.is_selected() == False):
            ntp.click()
            ntp_server.clear()
            b.find_element_by_xpath('//*[@id="system_time"]/div[2]/div/button').click()
            print "hello"
            b.refresh()
            time.sleep(2)
            try:
                element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME,"test_ntp"))
                )
            except:
                print "Checkpoint 18: [FAILED] System Time page not loaded."
                return 0
            ntp = b.find_element_by_name("ntp_enabled").is_enabled()
            if (ntp == True):
                print "Checkpoint 18: [FAILED] Null value saved as NTP server."
                print self.fail("Case Status: FAILED.")
                return 0
            else:
                print "Checkpoint 18: [PASSED] Null value not accepted as NTP server."
        else:
            ntp_server.clear()
            b.find_element_by_xpath('//*[@id="system_time"]/div[2]/div/button').click()
            b.refresh()
            time.sleep(2)
            try:
                element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME,"test_ntp"))
                )
            except:
                print "Checkpoint 18: [FAILED] System Time page not loaded."
                return 0
            ntp = b.find_element_by_name("ntp_enabled").is_enabled()
            if (ntp == True):
                print "Checkpoint 18: [FAILED] Null value saved as NTP server."
                print self.fail("Case Status: FAILED.")
                return 0
            else:
                print "Checkpoint 18: [PASSED] Null value not accepted as NTP server."
            
        print "\n## Test NTP server connection should not work in case if user does not provide any ntp server."
        ntp = b.find_element_by_name("ntp_enabled").is_selected()
        if (ntp == True):
            ntp_server.clear()
            b.find_element_by_name("test_ntp").click()
            if (str(b.find_element_by_id("ntp_bad").is_displayed() == True)):
                print "Checkpoint 19: [PASSED] A cross(X) icon is displayed successfully on testing ntp connection without providing a ntp server."
            else:
                print "Checkpoint 19: [FAILED] Trying to test the connection with NTP server even though no NTP server is given."
                print self.fail("Case Status: FAILED.")
                return 0
        else:
            ntp.click()
            ntp_server.clear()
            b.find_element_by_name("test_ntp").click()
            if (str(b.find_element_by_id("ntp_bad").is_displayed() == True)):
                print "Checkpoint 19: [PASSED] A cross(X) icon is displayed successfully on testing ntp connection without providing a ntp server."
            else:
                print "Checkpoint 19: [FAILED] Trying to test the connection with NTP server even though no NTP server is given."
                print self.fail("Case Status: FAILED.")
                return 0    
           
    def tearDown(self):
        do_logout(self)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
