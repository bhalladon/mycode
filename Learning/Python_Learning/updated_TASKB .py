#!/usr/bin/python

import httplib, urllib, json, unittest, time

class token_createuser(unittest.TestCase):

    def test_A_generate_token(self):
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

    def test_B_create_user(self):
        uniquekey = str(int(time.time()))
        user =  "rbhalla"+uniquekey 
        
        values = {'username': user, 'ui_password': 'bluecoat', 'ui_roles': 'administrator', 'token' : token}
        headers = {'User-Agent':  'python','Content-type': "application/x-www-form-urlencoded"}
        values = urllib.urlencode(values)
        conn = httplib.HTTPSConnection("10.138.128.2")
        conn.request("POST","/rapi/system/users", values, headers)
        response = conn.getresponse()
        data = response.read()
         
        if ("rbhalla"+uniquekey in data):
            print "\nUser with username rbhalla"+uniquekey+" created successfully."
        
        elif ("Specified username already exists" in data):
            print "\nUser rbhalla"+uniquekey+" already existing."
        
        else:
            print "Failed to create user with username rbhalla"+uniquekey
            
    def test_C_systemversion(self):
        values = {'token' : token}
        #headers = {'User-Agent': 'python', 'Content-type': "application/x-www-form-urlencoded"}
        values = urllib.urlencode(values)
        conn = httplib.HTTPSConnection("10.138.128.2")
        conn.request("GET", "/rapi/system/version_info?token="+token)
        response =conn.getresponse()
        data = response.read()
        fdata = json.loads(data)
        pattern_version= fdata['results']['patterns_version']
        print pattern_version
        conn.close()
    
if __name__ == '__main__':
    unittest.main()