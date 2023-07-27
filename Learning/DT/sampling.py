import httplib, urllib, json, unittest, time, sys, select, paramiko
from settings.conf import *


def get_build_version():
    version = ''
    app_url = "https://" + str(ma_ip)
    values = {'username' : adminuser,'password' : adminpassword}
    headers = {'User-Agent': 'python','Content-Type': 'application/x-www-form-urlencoded',}
    values = urllib.urlencode(values)
    conn = httplib.HTTPSConnection(app_url.replace('https://', '') )
    conn.request("POST", "/rapi/auth/session", values, headers)
    response = conn.getresponse()
    data = response.read()
    #print data
    fdata = json.loads(data)
    global token
    token = fdata['results']['session_token_string']        
    
    url = app_url +  "/rapi/system/version_info?token="+ str(token)      
    r = requests.get(url, verify=False)
    fdata = json.loads(r.text)
    version = fdata['results']['mag2_version']   
    return version