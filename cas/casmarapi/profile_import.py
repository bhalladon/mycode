import unittest, time,json
import requests.packages.urllib3
import paramiko
from paramiko_expect import SSHClientInteraction


try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
requests.packages.urllib3.has_memoryview = False

cas_ip="10.199.107.17:8082"
cas_ip_no_port = str(cas_ip).replace(":8082", '')
cas_adminuser="admin"
cas_adminpass="admin123"
url="http://10.199.97.68/casma/exported_base_img_profile/Rajiv/Win7_base_profile_withoffice2016/bin"

class casutilities():
    def generate_token(self):
        a = casutilities()
        values = {"username":cas_adminuser, "password":cas_adminpass}
        headers = {"User-Agent":"python"}
        token = a.httpcall("POST", "/rapi/auth/session", values, headers)['results']['session_token_string']
        return token
    
    def httpcall(self, call_method, rapicall, values, headers):
        url = "https://" +cas_ip+ rapicall
        call_method = call_method.lower()
        if call_method ==  "get":
            r = requests.get(url, data=values, headers=headers, verify=False)
        if call_method == "post":
            print url
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
                print r.text
                return r.text
                return r.status_code
    
    
    def sshcmd_cli_profile_import(self,cas_ip_no_port,url):
        file = open("testlog.txt","w")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(cas_ip_no_port, 22, username="admin", password="admin123")
        interact = SSHClientInteraction(ssh,timeout=10,display=True)
        interact.expect('.*CAS>.*')
        interact.send('en')
        interact.expect('.*Password:.*')
        interact.send('admin')
        interact.expect('.*CAS#.*')
        interact.send('ma-actions profiles imports download validate_cert 0 overwrite 1')
        interact.expect('.*Value for.*')
        interact.send(url)
        interact.expect('.*yes.*')
        interact.send('yes')
        time.sleep(10)
        interact.send('ma-actions profiles list')  
        file.write(interact.current_output)
        ssh.close()
    
    
    def buildvmprofile(self, profile_id_start, profile_id_end, token, timeout):
        a = casutilities
        profile_id_end = profile_id_end + 1
        for x in range(profile_id_start, profile_id_end):
            print "\nStart time: " + str(time.ctime())
            url = "https://" + str(cas_ip) + str("/rapi/system/vm/profiles/"+str(x)+"/build")
            values = {}
            headers = {'X-API-TOKEN': token}
            r = requests.post(url, data=values, headers=headers, verify=False)
            if r.status_code in [200, 201]:
                thinktime = 0
                status = True
                while status == True:
                    url = "https://" + str(cas_ip) + str("/rapi/system/vm/profiles/"+str(x))
                    values = {}
                    headers = {'X-API-TOKEN': token}
                    r = requests.get(url, data=values, headers=headers, verify=False)
                    profile_state = json.loads(r.text)['results'][0]['vm_profiles_status']
                    profile_progress = json.loads(r.text)['results'][0]['vm_profiles_progress']
                    profile_state = str(profile_state).lower()
                    if profile_state == "ready" and profile_progress == 100:
                        print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
                        print "Profile build-ed successfully." + "\n"
                        print "End time: " + str(time.ctime()) + "\n"
                        status = False

                    elif "failed" in profile_state or "error" in profile_state:
                        print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
                        assert False, profile_state
                    
                    elif profile_state != "ready" and profile_progress != 100:
                        print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
                        time.sleep(30)
                        thinktime = thinktime + 30
                        print "thinktime value" + str(thinktime)
                        if thinktime > timeout:
                            print "Profile not re-builded in given time: "+ str(timeout) + " seconds"
                            assert False, profile_state
                               
            if r.status_code in [504]:
                status = True
                thinktime = 0                
                while status == True:
                    r = requests.post(url, data=values, headers=headers, verify=False)
                    if r.status_code in [504]:
                        time.sleep(1)
                        thinktime = thinktime + 1
                        if thinktime > timeout:
                            print "IntelliVM Control Service remains busy. Unable to build profile in given time."
                        else:
                            pass
                    if r.status_code in [200, 201]:
                        thinktime = 0
                        status = True
                        while status == True:
                            url = "https://" + str(cas_ip) + str("/rapi/system/vm/profiles/"+str(x))
                            values = {}
                            headers = {'X-API-TOKEN': token}
                            r = requests.get(url, data=values, headers=headers, verify=False)
                            profile_state = json.loads(r.text)['results'][0]['vm_profiles_status']
                            profile_progress = json.loads(r.text)['results'][0]['vm_profiles_progress']
                            profile_state = str(profile_state).lower()
                            if profile_state == "ready" and profile_progress == 100:
                                print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
                                print "Profile build-ed successfully." + "\n"
                                print "End time: " + str(time.ctime()) + "\n"
                                status = False
                                         
        #                         pass
                            elif "failed" in profile_state or "error" in profile_state:
                                print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
                                assert False, profile_state
                            
                            elif profile_state != "ready" and profile_progress != 100:
                                print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
                                time.sleep(30)
                                thinktime = thinktime + 30
                                print "thinktime value" + str(thinktime)
                                if thinktime > timeout:
                                    print "Profile not re-builded in given time: "+ str(timeout) + " seconds"
                                    assert False, profile_state



    def get_profile_id(self,token):
        a = casutilities()
        values={}
        headers={"X-API-TOKEN":token}
        f = a.httpcall("GET", "/rapi/system/vm/profiles", values, headers)['results_count']
        for x in range(f):
            g = a.httpcall("GET", "/rapi/system/vm/profiles", values, headers)['results'][x]['vm_profiles_status']
            if "Downloading" in g:
                pro_id = a.httpcall("GET", "/rapi/system/vm/profiles", values, headers)['results'][x]['vm_profiles_vmp_id']
                '''now wait for the profile to be in ready state'''
                a.buildvmprofile(pro_id, pro_id, token, 2000)
#         file = open("testlog.txt","w")
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(cas_ip_no_port, 22, username="admin", password="admin123")
#         interact = SSHClientInteraction(ssh,timeout=10,display=True)
#         interact.expect('.*CAS>.*')
#         interact.send('en')
#         interact.expect('.*Password:.*')
#         interact.send('admin')
#         interact.expect('.*CAS#.*')
#         interact.send('ma-actions profiles list')
#         interact.send('exit')
#         time.sleep(4)
#         file.write(interact.current_output)
#         if "Downloading" in interact.current_output:
#             print "Profile import process started successfully."
#         else:
#             print interact.current_output
#             print "Failed to start the profile import process."
            

class test_systeminfo(unittest.TestCase):

    def setUp(self):
        global a
        a = casutilities()
        global token
        token = a.generate_token()
    
    def test_a_import_profile(self):
        a.sshcmd_cli_profile_import(cas_ip_no_port, url)
        #a.get_profile_id(token)
    
if __name__ == '__main__':
    unittest.main()
        
