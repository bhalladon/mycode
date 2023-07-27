import requests,json,paramiko,time,os,unittest,threading
import requests.packages.urllib3
from unittest.case import SkipTest
cas_ip=os.getenv("MAG2_RAPI")
cas_ip_no_port=str(os.getenv("MAG2_RAPI")).strip(":8082")
cas_ip="10.199.107.17:8082"
cas_ip_no_port="10.199.107.17"
cas_adminuser="admin"
cas_adminpass="admin123"
# winxp_location="http://10.199.97.67/casma/iso_import/base_img_bundle/WINXP-X14-73315.iso"
# win7_location="http://10.199.97.67/casma/iso_import/base_img_bundle/WIN7-x17-58517-39134fad6ccc6292a5e81a5dcedc4d13.iso"
# win10_location="http://10.199.97.67/rajiv/665735baa2d045b09502c7e07837ce51e067f9107c7cbe910717297525aa4888.iso"


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
                #print "Unable to process the request " + str(rapicall)
                #print "HTTP error code is: " + str(r.status_code)
                #print r.text
                return r.text
                return r.status_code
                #pass
        
            
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
    
    def getallprofileid(self,token):
        a = casutilities()
        values = {}
        headers = {'X-API-TOKEN': token}
        profileid = []
        results_count = a.httpcall("GET", "/rapi/system/vm/profiles", values, headers)['results_count']
        for x in range(results_count): 
            try:      
                profileid1 = a.httpcall("GET", "/rapi/system/vm/profiles", values, headers)['results'][x]['vm_profiles_vmp_id']
                profileid.append(profileid1)
            except IndexError:
                pass

        return profileid
    def sshcmd(self,cas_ip_no_port,command ):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(cas_ip_no_port, 22, username="clpdebug", password="12345678")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        return (ssh_stdout.read().decode('ascii')).strip()

    def addiso_pull_23(self, url, key, name, iso_type, token, timeout, profile_build, skip_activation, skip_event_verification, win10_version):
        a = casutilities()
        if "xp" in iso_type:
            print "Adding Windows XP base image"
        elif "win7" in iso_type:
            print "Adding Windows7x64 base image"
        elif "win10" in iso_type:
            print "Adding Windows10x64 base image"
        if skip_activation == "True":
            print "Skipping Activation"
            a.sshcmd(cas_ip_no_port, "df-config-mgr -w ivm.iso_import.skip_activation True")
            a.sshcmd(cas_ip_no_port, "df-config-mgr -w ivm.build.verify.require_activation False")       
        elif skip_activation == "False":
            print "Activation code enabled"
            a.sshcmd(cas_ip_no_port, "df-config-mgr -w ivm.iso_import.skip_activation False")
            a.sshcmd(cas_ip_no_port, "df-config-mgr -w ivm.build.verify.require_activation True")
        if skip_event_verification == "True":
            print "Skipping event verification during profile build"
            a.sshcmd(cas_ip_no_port, "df-config-mgr -w ivm.build.verify.basic_events False")
        else:
            print "Skipping event verification during profile build set to False"
            a.sshcmd(cas_ip_no_port, "df-config-mgr -w ivm.build.verify.basic_events True")
            
          
        ''' Get pattern Version '''
        values = {}
        headers = {"X-API-TOKEN":token}
        system_info = a.httpcall("GET", "/rapi/system/version_info", values, headers)['results']['patterns_version']
        print "Pattern version is: " + str(system_info).strip()
          
        ''' Set a unique name for base image '''
        uniquekey = str(int(time.time()))
        name = str(name) +str(uniquekey)      
        ''' pass data '''
        values = {"product_key":key, "url":url, "display_name": name, "iso_type": iso_type}
        headers = {"X-API-TOKEN":token}
        '''add base image with profile build '''
        if profile_build == 1:
            print "yes"
            addbase = a.httpcall("POST", "/rapi/system/vm/bases/pull_iso?queue_if_busy=1&finalize=1&build_profile=1&activate_and_build_profile=1&use_proxy=0", values=values, headers=headers)['results'][0]['vm_bases_vmb_id']
        else:
            print "no"
            addbase = a.httpcall("POST", "/rapi/system/vm/bases/pull_iso?queue_if_busy=1&finalize=1&build_profile=0&activate_and_build_profile=1&use_proxy=0", values=values, headers=headers)['results'][0]['vm_bases_vmb_id']
            
        print "New Base image id is: " + str(addbase)  
        status = True
        thinktime=0
        while status == True:
            values = {}
            headers = {"X-API-TOKEN": token}
            image_status = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase), values, headers)['results'][0]['vm_bases_status']
            image_progress = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase), values, headers)['results'][0]['vm_bases_progress']
            image_status = str(image_status).lower()
            if image_status == "ready" and image_progress == 100:
                print "Base image added successfully."
                print "Waiting for profile to be created successfully."
                print "Check Profile build is set to true or false"
                print "Profile build state is: " + str(profile_build)
                if profile_build == 1:
                ### Get profile ID ####
                    g = a.getprofileid(addbase, token)
                    print g
                    for x in g:
                        while status == True:
                            pro_status = a.httpcall("GET", "/rapi/system/vm/profiles/"+str(x), values, headers)['results'][0]['vm_profiles_status']
                            pro_status = str(pro_status).lower()
                            if pro_status == "ready":
                                print "Profile is also ready"
                                status = False
                            elif "failed" in pro_status or "error" in pro_status:
                                print "unable to add profile in alloted time. Manual investigation required."
                                print pro_status
                                #raise "Failed to add profile."
                                status = False
                            else:
                                pro_progresss = a.httpcall("GET", "/rapi/system/vm/profiles/"+str(x), values, headers)['results'][0]['vm_profiles_progress']
                                print "Profile status is: " + str(pro_status) + " " + str(pro_progresss) + "%"
                                time.sleep(20)
                                thinktime = thinktime + 20
                                print "Thinktime is: " + str(thinktime)
                                if thinktime > timeout:
                                    print "Not able to add profile in alloted time"
                                    #raise "Unable to add profile in alloted time."
                                    status = False 
                elif str(profile_build).strip() == '0':
                    print "Profile is not required to build."
                    status = False

                return addbase
            elif "awaiting version selection" in image_status:
                casutilities.get_index_number_win10(self, addbase, win10_version, key)
            elif "failed" in image_status or "error" in image_status:
                print "unable to add base image. Manual investigation required."
                print image_status
                raise "Failed to add base image."
            else:
                build_progress = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase), values, headers)['results'][0]['vm_bases_progress']
                print "Base image status is: " + str(image_status) + " " + str(build_progress) + "%"
                time.sleep(20)
                thinktime = thinktime + 20
                #print "Thinktime is: " + str(thinktime)
                if thinktime > timeout:
                    print "Not able to add base image in alloted time"
                    print image_status
                    raise "Unable to add base image in alloted time."
                    status = False

    def get_index_number_win10(self,addbase,win10_version,key):
        #### Get index value for selected Win10 version #####"
        print "Getting index number for selection windows type to install."
        values ={}
        headers = {'X-API-TOKEN': token}
        total_results = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase)+"/iso_selection", values, headers)['results_count']
        print "Total_results is: "+str(total_results)
        index = True
        try:
            while index == True:
                print "check1:"
                for x in range(total_results):
                    print "value of x: "+ str(x)
                    version = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase)+"/iso_selection", values, headers)['results'][x]['display_name']
                    print "version before removing spaces: "+str(version)
                    version = str(version).replace(' ', '')
                    print "version after removing spaces: " + str(version)
                    time.sleep(10)
                    if version == win10_version:
                        print "version matched."
                        print "value of x is: " + str(x)
                        get_index = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase)+str("/iso_selection"), values, headers)['results'][x]['index'] 
                        print "Value of get_index is: "+str(get_index)
                        values = {"version_index":int(get_index), "product_key":key}
                        headers = {"X-API-TOKEN": token}
                        select_version = a.httpcall("POST", "/rapi/system/vm/bases/"+str(addbase)+str("/iso_selection"), values, headers)
                        #print select_version
                        index = False
        except TypeError:
            pass

    def deletevmprofile(self,profile_id_start, profile_id_end, timeout ):
        a = casutilities()
        token = a.generate_token()
        profile_id_end = profile_id_end + 1
        for profile_id in range(profile_id_start, profile_id_end):
            values = {}
            headers = {'X-API-TOKEN': token}
            deleteprofile = a.httpcall("DELETE", "/rapi/system/vm/profiles/"+str(profile_id), values, headers)
            if "404: Not Found" in deleteprofile:
                print "VM profile id "+str(profile_id)+" does not exist."
            
            elif "504" in deleteprofile:
                #print "504"          
                status = True
                thinktime = 0
                while status == True:
                    status_code = [200, 202]
                    deleteprofile = a.httpcall("DELETE", "/rapi/system/vm/profiles/"+str(profile_id), values, headers)
                    if "200" or "202" not in deleteprofile:
                        thinktime = thinktime + 1
                        #print "thinktime: " + str(thinktime)
                        time.sleep(1)
                        if thinktime >=timeout:
                            #print "Thinktime timesout: " + str(thinktime)
                            #print "Unable to delete the profile in specified time: " + str(timeout) + " seconds"
                            status = False
                        pass
                    
                    else:
                        print "VM profile id "+str(profile_id)+" deleted successfully."
                        status = False    
    
class test_iso_import(unittest.TestCase):
    def setUp(self):
        global a
        a = casutilities()
        global token
        token = a.generate_token()
        global timeout
        timeout = 6000
    
    def test_a_delete_vmprofiles(self):
        f = a.getallprofileid(token)
        print f
        threads=list()
        for x in f:
            x = threading.Thread(target=a.deletevmprofile, args=(x,x,30, ))
            threads.append(x)
            x.start()
            if len(threads) % 100 == 0:
                while x.isAlive():
                    pass
        for x in threads:
            x.join(timeout=12)
        print "All profiles deleted successfully"
        #for x in f:
        #    a.deletevmprofile(x,x,30)
        
    def test_win7_iso_import(self):
        ###### Win7 Import ########
        if not os.getenv("win7_location"):
            print "Windows 7 ISO location not defined. Not proceeding with Win7 ISO IMPORT."
            raise SkipTest()
        else:
            url = os.getenv("win7_location")
            key = os.getenv("win7_key")
            iso_type = "win7x64-sp1"
            ''' Set a unique name for base image '''
            name ="testwin7"
            win10_version=""
            uniquekey = str(int(time.time()))
            name = str(name) +str(uniquekey)
            profile_build = 1
            skip_activation = os.getenv("skip_activation_win7")
            print "skip activation: " +str(skip_activation)
            skip_event_verification = os.getenv("skip_event_verification_win7")
            a.addiso_pull_23(url, key, name, iso_type, token, timeout, profile_build, skip_activation,skip_event_verification,win10_version)
   
    def test_win10_iso_import(self):
        ###### Win10 Import ########
        if not os.getenv("win10_location"):
            print "Windows 10 ISO location not defined. Not proceeding with Win10 ISO IMPORT."
            #win10_location="http://10.199.97.67/rajiv/665735baa2d045b09502c7e07837ce51e067f9107c7cbe910717297525aa4888.iso"
            raise SkipTest()
        else:
            url = os.getenv("win10_location")
            key = os.getenv("win10_key")
            iso_type = "win10x64"
            win10_version = os.getenv("win_10_version")
            ''' Set a unique name for base image '''
            name ="testwin10"
            uniquekey = str(int(time.time()))
            name = str(name) +str(uniquekey)
            profile_build = 1
            skip_activation = os.getenv("skip_activation_win10")
            print "skip activation: " +str(skip_activation)
            skip_event_verification = os.getenv("skip_event_verification_win10")
            a.addiso_pull_23(url, key, name, iso_type, token, timeout, profile_build, skip_activation,skip_event_verification,win10_version)

    def test_winxp_iso_import(self):
        ###### WinXP Import ########
        if not os.getenv("winxp_location"):
            print "Windows XP ISO location not defined. Not proceeding with WinXP ISO IMPORT."
            #winxp_location="http://10.199.97.67/casma/iso_import/base_img_bundle/WINXP-X14-73315.iso"
            raise SkipTest()
        else:
            url = os.getenv("winxp_location")
            key = os.getenv("winxp_key")
            iso_type = "winxp-sp3"
            ''' Set a unique name for base image '''
            name ="testwinxp"
            win10_version=""
            uniquekey = str(int(time.time()))
            name = str(name) +str(uniquekey)
            profile_build = 1
            skip_activation = os.getenv("skip_activation_winxp")
            print "skip activation: " +str(skip_activation)
            skip_event_verification = os.getenv("skip_event_verification_winXP")
            a.addiso_pull_23(url, key, name, iso_type, token, timeout, profile_build, skip_activation,skip_event_verification,win10_version)

        
if __name__ == '__main__':
    unittest.main() 
    
    
    
    
