import unittest, pprint, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def do_logout(self):
    self.driver.get(self.nnp_ip+'logout')
    #self.driver.find_element_by_id("userbtn").click()
    #self.driver.find_element_by_link_text("Logout").click()

def do_login(self,driver,webuser,webpassword):
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
    username.send_keys(webuser)
    password = b.find_element_by_name("password")
    password.clear()
    password.send_keys(webpassword)
    b.find_element_by_class_name("btn-primary").click()
     
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "uptime"))
        )
    except:
        print "Checkpoint 2: [FAILED] User not logged in."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 2: [PASSED] User successfully logs in."
    
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Support"))
        )
    except:
        print "Checkpoint 3: [FAILED] Support Link not found."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 3: [PASSED] Support link found."
    b.find_element_by_link_text("Support").click()
    
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Generate diagnostic data"))
        )
    except:
        print "Checkpoint 4: [FAILED] Generate diagnostic data Link not found."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 4: [PASSED] Generate diagnostic data link found."
    b.find_element_by_link_text("Generate diagnostic data").click()
    
    
class diagnosticdata(unittest.TestCase):
    nnp_ip = "https://192.168.3.141/"
    def setUp(self):
        self.driver=webdriver.Firefox()
    
    def test_a_gendata(self):
        print "\n##### To verify that diagnostic data generated or not."
        b=self.driver
        do_login(self,b,"admin","norman")
        try:
            element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "generate_and_send"))
            )
        except:
            print "Checkpoint 5: [FAILED] Generate diagnostic data page not loaded."
            print self.fail("Test Case Failed.")
            return 0
        print "Checkpoint 5: [PASSED] Generate diagnostic data page appears successfully."
        
        print ">>> Entering a new case ID."
        b.find_element_by_xpath('//*[@id="generate_diagnostic_data"]/div/div[1]/div[2]/span/input').clear()
        b.find_element_by_xpath('//*[@id="generate_diagnostic_data"]/div/div[1]/div[2]/span/input').send_keys("1234")
        time.sleep(1)
        
        print ">> Entering the time in seconds to capture."
        b.find_element_by_xpath('//*[@id="generate_diagnostic_data"]/div/div[1]/div[2]/span[2]/input').clear()
        b.find_element_by_xpath('//*[@id="generate_diagnostic_data"]/div/div[1]/div[2]/span[2]/input').send_keys("1")
        
        print "\n>>> Clicking on Generate diagnostic data button."
        b.find_element_by_id("generate_and_send").click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located,((By.ID,"gdd_progress_desc"))
            )
        except:
            print "Checkpoint 6: [FAILED] process of capturing data not started."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        capture_msg = b.find_element_by_id("gdd_progress_desc")
        
        if "Capturing traffic / collecting diagnostic data" in capture_msg.text:
            print "Checkpoint 6: [PASSED] Process of generating diagnostic data has been started."
        else:
            print "Checkpoint 6: [FAILED] Process of generating diagnostics data has not started."
            print self.fail("Case Status: FAILED.")
            return 0
        
        try:
            element = WebDriverWait(b,60).until(EC.presence_of_element_located,((By.ID,"gdd"))
            )
        except:            
            print "Checkpoint 7: [FAILED] Data not uploaded to Bluecoat."
            print self.fail("Case Status: FAILED.")
            return 0
              
        resultmsg = b.find_element_by_id("gdd")
        time.sleep(25)
        
        if "Data uploaded successfully to Blue Coat!" in resultmsg.text:
            print "Checkpoint 7: [PASSED] Data uploaded successfully to BlueCoat."
        else:
            print "hello12"
            print "Checkpoint 7: [FAILED] Data not uploaded to Bluecoat."
            print self.fail("Case Status: FAILED.")
            return 0

        
    def tearDown(self):
        do_logout(self)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
    
