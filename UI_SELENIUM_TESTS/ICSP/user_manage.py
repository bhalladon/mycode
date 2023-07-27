import unittest, time
from selenium import webdriver
#from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
#from timeit import itertools
#from wheel.signatures import assertTrue

def do_logout(self):
    self.driver.get(self.nnp_ip+'logout')
    #self.driver.find_element_by_id("userbtn").click()
    #self.driver.find_element_by_link_text("Logout").click()

def do_login(self,driver,webuser,webpassword):
    self.driver.get(self.nnp_ip)
    
    self.driver.maximize_window()
    b=self.driver
    #b.set_window_size(1280,900)
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
    time.sleep(1)
    username.send_keys(webuser)
    password = b.find_element_by_name("password")
    password.clear()
    password.send_keys(webpassword)
    b.find_element_by_class_name("btn-primary").click()
     
    try:
        element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "nnp_version_header"))
        )
    except:
        print "Checkpoint 2: [FAILED] User not logged in."
        print self.fail("Test Case Failed.")
        return 0
    print "Checkpoint 2: [PASSED] User successfully logs in."
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.ID, "userbtn")))
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.ID, "userbtn")))
    except:
        print "Checkpoint 3: [FAILED] 'admin' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_id("userbtn").click()
     
    try:
        element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Manage"))
        )
    except:
        print "Checkpoint 3: [FAILED] 'Manage' link not found."
        print self.fail("Test Case Failed.")
        return 0
    b.find_element_by_link_text("Manage").click()
     
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"add_user")))
    except:
        print "Checkpoint 3: [FAILED] User Management page not loaded."
        print self.fail("Case Status: FAILED.")
        return 0
    print "Checkpoint 3: [PASSED] Navigated to 'User > Manage' page successfully."

def delete_allusers(self):
    b=self.driver
    b.find_element_by_xpath('//*[@id="user_insertion_spot"]/div[2]/i[1]').click()
    try:
        element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME,"confirm"))
        )
        time.sleep(1)
        b.find_element_by_name("confirm").click()
    except:
        print "[FAILED] Pop-up window for the delete confirmation not displayed."
        print self.fail("Case Status: FAILED.")
        return 0
    try:
        element = WebDriverWait(b,5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="user_insertion_spot"]/div[2]/i[1]'))
        )
        time.sleep(1)
        delete_allusers(self)
    except TimeoutException:
        print "All users deleted successfully." 
    
class user_manage(unittest.TestCase):
    
    nnp_ip = "https://10.138.129.47/"
    
    def setUp(self):
        self.driver=webdriver.Firefox()
         
     
    def test_a_usermanagement(self):
        print "\n##### Add a single user"
        b=self.driver
        do_login(self,b,"admin","norman")
          
        time.sleep(1)
        print "Delete all users other than admin if exist any"
        try:
            element = WebDriverWait(b,5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="user_insertion_spot"]/div[2]/i[1]'))
            )
            delete_allusers(self)
        except TimeoutException:
            print "No users other than admin exists."
        #############################################################################
        
        print '>>> Clicking on "Add User" button.'
        b.find_element_by_id("add_user").click()
        try:
            element=WebDriverWait(b,10).until(EC.presence_of_element_located,((By.ID,"new_username_input"))
            )
        except:
            print "Checkpoint 4: [FAILED] pop-up for inputting username not displayed after clicking 'Add user' button."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 4: [PASSED] Pop-up for inputting username and password displayed successfully."
        time.sleep(2)
        print "\n>>> Creating a new user named 'admin1'."
        b.find_element_by_id("new_username_input").send_keys("admin1")
        b.find_element_by_id("password_input").send_keys("norman")
        b.find_element_by_id("repeat_password_input").send_keys("norman")
        b.find_element_by_name("confirm").click()
        time.sleep(1)
        new_user = b.find_element_by_xpath('//*[@id="user_insertion_spot"]/div[2]')
        if "admin1" in new_user.text:
            print 'Checkpoint 5: [PASSED] User "admin1" added successfully.'
        else:
            print 'checkpoint 5: [FAILED] User "admin1" not added.'
            print self.fail("Case Status: FAILED.")
            return 0
        ########################################################################
        print "\n#############################"
        print ">>> Adding a duplicate user."
        print ">>> Clicking on 'Add new user' button."
        time.sleep(1)
        b.find_element_by_id("add_user").click()
        try:
            element=WebDriverWait(b,10).until(EC.presence_of_element_located,((By.ID,"new_username_input"))
            )
        except:
            print "Checkpoint 6: [FAILED] pop-up for inputting username not displayed after clicking 'Add user' button."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 6: [PASSED] Pop-up for inputting username and password displayed successfully."
        time.sleep(2)
        b.find_element_by_id("new_username_input").send_keys("admin1")
        b.find_element_by_id("password_input").send_keys("norman")
        b.find_element_by_id("repeat_password_input").send_keys("norman")
        b.find_element_by_name("confirm").click()
        time.sleep(1)
             
        if (str(b.find_element_by_id("username_ctl").get_attribute("text") == "Username is already taken. Choose another one.")):
            print "Checkpoint 7: [PASSED] Duplicate user not added."
            b.find_element_by_name("cancel").click()
        else:
            print "Checkpoint 7: [FAILED] Duplicate user added successfully."
            self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
           
        #################################################
        print "\n#############################"
        print ">>> Change user password"
        print ">> Clicking of edit icon."
        b.find_element_by_xpath('//*[@id="user_insertion_spot"]/div[2]/i[2]').click()
        try:
            element=WebDriverWait(b,10).until(EC.presence_of_element_located,((By.ID,"old_password_input"))
            )
        except:
            print "Checkpoint 8: [FAILED] pop-up for inputting old password and new password not displayed after clicking on edit icon."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 8: [PASSED] Pop-up for inputting old password and new password displayed successfully."
        time.sleep(2)
        b.find_element_by_id("old_password_input").send_keys("norman")
        b.find_element_by_id("new_password_input").send_keys("norman1")
        b.find_element_by_id("repeat_password_input").send_keys("norman1")
        b.find_element_by_name("confirm").click()
        time.sleep(2)
        print ">>> Logging out."
        do_logout(self)
        try:
            element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.NAME, "username"))
            )
        except:
            print "Checkpoint 9: [FAILED] Login page not opened after logging out."
            print self.fail("Test case Failed.")
            return 0
        print "Checkpoint 9: [PASSED] Logged out and login page appeared successfully."
        time.sleep(1)
        print ">>> Logging with the changed password now."
        username = b.find_element_by_name("username")
        username.clear()
        username.send_keys("admin1")
        password = b.find_element_by_name("password")
        password.clear()
        password.send_keys("norman1")
        b.find_element_by_class_name("btn-primary").click()
        try:
            element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "nnp_version_header"))
            )
        except:
            print "Checkpoint 10: [FAILED] Page not loaded after successful login."
            print self.fail("Test Case Failed.")
            return 0
        print "Checkpoint 10: [PASSED] User successfully logged in using new(changed) password."
        print ">>> Logging out."
        time.sleep(1)
        do_logout(self)
        print ">>> Logging in with the admin user."
        username = b.find_element_by_name("username")
        username.clear()
        username.send_keys("admin")
        password = b.find_element_by_name("password")
        password.clear()
        password.send_keys("norman")
        b.find_element_by_class_name("btn-primary").click()
        try:
            element = WebDriverWait(b, 10).until(EC.presence_of_element_located((By.ID, "nnp_version_header"))
            )
        except:
            print "Checkpoint 11: [FAILED] Page not loaded after successful login."
            print self.fail("Test Case Failed.")
            return 0
        try:
            element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.ID, "userbtn"))
            )
            element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.ID, "userbtn")))
        except:
            print "Checkpoint 11: [FAILED] 'admin' link not found."
            print self.fail("Test Case Failed.")
            return 0
        print "test12"
        b.find_element_by_id("userbtn").click()
        print "test13"
        try:
            element = WebDriverWait(b,20).until(EC.presence_of_element_located((By.LINK_TEXT, "Manage"))
            )
        except:
            print "Checkpoint 11: [FAILED] 'Manage' link not found."
            print self.fail("Test Case Failed.")
            return 0
        b.find_element_by_link_text("Manage").click()
        print "Checkpoint 11: Navigated to user manage page successfully."
        #############################################################################   
        print "\n#############################"
        print ">>> Deleting newly added user i.e 'admin1'"
        time.sleep(1)
        b.find_element_by_xpath('//*[@id="user_insertion_spot"]/div[2]/i[1]').click()
        time.sleep(1)
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located,((By.NAME,"confirm"))
            )
        except:
            print "Checkpoint 12: [FAILED] Pop-up to confirm the deletion of a user is not displayed."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 12: [PASSED] Pop-up to confirm the deletion of a user is displayed successfully."
        b.find_element_by_name("confirm").click()
        time.sleep(2)
        try:
            elememt = WebDriverWait(b,4).until_not(EC.presence_of_element_located((By.CSS_SELECTOR,"#user_insertion_spot > div:nth-child(2)"))
            )
        except:
            print "Checkpoint 13: [FAILED] User 'admin1' not deleted."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 13: [PASSED] User 'admin1 deleted successfully."
        time.sleep(1)
        ##########################################################################
        print "\n#############################"
        print ">>> Add a new user with password and confirm password does not match"
        b.find_element_by_id("add_user").click()
        try:
            element=WebDriverWait(b,10).until(EC.presence_of_element_located,((By.ID,"new_username_input"))
            )
        except:
            print "Checkpoint 14: [FAILED] pop-up for inputting username not displayed after clicking 'Add user' button."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 14: [PASSED] Pop-up for inputting username and password displayed successfully."
        time.sleep(2)
        b.find_element_by_id("new_username_input").send_keys("admin1")
        b.find_element_by_id("password_input").send_keys("norman")
        b.find_element_by_id("repeat_password_input").send_keys("norman1")
        b.find_element_by_name("confirm").click()
        time.sleep(1)
        if (str(b.find_element_by_id("repeat_password_control").get_attribute("text") == "Passwords fields does not match.")):
            print "Checkpoint 15: [PASSED] User not added as expected since password and confirm password does not match."
            b.find_element_by_name("cancel").click()
        else:
            print "Checkpoint 15: [FAILED] User added successfully even though the passwords does not match."
            self.fail("Case Status: FAILED.")
            return 0
              
        ########################################################################
        print "\n#############################"
        print ">>> Add a new user with null password and confirm password."
        time.sleep(1)
        b.find_element_by_id("add_user").click()
        try:
            element=WebDriverWait(b,10).until(EC.presence_of_element_located,((By.ID,"new_username_input"))
            )
        except:
            print "Checkpoint 16: [FAILED] pop-up for inputting username not displayed after clicking 'Add user' button."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 16: [PASSED] Pop-up for inputting username and password displayed successfully."
        time.sleep(2)
        b.find_element_by_id("new_username_input").send_keys("admin1")
        b.find_element_by_id("password_input").clear()
        b.find_element_by_id("repeat_password_input").clear()
        b.find_element_by_name("confirm").click()
        time.sleep(1)
        if (str(b.find_element_by_id("repeat_password_control").get_attribute("text") == "Passwords fields are blank!")):
            print "Checkpoint 17: [PASSED] User not added as expected since password and confirm password are blank."
            b.find_element_by_name("cancel").click()
        else:
            print "Checkpoint 17: [FAILED] User added successfully even though the passwords are blank."
            self.fail("Case Status: FAILED.")
            return 0
              
        ########################################################################
        print "\n#############################"
        print ">>> Add a new user with a valid password and blank confirm password."
        time.sleep(1)
        b.find_element_by_id("add_user").click()
        try:
            element=WebDriverWait(b,10).until(EC.presence_of_element_located,((By.ID,"new_username_input"))
            )
        except:
            print "Checkpoint 18: [FAILED] pop-up for inputting username not displayed after clicking 'Add user' button."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 18: [PASSED] Pop-up for inputting username and password displayed successfully."
        time.sleep(2)
        b.find_element_by_id("new_username_input").send_keys("admin1")
        b.find_element_by_id("password_input").send_keys("norman")
        b.find_element_by_id("repeat_password_input").clear()
        b.find_element_by_name("confirm").click()
        time.sleep(1)
        if (str(b.find_element_by_id("repeat_password_control").get_attribute("text") == "Passwords fields does not match.")):
            print "Checkpoint 19: [PASSED] User not added as expected since confirm password is blank."
            b.find_element_by_name("cancel").click()
        else:
            print "Checkpoint 19: [FAILED] User added successfully even though the confitm password filed is blank."
            self.fail("Case Status: FAILED.")
            return 0
        ########################################################################
        print "\n#############################"
        print ">>> Add a new user with a blank password and a valid confirm password."
        time.sleep(1)
        b.find_element_by_id("add_user").click()
        try:
            element=WebDriverWait(b,10).until(EC.presence_of_element_located,((By.ID,"new_username_input"))
            )
        except:
            print "Checkpoint 20: [FAILED] pop-up for inputting username not displayed after clicking 'Add user' button."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 20: [PASSED] Pop-up for inputting username and password displayed successfully."
        time.sleep(2)
        b.find_element_by_id("new_username_input").send_keys("admin1")
        b.find_element_by_id("password_input").clear()
        b.find_element_by_id("repeat_password_input").send_keys("norman")
        b.find_element_by_name("confirm").click()
        time.sleep(1)
        if (str(b.find_element_by_id("repeat_password_control").get_attribute("text") == "Passwords fields does not match.")):
            print "Checkpoint 21: [PASSED] User not added as expected since confirm password is blank."
            b.find_element_by_name("cancel").click()
        else:
            print "Checkpoint 21: [FAILED] User added successfully even though the confirm password filed is blank."
            self.fail("Case Status: FAILED.")
            return 0
        try:
            element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"add_user"))
            )
        except:
            print "Checkpoint 22: [FAILED] On clicking cancel button page is not returned to user management page."
            print self.fail("Case Status: FAILED.")
            return 0
        time.sleep(1)
        print "\n###### ADD MULTIPLE USERS."
        b.find_element_by_id("add_user").click()
        try:
            element=WebDriverWait(b,10).until(EC.presence_of_element_located,((By.ID,"new_username_input"))
            )
        except:
            print "Checkpoint 22: [FAILED] pop-up for inputting username not displayed after clicking 'Add user' button."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 22: [PASSED] Pop-up for inputting username and password displayed successfully."
        for k in range(1,7):
            time.sleep(2)
            username = b.find_element_by_id("new_username_input")
            password = b.find_element_by_id("password_input")
            repeat_password = b.find_element_by_id("repeat_password_input")    
            username.send_keys("admin%d" % (k))
            password.send_keys("norman")
            repeat_password.send_keys("norman")
            b.find_element_by_name("confirm").click()
            try:
                element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.ID,"add_user"))
                )
            except:
                print "Checkpoint 23: [FAILED] After adding user, page not returned to previous screen."
                print self.fail("Case Status: FAILED.")
                return 0
            time.sleep(1)
            b.find_element_by_id("add_user").click()
        time.sleep(1)
        b.find_element_by_name("cancel").click()
        try:
            elememt = WebDriverWait(b,4).until(EC.presence_of_element_located((By.XPATH,'//*[@id="user_insertion_spot"]/div[7]'))
            )
        except:
            print "Checkpoint 23: [FAILED] All expected user names not added." 
            print self.fail("Case Status: FAILED.")
            return 0 
        print "Checkpoint 23: [PASSED] All users added successfully."
        #######################################################################
        print "\n#############################"
        print ">>> Delete all users added above."
             
        for k in range(1,7):
            b.find_element_by_xpath('//*[@id="user_insertion_spot"]/div[2]/i[1]').click()
            time.sleep(1)
            try:
                element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME,"confirm"))
                )
            except:
                print "Checkpoint 24: [FAILED] Pop-up window for the delete confirmation not displayed."
                print self.fail("Case Status: FAILED.")
                return 0
            time.sleep(1)
            b.find_element_by_name("confirm").click()
            time.sleep(2)
                    
        try:
            elememt = WebDriverWait(b,4).until(EC.presence_of_element_located((By.XPATH,'//*[@id="user_insertion_spot"]/div[2]/i[1]'))
            )
            print "Checkpoint 24: [FAILED] All expected user not deleted." 
            print self.fail("Case Status: FAILED.")
            return 0
        except:
            print "Checkpoint 24: [PASSED] All users deleted successfully." 
            #return 0
        

        ###########################################################
        print "\n#############################"
        print ">>> Add a new user which has exclamation (!) character in username and edit the user. Edit window should open up."
        time.sleep(1)
        print ">>> Click on 'Add new user' button."
        b.find_element_by_id("add_user").click()
         
        try:
            element=WebDriverWait(b,10).until(EC.presence_of_element_located,((By.ID,"new_username_input"))
            )
        except:
            print "Checkpoint 25: [FAILED] pop-up for inputting username not displayed after clicking 'Add user' button."
            print self.fail("Case Status: FAILED.")
            return 0
        print "Checkpoint 25: [PASSED] Pop-up for inputting username and password displayed successfully."
        time.sleep(2)
        print "\n>>> Creating a new user named 'user!'."
        b.find_element_by_id("new_username_input").send_keys("user!")
        b.find_element_by_id("password_input").send_keys("norman")
        b.find_element_by_id("repeat_password_input").send_keys("norman")
        b.find_element_by_name("confirm").click()
        time.sleep(1)
        new_user = b.find_element_by_xpath('//*[@id="user_insertion_spot"]/div[2]')
        if "user!" in new_user.text:
            print 'Checkpoint 25: [PASSED] User "user!" added successfully.'
        else:
            print 'checkpoint 25: [FAILED] User "user!" not added.'
            print self.fail("Case Status: FAILED.")
            return 0
        print "\n>>> Clicking on 'edit' icon now."
        b.find_element_by_xpath('//*[@id="user_insertion_spot"]/div[2]/i[2]').click()
        time.sleep(2)
        try:
            element=WebDriverWait(b,10).until_not(EC.presence_of_element_located,((By.ID,"old_password_input"))
            )
            print "Checkpoint 26: [PASSED] Pop-up for inputting old password and new password displayed successfully."
            b.find_element_by_name("cancel").click()
            time.sleep(1)
            print "\n###########################"
            print ">>> Deleting the user created above."
            b.find_element_by_xpath('//*[@id="user_insertion_spot"]/div[2]/i[1]').click()
            time.sleep(1)
            try:
                element = WebDriverWait(b,10).until(EC.presence_of_element_located((By.NAME,"confirm"))
                )
            except:
                print "Checkpoint 27: [FAILED] Pop-up window for the delete confirmation not displayed."
                print self.fail("Case Status: FAILED.")
                return 0
            time.sleep(1)
            b.find_element_by_name("confirm").click()
            time.sleep(2)
             
        except:
            print "Checkpoint 26: [FAILED] pop-up for inputting old password and new password not displayed after clicking on edit icon."
            print self.fail("Case Status: FAILED.")
            return 0


        #########################################################################
        
    
        


    def tearDown(self):
        do_logout(self)
        self.driver.close()
        
if __name__ == '__main__':
    unittest.main()