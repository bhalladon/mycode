#!/usr/bin/python

import httplib, urllib, json

def generate_token():
    values = {'username': 'admin', 'password': 'admin'}
    headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
    values = urllib.urlencode(values)
    conn = httplib.HTTPSConnection("10.138.128.2")
    conn.request("POST", "/rapi/auth/session", values, headers)
    response = conn.getresponse()
    data = response.read()
    fdata =json.loads(data)
    global token
    token = fdata['results']['session_token_string']
    print "Generated token is: " + token
    conn.close()

def create_user():
    values = {'token' : token} 
    #values = {'username': 'rbhalla', 'ui_password': 'bluecoat', 'ui_roles': 'administrator', 'token' : token}
    headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
    values = urllib.urlencode(values)
    conn = httplib.HTTPSConnection("10.138.128.2")
    conn.request("GET","/rapi/system/version_info?token="+token, values, headers)
    response = conn.getresponse()
    data = response.read()
    print data
    
    if ('"users_username": "rbhalla"' in data):
        print "\n\nUser with username rbhalla created successfully."
    else:
        print "Failed to create user with username 'rbhalla'"
    
    conn.close()

generate_token()
create_user()    