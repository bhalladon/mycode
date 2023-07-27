#!/usr/bin/python

from selenium import webdriver
from settings import *
from selenium.webdriver.common.by import By
import unittest, time


class selenium_framework():
    
    def wait(self,driver,timeout,attribute,value):
        thinktime = 1
        status = False
        while True:    
            try:
                if (driver.find_elements(attribute,value).__len__() > 0):
                    status = True
                else:
                    status = False
            except:
                status =  False
            
            if (status == True):           
                break 
            else:
                thinktime = thinktime + 1
                time.sleep(1)
                
            if (thinktime> timeout):
                #reporting(html_report,driver,"TimeOut: [FAILED] Element "+attribute +" with value "+ value + " not found")
                print "TimeOut: [FAILED] Element "+attribute +" with value "+ value + " not found"
                print  self.fail("Case Status: [Failed]")
                #name = str(datetime.datetime.utcnow())
                #name = name.replace(":","_").replace(".", "_")
                #driver.get_screenshot_as_file("ScreenShot_"+name+".png") ## Not saving the screenshots for now
                break
            return status
    
    def login(self, driver, user, password1):
        selenium_framework.wait(self, driver, 10, By.ID, "username")
        username = driver.find_element_by_id("username")
        username.click()
        username.clear()
        username.send_keys(user)
        password = driver.find_element_by_id("password")
        password.click()
        password.clear()
        password.send_keys(password1)
        driver.find_element_by_id("submit").click()
                    
    def select_from_dropdown(self, driver, attribute, value):
        b = self.driver
        b.find_element_by_class_name("primary_menu")
        
