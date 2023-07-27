#from config.config_data import *
import unittest, time, selenium
from selenium.common.exceptions import ElementClickInterceptedException as EC
from lib.common_functions import *
from selenium.webdriver.common.keys import Keys
import xmlrunner

class uitests(unittest.TestCase):

    def setUp(self):
        global c
        c = uiutilities()
        global b
        b = c.driver

    def test_a_request_demo(self):
        print("starting tests")
        try:
            if b.find_element_by_id("alert-box-message"):
                if b.find_element_by_class_name("accept-cookies-button"):
                    time.sleep(10)
                    #wait = WebDriverWait(b, 20)
                    #wait.until(EC.((By.XPATH, "//button[contains(.,'Accept Cookies')]"))).click()
                    #wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Accept Cookies')]")))
                    b.find_element_by_xpath("//button[contains(.,'Accept Cookies')]").click()
                    # b.find_element_by_xpath("//*[@class='accept-cookies-button']//*[text()='Accept Cookies']").click()

            request_demo = b.find_element_by_link_text("Request Demo")
            request_demo.click()


            if b.find_element_by_name("FirstName"):
                b.find_element_by_name("FirstName").click()
                b.find_element_by_name("FirstName").clear()
                b.find_element_by_name("FirstName").send_keys("Test")

            if b.find_element_by_name("LastName"):
                b.find_element_by_name("LastName").click()
                b.find_element_by_name("LastName").clear()
                b.find_element_by_name("LastName").send_keys("Test")

            if b.find_element_by_id("Job_Level__c-selectized"):
                print ("Element found")
                b.find_element_by_id("Job_Level__c-selectized").click()
                b.find_element_by_xpath("//*[@class='selectize-dropdown-content']//*[text()='Director']").click()

            if b.find_element_by_id("Job_Function__c-selectized"):
                b.find_element_by_id("Job_Function__c-selectized").click()
                b.find_element_by_xpath("//*[@class='selectize-dropdown-content']//*[text()='IT']").click()

            try:
                if b.find_element_by_name("Email"):
                    b.find_element_by_name("Email").click()
                    b.find_element_by_name("Email").clear()
                    b.find_element_by_name("Email").send_keys("abcxyz@google.com")
            except EC:
                print("Please enter a corporate email address")
                b.find_element_by_name("Email").click()
                b.find_element_by_name("Email").clear()
                b.find_element_by_name("Email").send_keys("abcxyz@google.com")

            try:
                if b.find_element_by_name("Phone"):
                    b.find_element_by_name("Phone").click()
                    b.find_element_by_name("Phone").clear()
                    b.find_element_by_name("Phone").send_keys("1234567890")

            except EC:
                if b.find_element_by_name("Phone"):
                    print ("yahoo")
                    b.find_element_by_name("Phone").click()
                    b.find_element_by_name("Phone").clear()
                    b.find_element_by_name("Phone").send_keys("123456789")

            if b.find_element_by_name("Company"):
                b.find_element_by_name("Company").click()
                b.find_element_by_name("Company").clear()
                b.find_element_by_name("Company").send_keys("abcxyz")

            if b.find_element_by_id("No_Employees_Users__c-selectized"):
                b.find_element_by_id("No_Employees_Users__c-selectized").click()
                b.find_element_by_xpath("//*[@class='selectize-dropdown-content']//*[text()='100 - 499']").click()

            if b.find_element_by_id("Country-selectized"):
                b.find_element_by_id("Country-selectized").click()
                b.find_element_by_xpath("//*[@class='selectize-dropdown-content']//*[text()='Albania']").click()

            time.sleep(2)

            if b.find_element_by_id("btn-form-contact-us"):
                b.find_element_by_id("btn-form-contact-us").click()

            time.sleep(10)
            fp = open("logs.txt", 'w')
            fp.write(str(b.page_source.encode('utf8')))
            fp.close()
            fp = open("logs.txt", 'r')
            for line in fp.readlines():
                if "Thank you! We will be in touch within one business&nbsp;day" in line:
                    print("Request for demo submitted successfully")
                    fp.close()
                    os.remove("logs.txt")
                    break
                else:
                    pass
            if os.path.exists(os.path.join(os.getcwd(), "logs.txt")):
                self.fail("Request for demo not submitted successfully.")
                fp.close()
        except:
            self.fail("Request for demo not submitted successfully.")

    def tearDown(self):
        print("Closing browser")
        b.close()


if __name__ == '__main__':
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)

