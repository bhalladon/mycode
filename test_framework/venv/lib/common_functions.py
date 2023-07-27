import requests
import httplib, unittest, time, sys, select, requests, os, time, urllib
import simplejson as json
from casmarapi.config.config import *
import requests.packages.urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
import shutil,ssl
from timeit import itertools
import paramiko
from paramiko import ssh_exception
from paramiko_expect import SSHClientInteraction

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
requests.packages.urllib3.has_memoryview = False

class casutilities():

    def httpcall(self, call_method, rapicall, values, headers):
        url = "https://" +cas_ip+ rapicall
        call_method = call_method.lower()
        if call_method == "get":
            r = requests.get(url, data=values, headers=headers, verify=False)
        if call_method == "post":
            r = requests.post(url, data=values, headers=headers, verify=False)
        if call_method == "delete":
            r = requests.delete(url, data=values, headers=headers, verify=False)
        if r.status_code in [200,201]:
            fdata = json.loads(r.text)
            return fdata

        else:
            if "HTTP 504: Gateway Timeout (IntelliVM Control Service busy" in r.text:
                return r.text
                return r.status_code
            else:
                print "Unable to process the request " + str(rapicall)
                print "HTTP error code is: " + str(r.status_code)
                return r.text
                return r.status_code


    def generate_token(self):
        a = casutilities()
        values = {"username":cas_adminuser, "password":cas_adminpass}
        headers = {"User-Agent":"python"}
        token = a.httpcall("POST", "/rapi/auth/session", values, headers)['results']['session_token_string']
        return token