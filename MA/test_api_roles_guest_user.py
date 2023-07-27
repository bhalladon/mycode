from common_functions import *

class test_createuser(unittest.TestCase):
            
    def test_a_verify_api_roles_guest_user(self):
        print "Test for creating a user, and then create API keys with role as guest and automatically test \
                their privileges"
        ''' Generate token to create a new user'''
        values = {'username': 'admin', 'password': 'admin'}
        headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
        values = urllib.urlencode(values)
        conn = httplib.HTTPSConnection(ma_ip)
        conn.request("POST", "/rapi/auth/session", values, headers)
        response = conn.getresponse()
        data = response.read()
        fdata =json.loads(data)
        global token
        token = fdata['results']['session_token_string']
        print "Generated token is: " + token
        
    
        ''' Create a new user now '''
        uniquekey = str(int(time.time()))
        user = "rbhalla"+str(uniquekey)
        values = {'username': user, 'ui_password': 'bluecoat', 'ui_roles': 'administrator', 'token' : token}
        headers = {'User-Agent':  'python','Content-type': "application/x-www-form-urlencoded"}
        values = urllib.urlencode(values)
        #conn = httplib.HTTPSConnection(ma_ip)
        conn.request("POST","/rapi/system/users", values, headers)
        response = conn.getresponse()
        data = response.read()
        fdata = json.loads(data)
        uid = fdata['results'][0]['users_uid']
        uid = str(uid).strip()
        print "user created with uid: " + uid
          
        if ("rbhalla"+uniquekey in data):
            print "\nUser with username rbhalla"+uniquekey+" created successfully."
          
        elif ("Specified username already exists" in data):
            print "\nUser rbhalla"+uniquekey+" already existing."
          
        else:
            print "Failed to create user with username rbhalla"+uniquekey
             
        ''' Now create an api keys with role as guest '''
         
        roles_types = ["guest", "observer", "analyst","super-analyst", "sysconfig", "administrator"]
         
        print "Creating API keys with different user roles"
        for roles in roles_types:
            ''' Creating a api key with role guest '''
            values = {"roles": roles, "token": token, "uid": uid}
            headers = {'User-Agent':  'python','Content-type': "application/x-www-form-urlencoded"}
            values = urllib.urlencode(values)
            conn.request("POST","/rapi/system/users/api_keys", values, headers)
            response = conn.getresponse()
            data = response.read()
            fdata = json.loads(data)
            roles_api_key = fdata['results'][0]['api_keys_api_key']
            api_key_guest = str(roles_api_key).strip()
            print "API key with "+ roles + "role access is: " + api_key_guest
                
        ''' Test privileges now '''
                 
        ''' Test view basic system information '''
        values = {}
        headers = {'User-Agent':  'python','Content-type': "application/x-www-form-urlencoded"}
        values = urllib.urlencode(values)
        conn.request("GET","/rapi/system/version_info?token="+api_key_guest, values , headers)
        response = conn.getresponse()
        data = response.read()
        data = str(data).strip().lower()
        if "mag2_version" in data:
            print "[Passed] API key with guest role can access system information."
        else:
            print "[Failed] API key with guest role cannot access system information."
            print self.fail("API key with guest role cannot access system information.")
        conn.close()
        ''' Test System Patterns '''
        values = {}
        headers = {'User-Agent':  'python','Content-type': "application/x-www-form-urlencoded"}
        values = urllib.urlencode(values)
        conn.request("GET","/rapi/pattern_groups?token="+api_key_guest, values , headers)
        response = conn.getresponse()
        data = response.read()
        data = str(data).strip().lower()
        if "revision" and "risk_score" in data:
            print "[Passed] API key with guest role can access system patterns."
        else:
            print "[Failed] API key with guest role cannot access system patterns."
            print self.fail("API key with guest role cannot access system patterns.")
               
        ''' Test patterns created by another user '''
        ''' create a pattern by user admin '''
        name = "test"+ str(uniquekey)
        name = str(name).strip().lower()
        token = str(token).strip()
        values = {'description': 'No description', 'is_enabled': 1, 'is_global': 0, 'owner': 'admin', 'name':name, 'risk_score': 1, 'type': 'simple', 'mode': 'any_of'}
        values = json.dumps(values)
        headers = {'User-Agent': 'python','Content-type': 'application/json'}        
        conn = httplib.HTTPSConnection(ma_ip)
        conn.request("POST", "/rapi/pattern_groups?token="+token, values , headers)
        response = conn.getresponse()
        data = response.read()
        fdata = json.loads(data)
        pattern_uid = fdata['results'][0]
         
        ''' Now try to access the pattern created above by user admin '''
        values = {}
        headers = {'User-Agent':  'python','Content-type': "application/x-www-form-urlencoded"}
        values = urllib.urlencode(values)
        conn.request("GET","/rapi/pattern_groups/"+str(pattern_uid)+"?token="+api_key_guest, values , headers)
        response = conn.getresponse()
        data = response.read()
        data = str(data).strip().lower()
        #print data
        if "http 403: forbidden (insufficient privileges to view this pattern)" in data:
            print "[Passed] API key with guest role can not access patterns created by other users (non-system) ."
        else:
            print "[Failed] API key with guest role can access patterns created by other users (non-system)."
            print self.fail("API key with guest role can access patterns created by other users (non-system).")


if __name__ == '__main__':
    unittest.main()
 
        
