import unittest, pprint, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.common.exceptions import NoSuchElementException


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
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Network Threat Discovery"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Network Threat Discovery' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Network Threat Discovery").click() ## CLick on "Network Threat Discovery"
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"mag2config_part")))
    except:
        print "Checkpoint 3: [FAILED] Network Threat Discovery page not loaded."
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 3: [PASSED] Navigated to 'Network Threat Discovery' page successfully."
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located,((By.XPATH, '//*[@id="mag2proxy_part"]/div/span[2]/label'))
        )
    except:
        print "Checkpoint 4: [FAILED] Proxy settings page not loaded."
        print self.fail("Test case Failed.")
        return 0
    b.find_element_by_xpath('//*[@id="ntd"]/div/div[1]/ul/li[2]/a').click() ## Click on "Proxy settings"
    print "Checkpoint 4: [PASSED] Navigated to NTD proxy settings page."
    
class Mailscanning(unittest.TestCase):
    nnp_ip = "https://192.168.3.241/"
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        
    def test_A_proxy(self):
        print "\n>> #### TC1 - Configure proxy settings"
        do_login(self)
        b=self.driver
        use_proxy_server = b.find_element_by_xpath('//*[@id="mag2proxy_part"]/div/span[1]/input')
        if (use_proxy_server.get_attribute("checked")):
            pass
        else:
            use_proxy_server.click()
        
        proxy_address = b.find_element_by_xpath('//*[@id="mag2proxy_part"]/div/span[2]/input')
        proxy_address.clear()
        proxy_address.send_keys("192.168.3.35")
        
        proxy_server_port = b.find_element_by_xpath('//*[@id="mag2proxy_part"]/div/span[3]/input')
        proxy_server_port.clear()
        proxy_server_port.send_keys("3128")
        
        b.find_element_by_xpath('//*[@id="mag2proxy_part"]/div/button').click() ## Saving configuration
        time.sleep(2)
        
        if (use_proxy_server.is_selected() == True):
            print "Checkpoint 5: [PASSED] Proxy enabled successfully."
        else:
            print "Checkpoint 5: [FAILED] Failed to enable proxy."
            print self.fail("Test Case Failed.")
            return 0
        
        if (proxy_address.get_attribute("value") == "192.168.3.35"):
            print "Checkpoint 6: [PASSED] Proxy address saved with expected value successfully."
        else:
            print "Checkpoint 6: [FAILED] Proxy address not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0
        
        if (proxy_server_port.get_attribute("value") == "3128"):
            print "Checkpoint 7: [PASSED] Proxy server port saved with expected value successfully."
        else:
            print "Checkpoint 7: [FAILED] Proxy server port not saved with expected value."
            print self.fail("Test Case Failed.")
            return 0
        
        print "\n>> #### TC2 - Configure proxy authentication."
        proxy_auth = b.find_element_by_xpath('//*[@id="mag2proxy_part"]/div/span[4]/input')
        if (proxy_auth.get_attribute("checked")):
            pass
        else:
            proxy_auth.click()
        
        proxy_username = b.find_element_by_xpath('//*[@id="mag2proxy_part"]/div/span[5]/input')
        proxy_username.clear()
        proxy_username.send_keys("bluecoat")
        
        proxy_password = b.find_element_by_xpath('//*[@id="mag2proxy_part"]/div/span[6]/input')
        proxy_password.clear()
        proxy_password.send_keys("password")
        
        windows_nt_domain = b.find_element_by_xpath('//*[@id="mag2proxy_part"]/div/span[7]/input')
        windows_nt_domain.clear()
        windows_nt_domain.send_keys("proxy.local")
        
        b.find_element_by_xpath('//*[@id="mag2proxy_part"]/div/button').click() ## Saving configuration
        time.sleep(2)
        
        if (proxy_auth.is_selected() == True):
            print "Checkpoint 8: [PASSED] Proxy authentication enabled successfully."
        else:
            print "Checkpoint 8: [FAILED] Failed to enable proxy authentication."
            print self.fail("Test Case Failed.")
            return 0
    
        if (proxy_username.get_attribute("value") == "bluecoat"):
            print "Checkpoint 9: [PASSED] Proxy username successfully saved with expected value."
        else:
            print "Checkpoint 9: [FAILED] Proxy username not saved with expected value."
            print self.fail("Test case Failed.")
            return 0
        
        if (proxy_password.get_attribute("value") == "password"):
            print "Checkpoint 10: [PASSED] Proxy password successfully saved with expected value."
        else:
            print "Checkpoint 10: [FAILED] Proxy password not saved with expected value."
            print self.fail("Test case Failed.")
            return 0
        
        if (windows_nt_domain.get_attribute("value") == "proxy.local"):
            print "Checkpoint 11: [PASSED] Windows NT Domain name successfully saved with expected value."
        else:
            print "Checkpoint 11: [FAILED] Windows NT Domain name not saved with expected value."
            print self.fail("Test case Failed.")
            return 0
        
        #### Disable Proxy Server
        use_proxy_server.click()
        b.find_element_by_xpath('//*[@id="mag2proxy_part"]/div/button').click() ## Saving configuration
        time.sleep(2)
        
    def tearDown(self):
        do_logout(self)
        self.driver.close()