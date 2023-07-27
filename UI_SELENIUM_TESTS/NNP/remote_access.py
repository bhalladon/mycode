import unittest, pprint, time, sys
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
    print "Checkpoint 1: [PASSED] Login page open successfully."
    
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
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Remote Access"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Remote Access' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Remote Access").click()
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"add_acl_rule")))
    except:
        print "Checkpoint 3: [FAILED] Remote access page not loaded."
        return 0
    print "Checkpoint 3: [PASSED] Navigated to page 'Remote Access' successfully."

def do_logout(self):
    self.driver.get(self.nnp_ip+'/logout')
    
class remote_access(unittest.TestCase):
    nnp_ip="https://192.168.3.241/"
    
    def setUp(self):
        self.driver = webdriver.Firefox()
    
        
###### ADD A RULE #####
    
    def test_A_add_rule(self):
        print "####### TC1 - To add a Remote Access Rule."
        b=self.driver
        do_login(self)
        b.find_element_by_id("add_acl_rule").click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"new_ip")))
        except:
            print "Checkpoint 4: [FAILED] Pop-up window for adding a new remote access rule not displayed."
            return 0
        print "Checkpoint 4: [PASSED] Pop-up windows for adding a new rule displayed successfully."
        time.sleep(2)
        b.find_element_by_id("new_ip").clear()
        b.find_element_by_id("new_ip").send_keys("192.168.3.3")
        time.sleep(1)
        b.find_element_by_id("new_netmask").clear()
        b.find_element_by_id("new_netmask").send_keys("255.255.255.255")
        b.find_element_by_name("confirm").click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"add_acl_rule")))
        except:
            print "Checkpoint 5: [FAILED] After adding a rule page not navigated to Remote access page."
            return 0
        print "Checkpoint 5: [PASSED] After adding a rule page navigated to 'Remote Access' successfully."
        time.sleep(2)
        ip = b.find_element_by_xpath("//*[@id='acl_insertion_spot']/div[2]/p[2]").get_attribute("value")
        if ( ip == "192.168.3.3"):
            print "Checkpoint 6: [PASSED] Rule added successfully."
        else:
            print "Checkpoint 6: [FAILED] Rule not added."
            print self.fail("Test Case Failed.")
                 
        ####### ADDING A DUPLICATE RULE ###########
        time.sleep(2)
        print "\n###### TC2 - Adding a duplicate rule.\n"
        b.find_element_by_id("add_acl_rule").click()
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"new_ip")))
        except:
            print "Checkpoint 7: [FAILED] Pop-up window for adding a new remote access rule(duplicate) not displayed."
            return 0
        print "Checkpoint 7: [PASSED] Pop-up windows for adding a new rule(duplicate) displayed successfully."
        time.sleep(2)
        b.find_element_by_id("new_ip").clear()
        b.find_element_by_id("new_ip").send_keys("192.168.3.3")
        time.sleep(1)
        b.find_element_by_id("new_netmask").clear()
        b.find_element_by_id("new_netmask").send_keys("255.255.255.255")
        b.find_element_by_name("confirm").click()
        if ( self.driver.find_element_by_id("duplicate_acl_rule").get_attribute("value")):
            print "Checkpoint 8: [FAILED] Duplicate rule added successfully!"
            print self.fail("Test case Failed.")
        else:
            print "Checkpoint 8: [PASSED] This is a duplicate rule. A rule with same IP and netmask address already exists."
        b.find_element_by_name("cancel").click()
        
#                      
   
    def test_B_delete_rule(self):
        print "\n##### TC3 - Test Deletion of a rule added above"
        b=self.driver
        do_login(self)
        b.find_element_by_css_selector("#acl_insertion_spot > div:nth-child(2) > i").click()
        time.sleep(2)
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME,"confirm")))
        except:
            print "Checkpoint 4: [FAILED] Pop-up window for confirming the deletion of a rule is not displayed."
            print self.fail("Test case Failed.")
            return 0
        print "Checkpoint 4: [PASSED] Pop-up windows for confirming the deletion of a rule displayed successfully."
        b.find_element_by_name("confirm").click()
        time.sleep(2)
                
        try:
            elememt = WebDriverWait(b,4).until_not(EC.presence_of_element_located((By.CSS_SELECTOR,"#acl_insertion_spot > div:nth-child(2) > i")))
        except:
            print "Checkpoint 5: [FAILED] Rule not deleted successfully."
            print self.fail("Test case Failed.")
            return 0
        print "Checkpoint 5: [PASSED] Rule deleted successfully."
          
          
   
####### ADD MULTIPLE RULES ######
   
    def test_C_multiple_rules(self):
        print "\n###### TC4 - Adding multiple rules."
        b=self.driver
        do_login(self)
        for k in range(0,9):
            b.find_element_by_id("add_acl_rule").click()
            time.sleep(1)
            b.find_element_by_id("new_ip").clear()
            b.find_element_by_id("new_ip").send_keys("192.168.3.%d" % (k))
            b.find_element_by_id("new_netmask").clear()
            b.find_element_by_id("new_netmask").send_keys("255.255.255.255")
            b.find_element_by_name("confirm").click()
            time.sleep(1)
        print "Multiple rules Added Successfully"
        try:
            elememt = WebDriverWait(b,4).until(EC.presence_of_element_located((By.NAME,"10"))
            )
        except:
            print "Checkpoint 4: [FAILED] All Rules not added successfully."
            print self.fail("Test Case Failed.")
            return 0
        print "Checkpoint 4: [PASSED] All rules added successfully."   
          
          
######## Delete Multiple Rules Added Above ########
    def test_D_multiple_rules_deleted(self):
        print "\n##### TC5 - Deleting Multiple rules added above."
        b=self.driver
        do_login(self)
        for k in range(0,9):
            time.sleep(1)
            b.find_element_by_css_selector("#acl_insertion_spot > div:nth-child(2) > i").click()
            time.sleep(1)
            self.driver.find_element_by_name("confirm").click()
        try:
            elememt = WebDriverWait(b,4).until(EC.presence_of_element_located((By.CSS_SELECTOR,"acl_insertion_spot > div:nth-child(2) > i"))
            )
        except:
            print "Checkpoint 4: [PASSED] All Rules deleted successfully."
            return 0
        print "Checkpoint 4: [FAILED] All rules not deleted successfully." 
        print self.fail("Test case Failed.") 
           
         
    
    def tearDown(self):
        do_logout(self)
        self.driver.close()
        
if __name__ == '__main__':
    unittest.main()
