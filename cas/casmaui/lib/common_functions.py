
import unittest, time, sys, select, os, time
from casmaui.config.config import *
import requests.packages.urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
requests.packages.urllib3.has_memoryview = False

        
class uitest():
    ## Reading web_browser value from config.py ##
    if web_browser == "chrome":
        chromdriver = "./chromedriver"
        driver = webdriver.Chrome(executable_path=chromdriver)
    if web_browser == "firefox":
        driver = webdriver.Firefox(executable_path='./geckodriver')
    if web_browser == "ie":
        driver = webdriver.Ie()
        
    if web_browser == "":
        driver = webdriver.Firefox()
    
    global b
    b = driver
    b.maximize_window()
    
    def waitfor(self,timeout,attribute,value):
        thinktime = 1
        status = False
        while True:    
                  
            try:
                if (b.find_elements(attribute,value).__len__() > 0):
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
                self.fail("Case Status: [Failed]")
                break
        return status
    
    def navigate_primary(self,page_name):   
        b.find_element_by_xpath("//div[contains(@class,'primary-navigation')]/descendant::node()/span[contains(.,'"+page_name+"')]").click()

    def navigate_secondary(self,page_name):        
        b.find_element_by_xpath("//div[contains(@class,'secondary-navigation')]/descendant::node()/span[contains(.,'"+page_name+"')]").click()

    def login(self, username, password):
        #self.driver = webdriver.Firefox()
        #b = self.driver
        b.get(cas_http_ip)
        if uitest.waitfor(self,20,By.NAME,"username"):
            print "Checkpoint 1: [Passed] Login page appeared successfully."
            username = b.find_element_by_name("username").send_keys(username)
        if uitest.waitfor(self,20,By.NAME,"password"):
            password = b.find_element_by_name("password").send_keys(password)
        if uitest.waitfor(self,20,By.LINK_TEXT,"Submit"):
            b.find_element_by_link_text("Submit").click()
        if uitest.waitfor(self,20,By.XPATH,"//div[contains(@class,'x-panel-body-default')]/descendant::node()/label[contains(.,'Service Uptime')]"):
            print "Checkpoint 2: [Passed] User successfully logged in."
            
    def upload_baseimage_url(self, baseimage_url, baseimage_key):
        if uitest.waitfor(self, 20, By.XPATH, '//div[contains(@class,"secondary-navigation-vertical")]/descendant::node()/span[contains(.,"On-box Sandboxing")]'):
            b.find_element_by_xpath('//div[contains(@class,"secondary-navigation-vertical")]/descendant::node()/span[contains(.,"On-box Sandboxing")]').click()
        if uitest.waitfor(self, 20, By.XPATH, '//div[contains(@class,"x-panel-default")]/descendant::node()/span[contains(.,"Add Base and Initial Profile")]'):
            print "On-Box Sandboxing page appeared successfully."
            b.find_element_by_xpath('//div[contains(@class,"x-panel-default")]/descendant::node()/span[contains(.,"Add Base and Initial Profile")]').click()
        if uitest.waitfor(self, 20, By.XPATH, '//div[contains(@class,"x-panel-default")]/descendant::node()/span[contains(.,"Url Download")]'):
            print "Add Base and Initial Profile page appeared successfully."
        if uitest.waitfor(self,20,By.XPATH,'//div[contains(@class,"x-panel-default")]/descendant::node()/span[contains(.,"Url Download")]'):
            print "hello"
            b.find_element_by_xpath('//div[contains(@class,"x-panel-default")]/descendant::node()/span[contains(.,"Url Download")]').click()
        if uitest.waitfor(self, 20, By.XPATH, '//div[contains(@class,"x-panel-body")]/descendant::node()/span[contains(.,"Base Image Url:")]'):
            print "Url Download tab opened successfully."
            base_image_url = b.find_element_by_xpath('//div[contains(@class,"x-panel-body")]/descendant::node()/input[@placeholder="Url to base image file"]')
            base_image_url.clear()
            base_image_url.send_keys(baseimage_url)
            product_key = b.find_element_by_name("product_key_url-inputEl")
            product_key.clear()
            product_key.send_keys(baseimage_key)
            #start_activation = b.find_element_by_xpath('//div[contains(@class,"x-panel-body-default")]/descendant::node()/span[@contains(.,"Start Activation")]')
            xx = b.find_elements(By.XPATH,'//div[contains(@class,"x-panel-body-default")]/descendant::node()/span[contains(.,"Start Activation")]')
            total_len = len(xx)
            for x in range(total_len):
                try:
                    xx[x].click()
                    break
                except ElementNotVisibleException:
                    pass
            print "DONE"
            b.close()
 
            
            
