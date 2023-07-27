import unittest, time 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from wheel.signatures import assertTrue
#from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.support.ui import Select

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
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Blocking"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Blocking' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Blocking").click()
    
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Block and Exclude Lists"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Block and Exclude Lists' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Block and Exclude Lists").click()
    
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"ip_block")))
    except:
        print "Checkpoint 3: [FAILED] Block and Exclude Lists page not loaded."
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 3: [PASSED] Navigated to 'Block and Exclude Lists' page successfully."
    
class BlockExclude(unittest.TestCase):
    nnp_ip = "https://192.168.3.241/"
    
    def setUp(self):
        self.driver = webdriver.Firefox()
    
    def test_A_IPBlock(self):
        print "\n>> #### TC1 - Configure IP Block List"
        do_login(self)
        b=self.driver
        b.find_element_by_xpath('//*[@id="block_exclude"]/div/div[1]/ul/li[1]/a').click() ### Clicking on IP Block list
        time.sleep(1)
        if (b.find_element_by_id("block_ip_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("block_ip_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="ip_block"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_name("select_all").click()
                b.find_element_by_name("rem_entry").click()
          
        add_ip = b.find_element_by_xpath('//*[@id="ip_block"]/form/fieldset/div/input')
        add_ip.clear()
        print ">> Adding a single IP address.."
        add_ip.send_keys("1.2.3.4") ## Add a single IP
        b.find_element_by_name("add").click()
        time.sleep(1)
        added_ip = b.find_element_by_xpath('//*[@id="block_ip"]/tbody/tr/td')
        if (added_ip.text == "1.2.3.4"):
            print "Checkpoint 4: [PASSED] Single IP address added successfully."
        else:
            print "Checkpoint 4: [FAILED] IP address not added."
            print self.fail("Test case Failed.")
            return 0
        ##################################################
        print ">> Testing Deselect all functionality."
        b.find_element_by_xpath('//*[@id="ip_block"]/form/fieldset/div/div/a').click() ## Click on Action
        time.sleep(1)
        b.find_element_by_name("select_all").click()
        time.sleep(1) 
        if (b.find_element_by_xpath('//*[@id="block_ip"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            b.find_element_by_xpath('//*[@id="ip_block"]/form/fieldset/div/div/a').click()
            b.find_element_by_name("deselect_all").click()
            if (b.find_element_by_xpath('//*[@id="block_ip"]/tbody/tr').get_attribute("class") == "odd"):
                print "Checkpoint 5: [PASSED] Deselect all function working as expected."
            else:
                print "Checkpoint 5: [FAILED] Deselect all function not working as expected."
                print self.fail("Test Case Failed.")
                return 0
                  
        else:
            print "Checkpoint 5: [FAILED] Cannot test deselect since select all is not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ################################################
        print ">> Testing Inverse selection functionality."
        b.find_element_by_xpath('//*[@id="ip_block"]/form/fieldset/div/div/a').click()
        b.find_element_by_name("inverse").click()
        if (b.find_element_by_xpath('//*[@id="block_ip"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            print "Checkpoint 6: [PASSED] Inverse Selection function working as expected."
        else:
            print "Checkpoint 6: [FAILED] Inverse Selection function not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ##################################################
        print ">> Testing search functionality."
        add_ip.clear()
        add_ip.send_keys("5.6.7.8")
        b.find_element_by_name("add").click()
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="block_ip"]/tbody/tr[2]/td').text == "5.6.7.8"):
            search = b.find_element_by_xpath('//*[@id="block_ip_filter"]/label/input')
            search.clear()
            search.send_keys("5.6")
            if (b.find_element_by_xpath('//*[@id="block_ip"]/tbody/tr/td').text == "5.6.7.8"):
                print "Checkpoint 7: [PASSED] Searching working fine."
            else:
                print "Checkpoint 7: [FAILED] Failed to search the expected IP address."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 7: [FAILED] Failed to add another IP address required for searching."
            print self.fail("Test case Failed.")
            return 0
        #################################################
        print ">> Testing Sorting based on IP address"
        search.send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE)
           
        b.find_element_by_xpath('//*[@id="block_ip"]/thead/tr/th').click() ## Click on Sort icon
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="block_ip"]/tbody/tr/td').text == "5.6.7.8" and b.find_element_by_xpath('//*[@id="block_ip"]/tbody/tr[2]/td').text == "1.2.3.4"):
            print "Checkpoint 8: [PASSED] Sorting is working fine."
        else:
            print "Checkpoint 8: [FAILED] Sorting not working."
            print self.fail("Test case Failed.")
            return 0
        ############################################### 
        print ">> Testing of removal of single IP address"
        b.find_element_by_xpath('//*[@id="block_ip"]/tbody/tr/td').click()
        b.find_element_by_name("rem_entry").click()
        time.sleep(1)
           
        if (b.find_element_by_xpath('//*[@id="block_ip"]/tbody/tr/td').text == "1.2.3.4"):
            print "Checkpoint 9: Selected IP address removed successfully."
           
        elif (b.find_element_by_xpath('//*[@id="block_ip"]/tbody/tr/td').text == "5.6.7.8"):
            print "Checkpoint 9: Selected IP address not deleted."
            print self.fail("Test case Failed.")
            return 0
        ##########################################
        print ">> Testing of number of entries shown per page."
        print ">> Adding 10 more IP addresses"
        for x in range (1,11):
            add_ip.clear()
            add_ip.send_keys("2.3.4.%d" %(x))
            b.find_element_by_name("add").click()
        time.sleep(2)
        if (b.find_element_by_id("block_ip_info").text == "Showing 1 to 10 of 11 entries"):
            print "Checkpoint 10: [PASSED] Number of entries '10' per page shown successfully."
        else:
            print "Checkpoint 10: [FAILED] Number of entries '10' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ###########################################
        print ">> Adding 20 more IP addresses"
        for x in range (11,31):
            add_ip.clear()
            add_ip.send_keys("2.3.4.%d" %(x))
            b.find_element_by_name("add").click()
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="block_ip_length"]/label/select/option[2]').click()
        time.sleep(1)
        if (b.find_element_by_id("block_ip_info").text == "Showing 1 to 25 of 31 entries"):
            print "Checkpoint 11: [PASSED] Number of entries '25' per page shown successfully."
        else:
            print "Checkpoint 11: [FAILED] Number of entries '25' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 20 more IP addresses"
        for x in range (31,51):
            add_ip.clear()
            add_ip.send_keys("2.3.4.%d" %(x))
            b.find_element_by_name("add").click()
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="block_ip_length"]/label/select/option[3]').click()
        if (b.find_element_by_id("block_ip_info").text == "Showing 1 to 50 of 51 entries"):
            print "Checkpoint 12: [PASSED] Number of entries '50' per page shown successfully."
        else:
            print "Checkpoint 12: [FAILED] Number of entries '50' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 50 more IP addresses"
        for x in range (51,101):
            add_ip.clear()
            add_ip.send_keys("2.3.4.%d" %(x))
            b.find_element_by_name("add").click()
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="block_ip_length"]/label/select/option[4]').click()
        if (b.find_element_by_id("block_ip_info").text == "Showing 1 to 100 of 101 entries"):
            print "Checkpoint 13: [PASSED] Number of entries '100' per page shown successfully."
        else:
            print "Checkpoint 13: [FAILED] Number of entries '100' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Test Paging"
        time.sleep(2)
        b.find_element_by_id("block_ip_next").click()
        if (b.find_element_by_id("block_ip_info").text == "Showing 101 to 101 of 101 entries"):
            print "Checkpoint 14: [PASSED] Paging functionality (Next) working fine."
            b.find_element_by_id("block_ip_previous").click()
            if (b.find_element_by_id("block_ip_info").text == "Showing 1 to 100 of 101 entries"):
                print "Checkpoint 15: [PASSED] Paging functionality (Previous) working fine."
                   
        else:
            print "Checkpoint 14: [FAILED] Paging functionality not working as expected."
            print self.fail("Test case Failed.")
            return 0
        ###########################################
        print ">> Deleting all IP addresses using select all button."
        time.sleep(2)
        if (b.find_element_by_id("block_ip_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("block_ip_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="ip_block"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_name("select_all").click()
                b.find_element_by_name("rem_entry").click()
           
        if (b.find_element_by_id("block_ip_info").text == "Showing 0 to 0 of 0 entries"):
            print "Checkpoint 16: [PASSED] All IP addresses deleted successfully.."
        else:
            print "Checkpoint 16: [FAILED] Failed to delete all IP addresses."
            print self.fail("Test Case Failed.")
            return 0
         
    def test_B_IPExclude(self):
        print "\n\n>> #### TC2 - Configure IP Exclude List"
        do_login(self)
        b=self.driver
        b.find_element_by_xpath('//*[@id="block_exclude"]/div/div[1]/ul/li[2]/a').click() ### Clicking on IP Excluce list
        time.sleep(1)
        if (b.find_element_by_id("exclude_ip_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("exclude_ip_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/div/ul/li[1]/a').click()
                #b.find_element_by_name("select_all").click()
                b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/button[2]').click()
                #b.find_element_by_name("rem_entry").click()
         
        add_ip = b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/input')
        add_ip.clear()
        print ">> Adding a single IP address.."
        add_ip.send_keys("1.2.3.4") ## Add a single IP
        b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        #b.find_element_by_name("add").click()
         
        time.sleep(1)
        added_ip = b.find_element_by_xpath('//*[@id="exclude_ip"]/tbody/tr/td')
        if (added_ip.text == "1.2.3.4"):
            print "Checkpoint 4: [PASSED] Single IP address added successfully."
        else:
            print "Checkpoint 4: [FAILED] IP address not added."
            print self.fail("Test case Failed.")
            return 0
        ##################################################
        print ">> Testing Deselect all functionality."
        b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/div/ul/li[1]/a').click() ## CLick on Select all
        #b.find_element_by_name("select_all").click()
        time.sleep(1) 
        if (b.find_element_by_xpath('//*[@id="exclude_ip"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
            b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/div/ul/li[2]/a').click() ## Click on Deselect all
            #b.find_element_by_name("deselect_all").click()
            if (b.find_element_by_xpath('//*[@id="exclude_ip"]/tbody/tr').get_attribute("class") == "odd"):
                print "Checkpoint 5: [PASSED] Deselect all function working as expected."
            else:
                print "Checkpoint 5: [FAILED] Deselect all function not working as expected."
                print self.fail("Test Case Failed.")
                return 0
                 
        else:
            print "Checkpoint 5: [FAILED] Cannot test deselect since select all is not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ################################################
        print ">> Testing Inverse selection functionality."
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
        b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/div/ul/li[3]/a').click() ## Click on Inverse selection
        if (b.find_element_by_xpath('//*[@id="exclude_ip"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            print "Checkpoint 6: [PASSED] Inverse Selection function working as expected."
        else:
            print "Checkpoint 6: [FAILED] Inverse Selection function not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ##################################################
        print ">> Testing search functionality."
        add_ip.clear()
        add_ip.send_keys("5.6.7.8")
        b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="exclude_ip"]/tbody/tr[2]/td').text == "5.6.7.8"):
            search = b.find_element_by_xpath('//*[@id="exclude_ip_filter"]/label/input')
            search.clear()
            search.send_keys("5.6")
            if (b.find_element_by_xpath('//*[@id="exclude_ip"]/tbody/tr/td').text == "5.6.7.8"):
                print "Checkpoint 7: [PASSED] Searching working fine."
            else:
                print "Checkpoint 7: [FAILED] Failed to search the expected IP address."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 7: [FAILED] Failed to add another IP address required for searching."
            print self.fail("Test case Failed.")
            return 0
        #################################################
        print ">> Testing Sorting based on IP address"
        search.send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE)
           
        b.find_element_by_xpath('//*[@id="exclude_ip"]/thead/tr/th').click() ## Click on Sort icon
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="exclude_ip"]/tbody/tr/td').text == "5.6.7.8" and b.find_element_by_xpath('//*[@id="exclude_ip"]/tbody/tr[2]/td').text == "1.2.3.4"):
            print "Checkpoint 8: [PASSED] Sorting is working fine."
        else:
            print "Checkpoint 8: [FAILED] Sorting not working."
            print self.fail("Test case Failed.")
            return 0
        ############################################### 
        print ">> Testing of removal of single IP address"
        b.find_element_by_xpath('//*[@id="exclude_ip"]/tbody/tr/td').click()
        b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/button[2]').click()
        time.sleep(1)
           
        if (b.find_element_by_xpath('//*[@id="exclude_ip"]/tbody/tr/td').text == "1.2.3.4"):
            print "Checkpoint 9: Selected IP address removed successfully."
           
        elif (b.find_element_by_xpath('//*[@id="exclude_ip"]/tbody/tr/td').text == "5.6.7.8"):
            print "Checkpoint 9: Selected IP address not deleted."
            print self.fail("Test case Failed.")
            return 0
        ##########################################
        print ">> Testing of number of entries shown per page."
        print ">> Adding 10 more IP addresses"
        for x in range (1,11):
            add_ip.clear()
            add_ip.send_keys("2.3.4.%d" %(x))
            b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)
        if (b.find_element_by_id("exclude_ip_info").text == "Showing 1 to 10 of 11 entries"):
            print "Checkpoint 10: [PASSED] Number of entries '10' per page shown successfully."
        else:
            print "Checkpoint 10: [FAILED] Number of entries '10' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ###########################################
        print ">> Adding 20 more IP addresses"
        for x in range (11,31):
            add_ip.clear()
            add_ip.send_keys("2.3.4.%d" %(x))
            b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="exclude_ip_length"]/label/select/option[2]').click()
        if (b.find_element_by_id("exclude_ip_info").text == "Showing 1 to 25 of 31 entries"):
            print "Checkpoint 11: [PASSED] Number of entries '25' per page shown successfully."
        else:
            print "Checkpoint 11: [FAILED] Number of entries '25' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 20 more IP addresses"
        for x in range (31,51):
            add_ip.clear()
            add_ip.send_keys("2.3.4.%d" %(x))
            b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="exclude_ip_length"]/label/select/option[3]').click()
        if (b.find_element_by_id("exclude_ip_info").text == "Showing 1 to 50 of 51 entries"):
            print "Checkpoint 12: [PASSED] Number of entries '50' per page shown successfully."
        else:
            print "Checkpoint 12: [FAILED] Number of entries '50' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 50 more IP addresses"
        for x in range (51,101):
            add_ip.clear()
            add_ip.send_keys("2.3.4.%d" %(x))
            b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="exclude_ip_length"]/label/select/option[4]').click()
        if (b.find_element_by_id("exclude_ip_info").text == "Showing 1 to 100 of 101 entries"):
            print "Checkpoint 13: [PASSED] Number of entries '100' per page shown successfully."
        else:
            print "Checkpoint 13: [FAILED] Number of entries '100' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Test Paging"
        time.sleep(2)
        b.find_element_by_id("exclude_ip_next").click()
        if (b.find_element_by_id("exclude_ip_info").text == "Showing 101 to 101 of 101 entries"):
            print "Checkpoint 14: [PASSED] Paging functionality (Next) working fine."
            b.find_element_by_id("exclude_ip_previous").click()
            if (b.find_element_by_id("exclude_ip_info").text == "Showing 1 to 100 of 101 entries"):
                print "Checkpoint 15: [PASSED] Paging functionality (Previous) working fine."
                   
        else:
            print "Checkpoint 14: [FAILED] Paging functionality not working as expected."
            print self.fail("Test case Failed.")
            return 0
        ###########################################
        print ">> Deleting all IP addresses using select all button."
        time.sleep(2)
        if (b.find_element_by_id("exclude_ip_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("exclude_ip_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/div/ul/li[1]/a').click()
                b.find_element_by_xpath('//*[@id="ip_exclude"]/form/fieldset/div/button[2]').click()
           
        if (b.find_element_by_id("exclude_ip_info").text == "Showing 0 to 0 of 0 entries"):
            print "Checkpoint 16: [PASSED] All IP addresses deleted successfully.."
        else:
            print "Checkpoint 16: [FAILED] Failed to delete all IP addresses."
            print self.fail("Test Case Failed.")
            return 0

    def test_C_MacBlock(self):
        print "\n\n>> #### TC3 - Configure Mac Block List"
        do_login(self)
        b=self.driver
        b.find_element_by_xpath('//*[@id="block_exclude"]/div/div[1]/ul/li[3]/a').click() ### Clicking on Mac Block list
        time.sleep(1)
        if (b.find_element_by_id("blocked_mac_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("blocked_mac_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/div/ul/li[1]/a').click()
                #b.find_element_by_name("select_all").click()
                b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/button[2]').click()
                #b.find_element_by_name("rem_entry").click()
          
        add_mac = b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/input')
        add_mac.clear()
        print ">> Adding a single MAC address.."
        add_mac.send_keys("01-50-56-C0-00-08") ## Add a single IP
        b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        #b.find_element_by_name("add").click()
          
        time.sleep(1)
        added_mac = b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr/td')
        if (added_mac.text == "01-50-56-C0-00-08"):
            print "Checkpoint 4: [PASSED] Single MAC address added successfully."
        else:
            print "Checkpoint 4: [FAILED] MAC address not added."
            print self.fail("Test case Failed.")
            return 0
        ##################################################
        print ">> Testing Deselect all functionality."
        b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/div/a').click() ## Click on Action
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/div/ul/li[1]/a').click() ## CLick on Select all
         
        if (b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/div/a').click() ## Click on Action
            b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/div/ul/li[2]/a').click() ## Click on Deselect all
            #b.find_element_by_name("deselect_all").click()
            if (b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr').get_attribute("class") == "odd"):
                print "Checkpoint 5: [PASSED] Deselect all function working as expected."
            else:
                print "Checkpoint 5: [FAILED] Deselect all function not working as expected."
                print self.fail("Test Case Failed.")
                return 0
                  
        else:
            print "Checkpoint 5: [FAILED] Cannot test deselect since select all is not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ################################################
        print ">> Testing Inverse selection functionality."
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/div/a').click() ## Click on Action
        b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/div/ul/li[3]/a').click() ## Click on Inverse selection
        if (b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            print "Checkpoint 6: [PASSED] Inverse Selection function working as expected."
        else:
            print "Checkpoint 6: [FAILED] Inverse Selection function not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ##################################################
        print ">> Testing search functionality."
        add_mac.clear()
        add_mac.send_keys("01-51-56-C0-00-08")
        b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr[2]/td').text == "01-51-56-C0-00-08"):
            search = b.find_element_by_xpath('//*[@id="blocked_mac_filter"]/label/input')
            search.clear()
            search.send_keys("51")
            if (b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr/td').text == "01-51-56-C0-00-08"):
                print "Checkpoint 7: [PASSED] Searching working fine."
            else:
                print "Checkpoint 7: [FAILED] Failed to search the expected MAC address."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 7: [FAILED] Failed to add another MAC address required for searching."
            print self.fail("Test case Failed.")
            return 0
        #################################################
        print ">> Testing Sorting based on MAC address"
        search.send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE)
            
        b.find_element_by_xpath('//*[@id="blocked_mac"]/thead/tr/th').click() ## Click on Sort icon
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr/td').text == "01-51-56-C0-00-08" and b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr[2]/td').text == "01-50-56-C0-00-08"):
            print "Checkpoint 8: [PASSED] Sorting is working fine."
        else:
            print "Checkpoint 8: [FAILED] Sorting not working."
            print self.fail("Test case Failed.")
            return 0
        ############################################### 
        print ">> Testing of removal of single MAC address"
        b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr/td').click()
        b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/button[2]').click()
        time.sleep(1)
            
        if (b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr/td').text == "01-50-56-C0-00-08"):
            print "Checkpoint 9: Selected IP address removed successfully."
            
        elif (b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr/td').text == "01-51-56-C0-00-08"):
            print "Checkpoint 9: Selected IP address not deleted."
            print self.fail("Test case Failed.")
            return 0
        ##########################################
        print ">> Testing of number of entries shown per page."
        print ">> Adding 10 more MAC addresses"
        for x in range (1,10):
            add_mac.clear()
            add_mac.send_keys("0%d-52-56-C0-00-08" %(x))
            b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        add_mac.clear()
        add_mac.send_keys("10-52-56-C0-00-08")
        b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)
        if (b.find_element_by_id("blocked_mac_info").text == "Showing 1 to 10 of 11 entries"):
            print "Checkpoint 10: [PASSED] Number of entries '10' per page shown successfully."
        else:
            print "Checkpoint 10: [FAILED] Number of entries '10' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ###########################################
        print ">> Adding 20 more MAC addresses"
        for x in range (11,31):
            add_mac.clear()
            add_mac.send_keys("%d-52-56-C0-00-08" %(x))
            b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="blocked_mac_length"]/label/select/option[2]').click()
        if (b.find_element_by_id("blocked_mac_info").text == "Showing 1 to 25 of 31 entries"):
            print "Checkpoint 11: [PASSED] Number of entries '25' per page shown successfully."
        else:
            print "Checkpoint 11: [FAILED] Number of entries '25' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 20 more MAC addresses"
        for x in range (31,51):
            add_mac.clear()
            add_mac.send_keys("%d-52-56-C0-00-08" %(x))
            b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="blocked_mac_length"]/label/select/option[3]').click()
        if (b.find_element_by_id("blocked_mac_info").text == "Showing 1 to 50 of 51 entries"):
            print "Checkpoint 12: [PASSED] Number of entries '50' per page shown successfully."
        else:
            print "Checkpoint 12: [FAILED] Number of entries '50' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 50 more MAC addresses"
        for x in range (51,100):
            add_mac.clear()
            add_mac.send_keys("%d-52-56-C0-00-08" %(x))
            b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        add_mac.clear()
        add_mac.send_keys("01-53-56-C0-00-08")
        b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="blocked_mac_length"]/label/select/option[4]').click()
        if (b.find_element_by_id("blocked_mac_info").text == "Showing 1 to 100 of 101 entries"):
            print "Checkpoint 13: [PASSED] Number of entries '100' per page shown successfully."
        else:
            print "Checkpoint 13: [FAILED] Number of entries '100' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Test Paging"
        time.sleep(2)
        b.find_element_by_id("blocked_mac_next").click()
        if (b.find_element_by_id("blocked_mac_info").text == "Showing 101 to 101 of 101 entries"):
            print "Checkpoint 14: [PASSED] Paging functionality (Next) working fine."
            b.find_element_by_id("blocked_mac_previous").click()
            if (b.find_element_by_id("blocked_mac_info").text == "Showing 1 to 100 of 101 entries"):
                print "Checkpoint 15: [PASSED] Paging functionality (Previous) working fine."
                    
        else:
            print "Checkpoint 14: [FAILED] Paging functionality not working as expected."
            print self.fail("Test case Failed.")
            return 0
#         ###########################################
        print ">> Deleting all MAC addresses using select all button."
        time.sleep(2)
        if (b.find_element_by_id("blocked_mac_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("blocked_mac_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/div/ul/li[1]/a').click()
                b.find_element_by_xpath('//*[@id="mac_block"]/form/fieldset/div/button[2]').click()
            
        if (b.find_element_by_id("blocked_mac_info").text == "Showing 0 to 0 of 0 entries"):
            print "Checkpoint 16: [PASSED] All MAC addresses deleted successfully.."
        else:
            print "Checkpoint 16: [FAILED] Failed to delete all MAC addresses."
            print self.fail("Test Case Failed.")
            return 0

    def test_D_MacBlock(self):
        print "\n\n>> #### TC4 - Configure Mac Exclude List"
        do_login(self)
        b=self.driver
        b.find_element_by_xpath('//*[@id="block_exclude"]/div/div[1]/ul/li[4]/a').click() ### Clicking on Mac Block list
        time.sleep(1)
        if (b.find_element_by_id("exclude_mac_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("exclude_mac_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/div/ul/li[1]/a').click()
                #b.find_element_by_name("select_all").click()
                b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/button[2]').click()
                #b.find_element_by_name("rem_entry").click()
          
        add_mac = b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/input')
        add_mac.clear()
        print ">> Adding a single MAC address.."
        add_mac.send_keys("01-50-56-C0-00-08") ## Add a single IP
        b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        #b.find_element_by_name("add").click()
          
        time.sleep(1)
        added_mac = b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr/td')
        if (added_mac.text == "01-50-56-C0-00-08"):
            print "Checkpoint 4: [PASSED] Single MAC address added successfully."
        else:
            print "Checkpoint 4: [FAILED] MAC address not added."
            print self.fail("Test case Failed.")
            return 0
        ##################################################
        print ">> Testing Deselect all functionality."
        b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/div/ul/li[1]/a').click() ## CLick on Select all
         
        if (b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
            b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/div/ul/li[2]/a').click() ## Click on Deselect all
            #b.find_element_by_name("deselect_all").click()
            if (b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr').get_attribute("class") == "odd"):
                print "Checkpoint 5: [PASSED] Deselect all function working as expected."
            else:
                print "Checkpoint 5: [FAILED] Deselect all function not working as expected."
                print self.fail("Test Case Failed.")
                return 0
                  
        else:
            print "Checkpoint 5: [FAILED] Cannot test deselect since select all is not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ################################################
        print ">> Testing Inverse selection functionality."
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
        b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/div/ul/li[3]/a').click() ## Click on Inverse selection
        if (b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            print "Checkpoint 6: [PASSED] Inverse Selection function working as expected."
        else:
            print "Checkpoint 6: [FAILED] Inverse Selection function not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ##################################################
        print ">> Testing search functionality."
        add_mac.clear()
        add_mac.send_keys("01-51-56-C0-00-08")
        b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr[2]/td').text == "01-51-56-C0-00-08"):
            search = b.find_element_by_xpath('//*[@id="exclude_mac_filter"]/label/input')
            search.clear()
            search.send_keys("51")
            if (b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr/td').text == "01-51-56-C0-00-08"):
                print "Checkpoint 7: [PASSED] Searching working fine."
            else:
                print "Checkpoint 7: [FAILED] Failed to search the expected MAC address."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 7: [FAILED] Failed to add another MAC address required for searching."
            print self.fail("Test case Failed.")
            return 0
        #################################################
        print ">> Testing Sorting based on MAC address"
        search.send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE)
            
        b.find_element_by_xpath('//*[@id="exclude_mac"]/thead/tr/th').click() ## Click on Sort icon
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr/td').text == "01-51-56-C0-00-08" and b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr[2]/td').text == "01-50-56-C0-00-08"):
            print "Checkpoint 8: [PASSED] Sorting is working fine."
        else:
            print "Checkpoint 8: [FAILED] Sorting not working."
            print self.fail("Test case Failed.")
            return 0
        ############################################### 
        print ">> Testing of removal of single MAC address"
        b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr/td').click()
        b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/button[2]').click()
        time.sleep(1)
            
        if (b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr/td').text == "01-50-56-C0-00-08"):
            print "Checkpoint 9: Selected IP address removed successfully."
            
        elif (b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr/td').text == "01-51-56-C0-00-08"):
            print "Checkpoint 9: Selected IP address not deleted."
            print self.fail("Test case Failed.")
            return 0
        ##########################################
        print ">> Testing of number of entries shown per page."
        print ">> Adding 10 more MAC addresses"
        for x in range (1,10):
            add_mac.clear()
            add_mac.send_keys("0%d-52-56-C0-00-08" %(x))
            b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        add_mac.clear()
        add_mac.send_keys("10-52-56-C0-00-08")
        b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)
        if (b.find_element_by_id("exclude_mac_info").text == "Showing 1 to 10 of 11 entries"):
            print "Checkpoint 10: [PASSED] Number of entries '10' per page shown successfully."
        else:
            print "Checkpoint 10: [FAILED] Number of entries '10' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ###########################################
        print ">> Adding 20 more MAC addresses"
        for x in range (11,31):
            add_mac.clear()
            add_mac.send_keys("%d-52-56-C0-00-08" %(x))
            b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="exclude_mac_length"]/label/select/option[2]').click()
        if (b.find_element_by_id("exclude_mac_info").text == "Showing 1 to 25 of 31 entries"):
            print "Checkpoint 11: [PASSED] Number of entries '25' per page shown successfully."
        else:
            print "Checkpoint 11: [FAILED] Number of entries '25' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 20 more MAC addresses"
        for x in range (31,51):
            add_mac.clear()
            add_mac.send_keys("%d-52-56-C0-00-08" %(x))
            b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="exclude_mac_length"]/label/select/option[3]').click()
        if (b.find_element_by_id("exclude_mac_info").text == "Showing 1 to 50 of 51 entries"):
            print "Checkpoint 12: [PASSED] Number of entries '50' per page shown successfully."
        else:
            print "Checkpoint 12: [FAILED] Number of entries '50' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 50 more MAC addresses"
        for x in range (51,100):
            add_mac.clear()
            add_mac.send_keys("%d-52-56-C0-00-08" %(x))
            b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        add_mac.clear()
        add_mac.send_keys("01-53-56-C0-00-08")
        b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="exclude_mac_length"]/label/select/option[4]').click()
        if (b.find_element_by_id("exclude_mac_info").text == "Showing 1 to 100 of 101 entries"):
            print "Checkpoint 13: [PASSED] Number of entries '100' per page shown successfully."
        else:
            print "Checkpoint 13: [FAILED] Number of entries '100' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Test Paging"
        time.sleep(2)
        b.find_element_by_id("exclude_mac_next").click()
        if (b.find_element_by_id("exclude_mac_info").text == "Showing 101 to 101 of 101 entries"):
            print "Checkpoint 14: [PASSED] Paging functionality (Next) working fine."
            b.find_element_by_id("exclude_mac_previous").click()
            if (b.find_element_by_id("exclude_mac_info").text == "Showing 1 to 100 of 101 entries"):
                print "Checkpoint 15: [PASSED] Paging functionality (Previous) working fine."
                    
        else:
            print "Checkpoint 14: [FAILED] Paging functionality not working as expected."
            print self.fail("Test case Failed.")
            return 0
#         ###########################################
        print ">> Deleting all MAC addresses using select all button."
        time.sleep(2)
        if (b.find_element_by_id("exclude_mac_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("exclude_mac_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/div/ul/li[1]/a').click()
                b.find_element_by_xpath('//*[@id="mac_exclude"]/form/fieldset/div/button[2]').click()
            
        if (b.find_element_by_id("exclude_mac_info").text == "Showing 0 to 0 of 0 entries"):
            print "Checkpoint 16: [PASSED] All MAC addresses deleted successfully.."
        else:
            print "Checkpoint 16: [FAILED] Failed to delete all MAC addresses."
            print self.fail("Test Case Failed.")
            return 0

    def test_E_vlanblock(self):
        print "\n\n>> #### TC5 - Configure Vlan Block List"
        do_login(self)
        b=self.driver
        b.find_element_by_xpath('//*[@id="block_exclude"]/div/div[1]/ul/li[5]/a').click() ### Clicking on Mac Block list
        time.sleep(1)
        if (b.find_element_by_id("blocked_vlan_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("blocked_vlan_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/div/ul/li[1]/a').click()
                #b.find_element_by_name("select_all").click()
                b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/button[2]').click()
                #b.find_element_by_name("rem_entry").click()
           
        add_vlan = b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/input')
        add_vlan.clear()
        print ">> Adding a single Vlan ID.."
        add_vlan.send_keys("1") ## Add a single Vlan ID
        b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        #b.find_element_by_name("add").click()
           
        time.sleep(1)
        added_vlan = b.find_element_by_xpath('//*[@id="blocked_vlan"]/tbody/tr/td')
        if (added_vlan.text == "1"):
            print "Checkpoint 4: [PASSED] Single VLAN ID added successfully."
        else:
            print "Checkpoint 4: [FAILED] VLAN ID not added."
            print self.fail("Test case Failed.")
            return 0
        ##################################################
        print ">> Testing Deselect all functionality."
        b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/div/a').click() ## Click on Action
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/div/ul/li[1]/a').click() ## CLick on Select all
          
        if (b.find_element_by_xpath('//*[@id="blocked_vlan"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/div/a').click() ## Click on Action
            b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/div/ul/li[2]/a').click() ## Click on Deselect all
            #b.find_element_by_name("deselect_all").click()
            if (b.find_element_by_xpath('//*[@id="blocked_vlan"]/tbody/tr').get_attribute("class") == "odd"):
                print "Checkpoint 5: [PASSED] Deselect all function working as expected."
            else:
                print "Checkpoint 5: [FAILED] Deselect all function not working as expected."
                print self.fail("Test Case Failed.")
                return 0
                   
        else:
            print "Checkpoint 5: [FAILED] Cannot test deselect since select all is not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ################################################
        print ">> Testing Inverse selection functionality."
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/div/a').click() ## Click on Action
        b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/div/ul/li[3]/a').click() ## Click on Inverse selection
        if (b.find_element_by_xpath('//*[@id="blocked_vlan"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            print "Checkpoint 6: [PASSED] Inverse Selection function working as expected."
        else:
            print "Checkpoint 6: [FAILED] Inverse Selection function not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ##################################################
        print ">> Testing search functionality."
        add_vlan.clear()
        add_vlan.send_keys("2")
        b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="blocked_vlan"]/tbody/tr[2]/td').text == "2"):
            search = b.find_element_by_xpath('//*[@id="blocked_vlan_filter"]/label/input')
            search.clear()
            search.send_keys("2")
            if (b.find_element_by_xpath('//*[@id="blocked_vlan"]/tbody/tr/td').text == "2"):
                print "Checkpoint 7: [PASSED] Searching working fine."
            else:
                print "Checkpoint 7: [FAILED] Failed to search the expected VLAN ID."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 7: [FAILED] Failed to add another VLAN ID required for searching."
            print self.fail("Test case Failed.")
            return 0
        #################################################
        print ">> Testing Sorting based on VLAN ID's"
        search.send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE)
             
        b.find_element_by_xpath('//*[@id="blocked_vlan"]/thead/tr/th').click() ## Click on Sort icon
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="blocked_vlan"]/tbody/tr/td').text == "2" and b.find_element_by_xpath('//*[@id="blocked_vlan"]/tbody/tr[2]/td').text == "1"):
            print "Checkpoint 8: [PASSED] Sorting is working fine."
        else:
            print "Checkpoint 8: [FAILED] Sorting not working."
            print self.fail("Test case Failed.")
            return 0
        ############################################### 
        print ">> Testing of removal of single VLAN ID"
        b.find_element_by_xpath('//*[@id="blocked_vlan"]/tbody/tr/td').click()
        b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/button[2]').click()
        time.sleep(1)
             
        if (b.find_element_by_xpath('//*[@id="blocked_vlan"]/tbody/tr/td').text == "1"):
            print "Checkpoint 9: Selected VLAN ID removed successfully."
             
        elif (b.find_element_by_xpath('//*[@id="blocked_mac"]/tbody/tr/td').text == "2"):
            print "Checkpoint 9: Selected VLAN ID not deleted."
            print self.fail("Test case Failed.")
            return 0
        ##########################################
        print ">> Testing of number of entries shown per page."
        print ">> Adding 10 more VLAN ID's"
        for x in range (2,12):
            add_vlan.clear()
            add_vlan.send_keys("%d" %(x))
            b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)
        if (b.find_element_by_id("blocked_vlan_info").text == "Showing 1 to 10 of 11 entries"):
            print "Checkpoint 10: [PASSED] Number of entries '10' per page shown successfully."
        else:
            print "Checkpoint 10: [FAILED] Number of entries '10' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ###########################################
        print ">> Adding 20 more VLAN ID's"
        for x in range (12,32):
            add_vlan.clear()
            add_vlan.send_keys("%d" %(x))
            b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="blocked_vlan_length"]/label/select/option[2]').click()
        if (b.find_element_by_id("blocked_vlan_info").text == "Showing 1 to 25 of 31 entries"):
            print "Checkpoint 11: [PASSED] Number of entries '25' per page shown successfully."
        else:
            print "Checkpoint 11: [FAILED] Number of entries '25' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 20 more VLAN ID's"
        for x in range (32,52):
            add_vlan.clear()
            add_vlan.send_keys("%d" %(x))
            b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="blocked_vlan_length"]/label/select/option[3]').click()
        if (b.find_element_by_id("blocked_vlan_info").text == "Showing 1 to 50 of 51 entries"):
            print "Checkpoint 12: [PASSED] Number of entries '50' per page shown successfully."
        else:
            print "Checkpoint 12: [FAILED] Number of entries '50' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 50 more VLAN ID's"
        for x in range (52,102):
            add_vlan.clear()
            add_vlan.send_keys("%d" %(x))
            b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="blocked_vlan_length"]/label/select/option[4]').click()
        if (b.find_element_by_id("blocked_vlan_info").text == "Showing 1 to 100 of 101 entries"):
            print "Checkpoint 13: [PASSED] Number of entries '100' per page shown successfully."
        else:
            print "Checkpoint 13: [FAILED] Number of entries '100' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Test Paging"
        time.sleep(2)
        b.find_element_by_id("blocked_vlan_next").click()
        if (b.find_element_by_id("blocked_vlan_info").text == "Showing 101 to 101 of 101 entries"):
            print "Checkpoint 14: [PASSED] Paging functionality (Next) working fine."
            b.find_element_by_id("blocked_vlan_previous").click()
            if (b.find_element_by_id("blocked_vlan_info").text == "Showing 1 to 100 of 101 entries"):
                print "Checkpoint 15: [PASSED] Paging functionality (Previous) working fine."
                     
        else:
            print "Checkpoint 14: [FAILED] Paging functionality not working as expected."
            print self.fail("Test case Failed.")
            return 0
#         ###########################################
        print ">> Deleting all MAC ID's using select all button."
        time.sleep(2)
        if (b.find_element_by_id("blocked_vlan_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("blocked_vlan_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/div/ul/li[1]/a').click()
                b.find_element_by_xpath('//*[@id="vlan_block"]/form/fieldset/div/button[2]').click()
             
        if (b.find_element_by_id("blocked_vlan_info").text == "Showing 0 to 0 of 0 entries"):
            print "Checkpoint 16: [PASSED] All VLAN ID's deleted successfully.."
        else:
            print "Checkpoint 16: [FAILED] Failed to delete all VLAN ID's."
            print self.fail("Test Case Failed.")
            return 0
        
    def test_F_vlanexclude(self):
        print "\n\n>> #### TC6 - Configure Vlan Exclude List"
        do_login(self)
        b=self.driver
        b.find_element_by_xpath('//*[@id="block_exclude"]/div/div[1]/ul/li[6]/a').click() ### Clicking on Mac Block list
        time.sleep(1)
        if (b.find_element_by_id("excluded_vlan_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("excluded_vlan_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/div/ul/li[1]/a').click()
                #b.find_element_by_name("select_all").click()
                b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/button[2]').click()
                #b.find_element_by_name("rem_entry").click()
          
        add_vlan = b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/input')
        add_vlan.clear()
        print ">> Adding a single Vlan ID.."
        add_vlan.send_keys("1") ## Add a single Vlan ID
        b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        #b.find_element_by_name("add").click()
          
        time.sleep(1)
        added_vlan = b.find_element_by_xpath('//*[@id="excluded_vlan"]/tbody/tr/td')
        if (added_vlan.text == "1"):
            print "Checkpoint 4: [PASSED] Single VLAN ID added successfully."
        else:
            print "Checkpoint 4: [FAILED] VLAN ID not added."
            print self.fail("Test case Failed.")
            return 0
        ##################################################
        print ">> Testing Deselect all functionality."
        b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/div/ul/li[1]/a').click() ## CLick on Select all
         
        if (b.find_element_by_xpath('//*[@id="excluded_vlan"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
            b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/div/ul/li[2]/a').click() ## Click on Deselect all
            #b.find_element_by_name("deselect_all").click()
            if (b.find_element_by_xpath('//*[@id="excluded_vlan"]/tbody/tr').get_attribute("class") == "odd"):
                print "Checkpoint 5: [PASSED] Deselect all function working as expected."
            else:
                print "Checkpoint 5: [FAILED] Deselect all function not working as expected."
                print self.fail("Test Case Failed.")
                return 0
                  
        else:
            print "Checkpoint 5: [FAILED] Cannot test deselect since select all is not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ################################################
        print ">> Testing Inverse selection functionality."
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
        b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/div/ul/li[3]/a').click() ## Click on Inverse selection
        if (b.find_element_by_xpath('//*[@id="excluded_vlan"]/tbody/tr').get_attribute("class") == "odd row_selected"):
            print "Checkpoint 6: [PASSED] Inverse Selection function working as expected."
        else:
            print "Checkpoint 6: [FAILED] Inverse Selection function not working as expected."
            print self.fail("Test Case Failed.")
            return 0
        ##################################################
        print ">> Testing search functionality."
        add_vlan.clear()
        add_vlan.send_keys("2")
        b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="excluded_vlan"]/tbody/tr[2]/td').text == "2"):
            search = b.find_element_by_xpath('//*[@id="excluded_vlan_filter"]/label/input')
            search.clear()
            search.send_keys("2")
            if (b.find_element_by_xpath('//*[@id="excluded_vlan"]/tbody/tr/td').text == "2"):
                print "Checkpoint 7: [PASSED] Searching working fine."
            else:
                print "Checkpoint 7: [FAILED] Failed to search the expected VLAN ID."
                print self.fail("Test case Failed.")
                return 0
        else:
            print "Checkpoint 7: [FAILED] Failed to add another VLAN ID required for searching."
            print self.fail("Test case Failed.")
            return 0
        #################################################
        print ">> Testing Sorting based on VLAN ID's"
        search.send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE)
            
        b.find_element_by_xpath('//*[@id="excluded_vlan"]/thead/tr/th').click() ## Click on Sort icon
        time.sleep(1)
        if (b.find_element_by_xpath('//*[@id="excluded_vlan"]/tbody/tr/td').text == "2" and b.find_element_by_xpath('//*[@id="excluded_vlan"]/tbody/tr[2]/td').text == "1"):
            print "Checkpoint 8: [PASSED] Sorting is working fine."
        else:
            print "Checkpoint 8: [FAILED] Sorting not working."
            print self.fail("Test case Failed.")
            return 0
        ############################################### 
        print ">> Testing of removal of single VLAN ID"
        b.find_element_by_xpath('//*[@id="excluded_vlan"]/tbody/tr/td').click()
        b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/button[2]').click()
        time.sleep(1)
            
        if (b.find_element_by_xpath('//*[@id="excluded_vlan"]/tbody/tr/td').text == "1"):
            print "Checkpoint 9: Selected VLAN ID removed successfully."
            
        elif (b.find_element_by_xpath('//*[@id="exclude_mac"]/tbody/tr/td').text == "2"):
            print "Checkpoint 9: Selected VLAN ID not deleted."
            print self.fail("Test case Failed.")
            return 0
        ##########################################
        print ">> Testing of number of entries shown per page."
        print ">> Adding 10 more VLAN ID's"
        for x in range (2,12):
            add_vlan.clear()
            add_vlan.send_keys("%d" %(x))
            b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)
        if (b.find_element_by_id("excluded_vlan_info").text == "Showing 1 to 10 of 11 entries"):
            print "Checkpoint 10: [PASSED] Number of entries '10' per page shown successfully."
        else:
            print "Checkpoint 10: [FAILED] Number of entries '10' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ###########################################
        print ">> Adding 20 more VLAN ID's"
        for x in range (12,32):
            add_vlan.clear()
            add_vlan.send_keys("%d" %(x))
            b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)
        b.find_element_by_xpath('//*[@id="excluded_vlan_length"]/label/select/option[2]').click()
        if (b.find_element_by_id("excluded_vlan_info").text == "Showing 1 to 25 of 31 entries"):
            print "Checkpoint 11: [PASSED] Number of entries '25' per page shown successfully."
        else:
            print "Checkpoint 11: [FAILED] Number of entries '25' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 20 more VLAN ID's"
        for x in range (32,52):
            add_vlan.clear()
            add_vlan.send_keys("%d" %(x))
            b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="excluded_vlan_length"]/label/select/option[3]').click()
        if (b.find_element_by_id("excluded_vlan_info").text == "Showing 1 to 50 of 51 entries"):
            print "Checkpoint 12: [PASSED] Number of entries '50' per page shown successfully."
        else:
            print "Checkpoint 12: [FAILED] Number of entries '50' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Adding 50 more VLAN ID's"
        for x in range (52,102):
            add_vlan.clear()
            add_vlan.send_keys("%d" %(x))
            b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/button[1]').click() ## Clicked on Add button
        time.sleep(2)    
        b.find_element_by_xpath('//*[@id="excluded_vlan_length"]/label/select/option[4]').click()
        if (b.find_element_by_id("excluded_vlan_info").text == "Showing 1 to 100 of 101 entries"):
            print "Checkpoint 13: [PASSED] Number of entries '100' per page shown successfully."
        else:
            print "Checkpoint 13: [FAILED] Number of entries '100' per page not shown."
            print self.fail("Test Case Failed.")
            return 0
        ##########################################
        print ">> Test Paging"
        time.sleep(2)
        b.find_element_by_id("excluded_vlan_next").click()
        if (b.find_element_by_id("excluded_vlan_info").text == "Showing 101 to 101 of 101 entries"):
            print "Checkpoint 14: [PASSED] Paging functionality (Next) working fine."
            b.find_element_by_id("excluded_vlan_previous").click()
            if (b.find_element_by_id("excluded_vlan_info").text == "Showing 1 to 100 of 101 entries"):
                print "Checkpoint 15: [PASSED] Paging functionality (Previous) working fine."
                    
        else:
            print "Checkpoint 14: [FAILED] Paging functionality not working as expected."
            print self.fail("Test case Failed.")
            return 0
#         ###########################################
        print ">> Deleting all MAC ID's using select all button."
        time.sleep(2)
        if (b.find_element_by_id("excluded_vlan_info").text != "Showing 0 to 0 of 0 entries"):
            while (b.find_element_by_id("excluded_vlan_info").text != "Showing 0 to 0 of 0 entries"):
                b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/div/a').click() ## Click on Action
                time.sleep(1)
                b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/div/ul/li[1]/a').click()
                b.find_element_by_xpath('//*[@id="vlan_exclude"]/form/fieldset/div/button[2]').click()
            
        if (b.find_element_by_id("excluded_vlan_info").text == "Showing 0 to 0 of 0 entries"):
            print "Checkpoint 16: [PASSED] All VLAN ID's deleted successfully.."
        else:
            print "Checkpoint 16: [FAILED] Failed to delete all VLAN ID's."
            print self.fail("Test Case Failed.")
            return 0


    def tearDown(self):
        do_logout(self)
        self.driver.close()