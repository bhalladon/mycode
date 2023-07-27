import requests,json,paramiko,time,os,unittest,threading
import requests.packages.urllib3
from unittest.case import SkipTest
cas_ip=os.getenv("MAG2_RAPI")
cas_ip_no_port=str(os.getenv("MAG2_RAPI")).strip(":8082")
#cas_ip="10.199.107.17:8082"
#cas_ip_no_port="10.199.107.17"
cas_adminuser="admin"
cas_adminpass="admin123"
win7_baseid=os.getenv("win7_baseid")
win10_baseid=os.getenv("win10_baseid")
winxp_baseid=os.getenv("winxp_baseid")
win7_howmanyprofiles=int(os.getenv("win7_howmanyprofiles"))
win10_howmanyprofiles=int(os.getenv("win10_howmanyprofiles"))
winxp_howmanyprofiles=int(os.getenv("winxp_howmanyprofiles"))
#winxp_location="http://10.199.97.67/casma/iso_import/base_img_bundle/WINXP-X14-73315.iso"


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
      
    def sshcmd(self,cas_ip_no_port,command ):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(cas_ip_no_port, 2024, username="clpdebug", password="12345678")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        return (ssh_stdout.read().decode('ascii')).strip()

    def createvmprofile(self, baseid, howmanyprofiles, token):
        profileid=[]
        for x in range(howmanyprofiles):
            uniquekey = str(int(time.time()))
            newprofilename = "test"+str(uniquekey)
            shortname = "short"+str(uniquekey) 
            url = "https://" + str(cas_ip) + str("/rapi/system/vm/profiles")
            values = {'vmb_id':baseid, 'name':newprofilename,'short_name':shortname}
            headers = {'X-API-TOKEN': token}
            r = requests.post(url, data=values, headers=headers, verify=False)
            if r.status_code == 400:
                print r.text
                print "[Failed] Unable to create a vm profile needed to perform delete function. Need Manual investigation."
                print self.fail("Failed")
            elif r.status_code == 403:
                print "[Failed] Unable to create a vm profile needed to perform delete function. Need Manual investigation."
            elif r.status_code == 200:
                data = r.text
                fdata = json.loads(data)
                profile_id = fdata['results'][0]['vm_profiles_vmp_id']
                print "profile id is: " + str(profile_id)
                profileid.append(profile_id)
                time.sleep(2)
            
            elif r.status_code == 504:
                status = True
                while status == True:
                    time.sleep(5)
                    r = requests.post(url, data=values, headers=headers, verify=False)
                    if r.status_code == 200:
                        data = r.text
                        fdata = json.loads(data)
                        profile_id = fdata['results'][0]['vm_profiles_vmp_id']
                        print "profile id is: " + str(profile_id)
                        profileid.append(profile_id)
                        status = False
                        
                    if r.status_code == 500:
                        print r.text
        if profileid:
            return profileid
        
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
                        #assert False, profile_state
                        print profile_state
                        status = False
                    elif profile_state != "ready" and profile_progress != 100:
                        print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
                        time.sleep(30)
                        thinktime = thinktime + 30
                        print "thinktime value" + str(thinktime)
                        if thinktime > timeout:
                            print "Profile not re-builded in given time: "+ str(timeout) + " seconds"
                            #assert False, profile_state
                            print profile_state
                            status = False
                    
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

                            elif "failed" in profile_state or "error" in profile_state:
                                print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
                                #assert False, profile_state
                                print profile_state
                                status = False
                            
                            elif profile_state != "ready" and profile_progress != 100:
                                print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
                                time.sleep(30)
                                thinktime = thinktime + 30
                                print "thinktime value" + str(thinktime)
                                if thinktime > timeout:
                                    print "Profile not re-builded in given time: "+ str(timeout) + " seconds"
                                    #assert False, profile_state
                                    print profile_state
                                    status = False

class test_profile_build(unittest.TestCase):
    def setUp(self):
        global a
        a = casutilities()
        global token
        token = a.generate_token()

    def test_win7_profile_build(self):
        if os.getenv("win7_baseid"):
            f = a.createvmprofile(win7_baseid, win7_howmanyprofiles, token)
            for x in f:
                a.buildvmprofile(x, x, token, 1200)
        else:
            print "Windows 7 base id not defined. Not proceeding with profile build."
            raise SkipTest()
            
   
    def test_win10_profile_build(self):
        if os.getenv("win10_baseid"):
            f = a.createvmprofile(win10_baseid, win10_howmanyprofiles, token)
            for x in f:
                a.buildvmprofile(x, x, token, 1200)
        else:
            print "Windows 10 base id not defined. Not proceeding with profile build."
            raise SkipTest()
 
    def test_winxp_profile_build(self):
        if os.getenv("winxp_baseid"):
            f = a.createvmprofile(winxp_baseid, winxp_howmanyprofiles, token)
            for x in f:
                a.buildvmprofile(x, x, token, 1200)
        else:
            print "Windows XP base id not defined. Not proceeding with profile build."
            raise SkipTest()
        ###### WinXP Import ########

if __name__ == '__main__':
    unittest.main() 
    
    
    
    

