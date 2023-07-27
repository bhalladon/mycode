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
        headers = {'User-Agent':  'python','Content-type': "application/x-www-form-urlencoded", 'token': token}
        #values = urllib.urlencode(values)
        conn = httplib.HTTPSConnection("10.138.128.2")
        conn.request("GET","/rapi/tasks/1")
        response = conn.getresponse()
        data = response.read()
        print data
        #fdata = json.loads(data)
        #md5 = fdata['results'][0]['sample_resources']['24']['sample_resources_md5']
        #print md5
          
        #if ("rbhalla"+uniquekey in data):
        #    print "\nUser with username rbhalla"+uniquekey+" created successfully."
         
        #elif ("Specified username already exists" in data):
        #    print "\nUser rbhalla"+uniquekey+" already existing."
         
        #else:
        #    print "Failed to create user with username rbhalla"+uniquekey
        #print data
        conn.close()
    
if __name__ == '__main__':
    unittest.main()