import unittest, pprint, time, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.support.ui import Select



def do_logout(self):
    self.driver.get(self.nnp_ip)

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
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Blocking"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Blocking' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Blocking").click()
    
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Custom URL Blocking"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Custom URL Blocking' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Custom URL Blocking").click()
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"custom_block_url_list")))
    except:
        print "Checkpoint 3: [FAILED] Custom URL Blocking page not loaded."
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 3: [PASSED] Navigated to 'Custom URL Blocking' page successfully."

class CusotmURLBlocking(unittest.TestCase):
    nnp_ip = "https://192.168.3.241"  
    
    def setUp(self):
        self.driver =webdriver.Firefox()
    
    def test_A_patterns(self):
        print "\n>> #### TC1 - ADD Exact Pattern."
        do_login(self)
        b=self.driver
        if (b.find_element_by_id("custom_url_block_t_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("custom_url_block_t_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="custom_url_blocking"]/div[2]/div/div[1]/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_id("custom_url_select_all").click()
                b.find_element_by_id("custom_url_block_del").click()
        
        url_block_pattern = b.find_element_by_name("pattern")
        url_block_pattern.clear()
        url_block_pattern.send_keys("http://www.google.com")
        comments = b.find_element_by_name("comments")
        comments.clear()
        comments.send_keys("Exact Pattern")
        b.find_element_by_id("add_custom_block").click() ## Click on Add button
        time.sleep(2)
        if (b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr/td[1]').text == "http://www.google.com"):
            print "Checkpoint 4: [PASSED] Exact pattern added successfully."
        else:
            print "Checkpoint 4: [FAILED] Exact pattern not added."
            print self.fail("Test case Failed.")
            return 0
        
        ####################################################
        print "\n>> #### TC2 - Add Prefix pattern."
        url_block_pattern.clear()
        url_block_pattern.send_keys("http://prefix.com")
        b.find_element_by_xpath('//*[@id="new_custom_url"]/div[3]/div/select/option[2]').click()
        comments.clear()
        comments.send_keys("Prefix Pattern")
        b.find_element_by_id("add_custom_block").click() ## Click on Add button
        time.sleep(2)
        if (b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr/td[1]').text == "http://prefix.com"):
            print "Checkpoint 5: [PASSED] Prefix pattern added successfully."
        else:
            print "Checkpoint 5: [FAILED] Prefix pattern not added."
            print self.fail("Test case Failed.")
            return 0
    
        ####################################################
        print "\n>> #### TC3 - Add Postfix pattern."
        url_block_pattern.clear()
        url_block_pattern.send_keys(".pdf")
        b.find_element_by_xpath('//*[@id="new_custom_url"]/div[3]/div/select/option[3]').click()
        comments.clear()
        comments.send_keys("Postfix Pattern")
        b.find_element_by_id("add_custom_block").click() ## Click on Add button
        time.sleep(2)
        if (b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr/td[1]').text == ".pdf"):
            print "Checkpoint 6: [PASSED] Postfix pattern added successfully."
        else:
            print "Checkpoint 6: [FAILED] Postfix pattern not added."
            print self.fail("Test case Failed.")
            return 0
    
        ####################################################
        print "\n>> #### TC4 - Add Wildcard pattern."
        url_block_pattern.clear()
        url_block_pattern.send_keys("http://go?gle*")
        b.find_element_by_xpath('//*[@id="new_custom_url"]/div[3]/div/select/option[4]').click()
        comments.clear()
        comments.send_keys("Wildcard Pattern")
        b.find_element_by_id("add_custom_block").click() ## Click on Add button
        time.sleep(2)
        if (b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr[2]/td[1]').text == "http://go?gle*"):
            print "Checkpoint 7: [PASSED] Wildcard pattern added successfully."
        else:
            print "Checkpoint 7: [FAILED] Wildcard pattern not added."
            print self.fail("Test case Failed.")
            return 0
        ##################################################
        print "\n>> #### TC5 - Testing Deselect all functionality."
        b.find_element_by_xpath('//*[@id="custom_url_blocking"]/div[2]/div/div[1]/a').click() ## Click on Action
        time.sleep(1)
        b.find_element_by_id("custom_url_select_all").click()
        time.sleep(1) 
        if (b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr[1]').get_attribute("class") == "odd row_selected"):
            b.find_element_by_xpath('//*[@id="custom_url_blocking"]/div[2]/div/div[1]/a').click() ## Click on Action
            b.find_element_by_id("custom_url_deselect_all").click()
            if (b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr[1]').get_attribute("class") == "odd"):
                print "Checkpoint 8: [PASSED] Deselect all function working as expected."
            else:
                print "Checkpoint 8: [FAILED] Deselect all function not working as expected."
                print self.fail("Test Case Failed.")
                return 0
                  
        else:
            print "Checkpoint 8: [FAILED] Cannot test deselect since select all is not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ################################################
        print "\n>> #### TC6 - Testing Inverse selection functionality."
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="custom_url_blocking"]/div[2]/div/div[1]/a').click() ## Click on Action
        b.find_element_by_id("custom_url_inverse").click()
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr[1]').get_attribute("class") == "odd row_selected"):
            print "Checkpoint 9: [PASSED] Inverse Selection function working as expected."
        else:
            print "Checkpoint 9: [FAILED] Inverse Selection function not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ##################################################
        print "\n>> #### TC7 - Testing search functionality."
        time.sleep(1)
        search = b.find_element_by_xpath('//*[@id="custom_url_block_t_filter"]/label/input')
        search.clear()
        search.send_keys("wild")
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr/td[1]').text == "http://go?gle*"):
            print "Checkpoint 10: [PASSED] Searching working fine."
        else:
            print "Checkpoint 10: [FAILED] Failed to search the expected IP address."
            print self.fail("Test case Failed.")
            return 0
        search.send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE)
        #################################################
        print "\n>> #### TC8 - Testing Sorting based"
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="custom_url_block_t"]/thead/tr/th[1]').click() ## Click on Sort icon
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr[1]/td[1]').text == "http://www.google.com" and b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr[2]/td[1]').text == "http://prefix.com"):
            print "Checkpoint 11: [PASSED] Sorting is working fine."
        else:
            print "Checkpoint 11: [FAILED] Sorting not working."
            print self.fail("Test case Failed.")
            return 0
        ############################################### 
        print "\n>> #### TC9 - Testing of removal of single rule"
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="custom_url_blocking"]/div[2]/div/div[1]/a').click() ## Click on Action
        b.find_element_by_id("custom_url_deselect_all").click()
        b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr[1]/td[1]').click()
        b.find_element_by_id("custom_url_block_del").click()
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="custom_url_block_t"]/tbody/tr[1]/td[1]').text != "http://www.google.com"):
            print "Checkpoint 12: Selected pattern rule removed successfully."
           
        else:
            print "Checkpoint 12: Selected pattern rule not deleted."
            print self.fail("Test case Failed.")
            return 0
        ##########################################
        print "\n>> #### TC10 - Testing of number of entries shown per page."
        time.sleep(2)
        print ">> Adding 10 more rules"
        for x in range (1,11):
            url_block_pattern.clear()
            time.sleep(1)
            url_block_pattern.send_keys(".exe%d" %(x))
            time.sleep(1)
            b.find_element_by_xpath('//*[@id="new_custom_url"]/div[3]/div/select/option[3]').click()
            time.sleep(1)
            b.find_element_by_id("add_custom_block").click() ## Click on Add button
            time.sleep(1)
        time.sleep(1)
        if (b.find_element_by_id("custom_url_block_t_info").text == "Showing 1 to 10 of 13 entries"):
            print "Checkpoint 13: [PASSED] Number of entries '10' per page shown successfully."
        else:
            print "Checkpoint 13: [FAILED] Number of entries '10' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ###########################################
        print "\n>> Adding 20 more rules"
        time.sleep(1)
        for x in range (11,31):
            url_block_pattern.clear()
            time.sleep(1)
            url_block_pattern.send_keys(".exe%d" %(x))
            time.sleep(1)
            b.find_element_by_xpath('//*[@id="new_custom_url"]/div[3]/div/select/option[3]').click()
            time.sleep(1)
            b.find_element_by_id("add_custom_block").click() ## Click on Add button
            time.sleep(1)
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="custom_url_block_t_length"]/label/select/option[2]').click()
        time.sleep(1)
        if (b.find_element_by_id("custom_url_block_t_info").text == "Showing 1 to 25 of 33 entries"):
            print "Checkpoint 14: [PASSED] Number of entries '25' per page shown successfully."
        else:
            print "Checkpoint 14: [FAILED] Number of entries '25' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ###########################################
        print "\n>> Adding 20 more rules"
        time.sleep(1)
        for x in range (31,51):
            url_block_pattern.clear()
            time.sleep(1)
            url_block_pattern.send_keys(".exe%d" %(x))
            time.sleep(1)
            b.find_element_by_xpath('//*[@id="new_custom_url"]/div[3]/div/select/option[3]').click()
            time.sleep(1)
            b.find_element_by_id("add_custom_block").click() ## Click on Add button
            time.sleep(1)
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="custom_url_block_t_length"]/label/select/option[3]').click()
        time.sleep(1)
        if (b.find_element_by_id("custom_url_block_t_info").text == "Showing 1 to 50 of 53 entries"):
            print "Checkpoint 15: [PASSED] Number of entries '50' per page shown successfully."
        else:
            print "Checkpoint 15: [FAILED] Number of entries '50' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ###########################################
        print "\n>> Adding 50 more rules"
        time.sleep(1)
        for x in range (51,101):
            url_block_pattern.clear()
            time.sleep(1)
            url_block_pattern.send_keys(".pdf%d" %(x))
            time.sleep(1)
            b.find_element_by_xpath('//*[@id="new_custom_url"]/div[3]/div/select/option[3]').click()
            time.sleep(1)
            b.find_element_by_id("add_custom_block").click() ## Click on Add button
            time.sleep(1)
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="custom_url_block_t_length"]/label/select/option[4]').click()
        time.sleep(1)
        if (b.find_element_by_id("custom_url_block_t_info").text == "Showing 1 to 100 of 103 entries"):
            print "Checkpoint 16: [PASSED] Number of entries '100' per page shown successfully."
        else:
            print "Checkpoint 16: [FAILED] Number of entries '100' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ###########################################
        ##########################################
        print "\n>> #### TC11 - Test Paging"
        time.sleep(2)
        b.find_element_by_id("custom_url_block_t_next").click()
        if (b.find_element_by_id("custom_url_block_t_info").text == "Showing 101 to 103 of 103 entries"):
            print "Checkpoint 17: [PASSED] Paging functionality (Next) working fine."
            b.find_element_by_id("custom_url_block_t_previous").click()
            if (b.find_element_by_id("custom_url_block_t_info").text == "Showing 1 to 100 of 103 entries"):
                print "Checkpoint 17: [PASSED] Paging functionality (Previous) working fine."
                   
        else:
            print "Checkpoint 17: [FAILED] Paging functionality not working as expected."
            print self.fail("Test case Failed.")
            return 0
        ###########################################
        print ">> Deleting all IP addresses using select all button."
        time.sleep(2)
        if (b.find_element_by_id("custom_url_block_t_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("custom_url_block_t_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="custom_url_blocking"]/div[2]/div/div[1]/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_id("custom_url_select_all").click()
                b.find_element_by_id("custom_url_block_del").click()
           
        if (b.find_element_by_id("custom_url_block_t_info").text == "Showing 0 to 0 of 0 entries"):
            print "Checkpoint 18: [PASSED] All pattern rules deleted successfully.."
        else:
            print "Checkpoint 18: [FAILED] Failed to delete all Pattern rules."
            print self.fail("Test Case Failed.")
            return 0
        
    def tearDown(self):
        self.driver.close()