import requests,json,paramiko,time,os,unittest
import requests.packages.urllib3
from unittest.case import SkipTest
import xmlrunner
#cas_ip=os.getenv("MAG2_RAPI")
cas_ip_no_port=str(os.getenv("MAG2_RAPI")).strip(":8082")
cas_ip="10.199.107.17:8082"
#cas_ip="[fd00:651::ac7:6e47]:8082"
cas_adminuser="admin"
cas_adminpass="admin123"
win7_path=os.getenv("win7_export_base_image")
#win7_path="http://10.199.97.68/casma/exported_base_img_profile/Rajiv/win7_baseImage_profile_automation/win7x64-sp1-base.bundle"
win10_path=os.getenv("win10_export_base_image")
# win10_path="http://[fd00:601::ac7:6144]/casma/exported_base_img_profile/win10x64.b7ccf912d6e34a8410859da4a9eab86f.TY8RT-VNF79-8Q78W-TK32Q-7T9R8.base"
winxp_path=os.getenv("winxp_export_base_image")
profile_build_xp=os.getenv("profile_build_winxp")
profile_build_win7=os.getenv("profile_build_win7")
profile_build_win10=os.getenv("profile_build_win10")
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
requests.packages.urllib3.has_memoryview = False


class casutilities():

    def setUp(self):
        global a
        a = casutilities()
        global token
        token = a.generate_token()
    
    def httpcall(self, call_method, rapicall, values, headers):
        url = str("https://") +str(cas_ip)+ str(rapicall)
        #print url
        call_method = call_method.lower()
        if call_method ==  "get":
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
    
    def getprofileid(self, baseid, token):
        a = casutilities()
        values = {}
        headers = {'X-API-TOKEN': token}
        profileid = []
        results_count = a.httpcall("GET", "/rapi/system/vm/profiles", values, headers)['results_count']
        for x in range(results_count):
            baseid1 = a.httpcall("GET", "/rapi/system/vm/profiles", values, headers)['results'][x]['vm_bases_vmb_id']
            if baseid1 == baseid:
                profileid1 = a.httpcall("GET", "/rapi/system/vm/profiles", values, headers)['results'][x]['vm_profiles_vmp_id']
                profileid.append(profileid1)
            else:
                pass
        return profileid
    
    def sshcmd(self,cas_ip_no_port,command ):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(cas_ip_no_port, 2024, username="clpdebug", password="12345678")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        return (ssh_stdout.read().decode('ascii')).strip()
            
    def addbaseimage_23(self, url, token, timeout,profile_build):
        a = casutilities()
        values = {"url":url}
        headers = {"X-API-TOKEN":token}
        print "profile_build values is: " + str(profile_build)
        if profile_build == "1":
            addbase = a.httpcall("POST", "/rapi/system/vm/pull?queue_if_busy=1&finalize=1&build_profile=1&activate_and_build_profile=1", values=values, headers=headers)['results'][0]['vm_bases_vmb_id']
        else:
            addbase = a.httpcall("POST", "/rapi/system/vm/pull?queue_if_busy=1&finalize=1&build_profile=0&activate_and_build_profile=1", values=values, headers=headers)['results'][0]['vm_bases_vmb_id']
            
        print "New Base image id is: " + str(addbase)
        #### Wait for the base image to be in READY state ####
        status = True
        thinktime=0
        while status == True:
            values = {}
            headers = {"X-API-TOKEN": token}
            image_status = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase), values, headers)['results'][0]['vm_bases_status']
            if image_status == "Ready":
                print "Base image added successfully."
                ### Get profile ID ####
                if profile_build == "1":
                    print "Waiting for profile to be created successfully."
                    g = a.getprofileid(addbase, token)
                    for x in g:
                        while status == True:
                            pro_status = a.httpcall("GET", "/rapi/system/vm/profiles/"+str(x), values, headers)['results'][0]['vm_profiles_status']
                            if pro_status == "Ready":
                                print "Profile is also ready"
                                status = False
                            elif "Failed to build profile" in pro_status:
                                assert False, "Profile build process failed with error" + str(pro_status)
                                break
                            else:
                                pro_progresss = a.httpcall("GET", "/rapi/system/vm/profiles/"+str(x), values, headers)['results'][0]['vm_profiles_progress']
                                print "Profile status is: " + str(pro_status) + " " + str(pro_progresss) + "%"
                                time.sleep(20)
                                thinktime = thinktime + 20
                                print "Thinktime is: " + str(thinktime)
                    if thinktime > timeout:
                                    print "Not able to add profile in alloted time"
                                    assert False, "Not able to add profile in alloted time. " +str(pro_status)
                                    status = False
                elif profile_build == "0":
                    print "Profile building is set to False. Exiting the script."
                    status = False
                                
            else:
                build_progress = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase), values, headers)['results'][0]['vm_bases_progress']
                print "Base image status is: " + str(image_status) + " " + str(build_progress) + "%"
                time.sleep(20)
                thinktime = thinktime + 20
                #print "Thinktime is: " + str(thinktime)
                if thinktime > timeout:
                    print "Not able to add base image in alloted time"
                    status = False

class test_iso_import(unittest.TestCase):
    def setUp(self):
        global a
        a = casutilities()
        global token
        token = a.generate_token()
        global timeout
        timeout = 3000
    
    def test_d(self):
        print token
    
    #@unittest.SkipTest
    def test_a_win7(self):
        if not os.getenv("win7_export_base_image"):
            raise SkipTest()
        print "token is: " + str(token)
        a.addbaseimage_23(win7_path, token, timeout,profile_build_win7)
    
    #@unittest.SkipTest
    def test_b_win10(self):
        if not os.getenv("win10_export_base_image"):
            raise SkipTest()
        print "token is: " + str(token)
        a.addbaseimage_23(win10_path, token, timeout,profile_build_win10)
    
    #@unittest.SkipTest   
    def test_c_winxp(self):
        if not os.getenv("winxp_export_base_image"):
            raise SkipTest()
        print "token is: " + str(token)
        a.addbaseimage_23(winxp_path, token, timeout,profile_build_xp)

if __name__ == '__main__':
    #reportlocation=os.path.join(os.getcwd(),"tests/Reports")
    runner = xmlrunner.XMLTestRunner(output="Reports")
    unittest.main(testrunner=runner) 
    
    
    
    
