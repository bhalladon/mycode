from config.config_data import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome
from selenium.webdriver.firefox.options import Options as firefox
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import os

import time


class uiutilities():
    print("bhalla")
    global b
    chrome_options = chrome()
    firefox_options = firefox()

    if str(headless).lower() == "true" and str(web_browser).lower() == "chrome":
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=3840x2160")
        print(os.getcwd())
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver")

    if str(headless).lower() == "false" and str(web_browser).lower() == "chrome":
        driver = webdriver.Chrome(executable_path="./chromedriver")
        #driver.set_window_size("3840", "2160")

    if str(headless).lower() == "true" and str(web_browser).lower() == "firefox":
        firefox_options.add_argument("--headless")
        #firefox_options.add_argument("--window-size=3840x2160")
        firefox_options.add_argument("--kiosk")
        driver = webdriver.Firefox(firefox_options=firefox_options, executable_path="./geckodriver")

    if str(headless).lower() == "false" and str(web_browser).lower() == "firefox":
        driver = webdriver.Firefox(executable_path="./geckodriver")
        #driver.set_window_size("3840", "2160")

    b = driver
    b.implicitly_wait(10)
    b.maximize_window()
    b.get(url)

    # def waitfor(self,timeout,By,value):
    #     d=b.find_elements(By,value)
    #     print("Value for d is: ") + str(d)
    #     thinktime = 0
    #     status = True
    #     while status == True:
    #         if d.__len__() > 0:
    #         #if b.find_element_by_link_text('Request Demo'):
    #             print("Element found.")
    #             status = False
    #         else:
    #             thinktime += 1
    #             time.sleep(1)
    #             if thinktime > timeout:
    #                 print("Element not found")
    #                 status = False
