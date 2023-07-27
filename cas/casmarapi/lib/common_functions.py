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
import threading
import socket

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
requests.packages.urllib3.has_memoryview = False

class casutilities():
        
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
    
    def sshcmd_cli(self,cas_ip_no_port,config,command):
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
        if config == "yes":
            interact.send('configure')
            interact.expect('.*Enter.*')
            #interact.expect('.*config.*')
            #interact.send('show version')
            #interact.send('exit')
            #print "ty"
            for x in command:
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(x,timeout=20)
                print (ssh_stdout.read().decode('ascii')).strip()
            #interact.send(command)
        elif config == "no":
            interact.send('ma-actions profiles imports download validate_cert 0 overwrite 1')
            interact.expect('.*Value for.*')
                #print "true"
            interact.send('http://10.199.97.68/casma/exported_base_img_profile/Rajiv/Win7_base_profile_withoffice2016/bin')
            interact.expect('.*yes.*')
            interact.send('yes')
            time.sleep(10)
            interact.send('ma-actions profiles list')
                
            #print (ssh_stdout.read().decode('ascii')).strip()            #try:
            #interact.send('ma-actions profiles imports download validate_cert 0 url http://10.199.97.68/casma/exported_base_img_profile/Rajiv/Win7_base_profile_withoffice2016/bin')
            #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command,timeout=10)
            #except socket.timeout:
            #return (ssh_stdout.read().decode('ascii')).strip()
            #return (ssh_stdout.read().decode('ascii')).strip()
            #interact.send(command)
        time.sleep(2)
            
        file.write(interact.current_output)
        ssh.close()
    
    def sshcmd_cli_upgrade(self,cas_ip_no_port,config,command):
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
#         if config == "yes":
#             interact.send('configure')
#             interact.expect('.*Enter.*')
#             #interact.expect('.*config.*')
#             #interact.send('show version')
#             #interact.send('exit')
#             #print "ty"
#             for x in command:
#                 ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(x,timeout=20)
#                 print (ssh_stdout.read().decode('ascii')).strip()
#             #interact.send(command)
#         elif config == "no":
        interact.send(command)
        interact.expect('.*1.*')    
            #print (ssh_stdout.read().decode('ascii')).strip()            #try:
            #interact.send('ma-actions profiles imports download validate_cert 0 url http://10.199.97.68/casma/exported_base_img_profile/Rajiv/Win7_base_profile_withoffice2016/bin')
            #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command,timeout=10)
            #except socket.timeout:
            #return (ssh_stdout.read().decode('ascii')).strip()
            #return (ssh_stdout.read().decode('ascii')).strip()
            #interact.send(command)
        time.sleep(2)
            
        file.write(interact.current_output)
        ssh.close()
        
    def sshcmd_cli_sg(self,proxy_ip,config,command):
        file1 = open("testlog.txt","w")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(proxy_ip, 22, username="admin", password="admin")
        interact = SSHClientInteraction(ssh,timeout=10,display=True)
        interact.expect('.*Blue Coat.*')
        interact.send('en')
        interact.expect('.*Password:.*')
        interact.send('admin')
        interact.expect('.*Blue Coat.*')
        time.sleep(1)
        interact.send('sdf')
        print "test12"
#         if config == "yes":
#             print("ok")
#             interact.send('configure')
#             interact.expect('.*Enter.*')
#             interact.send(command)
#         else:
#             print("chakde")
#             interact.send(command)
        time.sleep(2) 
        file1.write(interact.current_output)
        ssh.close()
    
    def download_license(self):
        print("Check license status before starting downloading")
        
    def get_iso_baseid(self, isotype, token):
        a = casutilities()
        headers = {"X-API-TOKEN": token}
        values = {}
        g = a.httpcall("GET","/rapi/system/vm/bases/isos", values, headers)
        print g
        f = a.httpcall("GET","/rapi/system/vm/bases/isos", values, headers)['results_count']
        for x in range(f):
            os = a.httpcall("GET","/rapi/system/vm/bases/isos", values, headers)['results'][x]['iso_type']
            if os == isotype:
                baseid = a.httpcall("GET","/rapi/system/vm/bases/isos", values, headers)['results'][x]['base_id']
                #print "Base id of " + str(isotype) + " is: " +str(baseid)
                break
            else:
                pass
        return baseid
    
    def get_download_iso_aws_link(self, baseid, token):
        a = casutilities()
        headers = {"X-API-TOKEN": token}
        values = {}
        download_link = a.httpcall("GET", "/rapi/system/vm/bases/isos/"+str(baseid)+"/download_url", values, headers)['results'][0]
        return download_link

    def download_iso_aws(self,download_link):
        #headers = {}
        #values = {}
        local_filename = download_link.split('/')[-1]
        r = requests.get(download_link, stream=True)
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return local_filename
    
    def get_profile_export_id(self, profileid,token):
        a=casutilities()
        #values = {}
        values = {'vmp_id':profileid}
        headers={'X-API-TOKEN': token}
        #result_count = a.httpcall("GET", "/rapi/system/vm/profiles/export", values, headers)['results_count']
        #print result_count
        export_id = a.httpcall("POST", "/rapi/system/vm/profiles/export", values, headers)['results'][0]['vm_exports_vme_id']
        return str(export_id)
        
    def installlanguage(self,profileid, langname, token, timeout):
        a = casutilities()
        url = "https://" + str(cas_ip) + str("/rapi/system/vm/profiles/"+str(profileid)+"/language")
        values = {'language':langname}
        headers = {'X-API-TOKEN': token}
        r = requests.post(url, data = values, headers=headers, verify= False )
        #print r.text
        #print r.status_code
        if r.status_code in [200,201]:
            print "check1"
            time.sleep(20)
            status = True
            thinktime=0
            while status == True:
                values = {}
                headers = {'X-API-TOKEN':token}
                prostatus = a.httpcall("GET", '/rapi/system/vm/profiles/'+str(profileid), values, headers)['results'][0]['vm_profiles_status']
                if prostatus == "Ready":
                    print "Profile status is: " + str(prostatus)
                    print "Language Pack Installed Successfully.\n"
                    status = False
                
                elif prostatus == "Building":
                    progstatus = a.httpcall("GET", '/rapi/system/vm/profiles/'+str(profileid), values, headers)['results'][0]['vm_profiles_progress']
                    print "Profile status is: " + str(prostatus) + " at " +  str(progstatus)
                    time.sleep(20)
                    thinktime = thinktime + 20
                    if thinktime > timeout:
                        print "Timeout installing language pack.\n"
                        status = False                   
                else:
                    print "Profile status is: " + str(prostatus)
                    time.sleep(20)
                    thinktime = thinktime + 20
                    if thinktime > timeout:
                        print "Timeout installing language pack.\n"
                        status = False
        
        elif r.status_code in [504]:
            print "check2"
            status = True
            thinktime = 0
            timeout = 60                
            while status == True:
                r = requests.post(url, data = values, headers=headers, verify= False )
                if r.status_code in [200,201]:
                    time.sleep(20)
                    status = True
                    thinktime=0
                    while status == True:
                        values = {}
                        headers = {'X-API-TOKEN':token}
                        prostatus = a.httpcall("GET", '/rapi/system/vm/profiles/'+str(profileid), values, headers)['results'][0]['vm_profiles_status']
                        if prostatus == "Ready":
                            print "Profile status is: " + str(prostatus)
                            print "Language Pack Installed Successfully.\n"
                            status = False
                        
                        elif prostatus == "Building":
                            progstatus = a.httpcall("GET", '/rapi/system/vm/profiles/'+str(profileid), values, headers)['results'][0]['vm_profiles_progress']
                            print "\nProfile status is: " + str(prostatus) + " at " +  str(progstatus)
                            time.sleep(20)
                            thinktime = thinktime + 20
                            if thinktime > timeout:
                                print "Timeout installing language pack.\n"
                                status = False                   
                        else:
                            print "Profile status is: " + str(prostatus)
                            time.sleep(20)
                            thinktime = thinktime + 20
                            if thinktime > timeout:
                                print "Timeout installing language pack.\n"
                                status = False                    
                elif r.status_code in [504]:
                    time.sleep(1)
                    thinktime = thinktime + 1
                    if thinktime > timeout:
                        print "IntelliControl Service busy for more than a minute."
                        print "Exiting the script."
                        status = False
                
                elif r.status_code in [400, 404]:
                    print "Error installing language pack.\n"
                    print r.status_code
                    print r.text
                    
        elif r.status_code in [400, 404]:
            print "Error installing language pack.\n"
            print r.status_code
            print r.text
                                
    def geinstalledlang(self, profileid, token):
        a = casutilities()
        values = {}
        headers = {'X-API-TOKEN': token}
        lang  = a.httpcall("GET", "/rapi/system/vm/profiles/"+str(profileid), values, headers)['results'][0]['vm_profiles_language']
        return lang
    
    def getsupportedlangpacks(self, token): 
        a = casutilities()
        values = {}
        headers = {'X-API-TOKEN': token}
        supported_lang_pack = a.httpcall("GET", "/rapi/system/vm/profiles/language", values, headers)['results_count']
        listlang=[]
        for x in range(supported_lang_pack):
            f = a.httpcall("GET", "/rapi/system/vm/profiles/language", values, headers)['results'][x]['code']
            listlang.append(f)
        return listlang
        #x2.update(supported_lang_pack)
        #print x2
        #x1.append(x2.values())
        #print x1
        #for item in x1[0]:
        #    x3.append(item)
        #return x3
    
    def gettaskstate(self, taskid, token):
        a = casutilities()
        values = {}
        headers = {'X-API-TOKEN': token}
        task_state = a.httpcall("GET", "/rapi/tasks/"+str(taskid), values, headers)['results'][0]['task_state_state']
        return task_state
    
    def gettaskevents(self,taskid,type,token):
        a = casutilities()
        values = {}
        headers = {'X-API-TOKEN': token}
        try:
            task_events = a.httpcall("GET", "/rapi/tasks/"+str(taskid)+"/events", values, headers)['results'][type]
        #task_events = json.dumps(task_events)
            item_dict = task_events
            print len(item_dict)
            return len(item_dict)
        except TypeError:
            print "Task Error"
            result = "Task Error"
            return result
        except KeyError:
            print 0
            result = 0
            return result
    
    def getmataskevents(self,taskid,type,token):
        a = casutilities()
        values = {}
        headers = {}
        try:
            task_events = a.httpcall("GET", "/rapi/tasks/"+str(taskid)+"/events?token="+str(token), values, headers)['results'][type]
        #task_events = json.dumps(task_events)
            item_dict = task_events
            print len(item_dict)
            return task_events
        except TypeError:
            print "Task Error"
        except KeyError:
            print 0
            
    
    def  getprofileid(self, baseid, token):
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

    
        
    def addbaseimage(self, url, key, token, timeout):
        a = casutilities()
        values = {"product_key":key, "url":url}
        headers = {"X-API-TOKEN":token}
        addbase = a.httpcall("POST", "/rapi/system/vm/pull?queue_if_busy=1&finalize=1&build_profile=1&activate_and_build_profile=1", values=values, headers=headers)['results'][0]['vm_bases_vmb_id']
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
                print "Waiting for profile to be created successfully."
                ### Get profile ID ####
                g = a.getprofileid(addbase, token)
                for x in g:
                    while status == True:
                        pro_status = a.httpcall("GET", "/rapi/system/vm/profiles/"+str(x), values, headers)['results'][0]['vm_profiles_status']
                        if pro_status == "Ready":
                            print "Profile is also ready"
                            status = False
                        else:
                            pro_progresss = a.httpcall("GET", "/rapi/system/vm/profiles/"+str(x), values, headers)['results'][0]['vm_profiles_progress']
                            print "Profile status is: " + str(pro_status) + " " + str(pro_progresss) + "%"
                            time.sleep(20)
                            thinktime = thinktime + 20
                            print "Thinktime is: " + str(thinktime)
                if thinktime > timeout:
                                print "Not able to add profile in alloted time"
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

    def addbaseimage_23(self, url, token, timeout):
        a = casutilities()
        values = {"url":url}
        headers = {"X-API-TOKEN":token}
        addbase = a.httpcall("POST", "/rapi/system/vm/pull?queue_if_busy=1&finalize=1&build_profile=1&activate_and_build_profile=1", values=values, headers=headers)['results'][0]['vm_bases_vmb_id']
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
                print "Waiting for profile to be created successfully."
                ### Get profile ID ####
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
                                
            else:
                build_progress = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase), values, headers)['results'][0]['vm_bases_progress']
                print "Base image status is: " + str(image_status) + " " + str(build_progress) + "%"
                time.sleep(20)
                thinktime = thinktime + 20
                #print "Thinktime is: " + str(thinktime)
                if thinktime > timeout:
                    print "Not able to add base image in alloted time"
                    status = False                    
                    
    def addiso_pull_23(self, url, key, name, iso_type, token, timeout, profile_build, skip_activation):
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
#       addbase = 29
        status = True
        thinktime=0
        while status == True:
            values = {}
            headers = {"X-API-TOKEN": token}
            image_status = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase), values, headers)['results'][0]['vm_bases_status']
            image_progress = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase), values, headers)['results'][0]['vm_bases_progress']
            if image_status == "Ready" and image_progress == 100:
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
                                raise "Failed to add profile."
                                #status = False
                            else:
                                pro_progresss = a.httpcall("GET", "/rapi/system/vm/profiles/"+str(x), values, headers)['results'][0]['vm_profiles_progress']
                                print "Profile status is: " + str(pro_status) + " " + str(pro_progresss) + "%"
                                time.sleep(20)
                                thinktime = thinktime + 20
                                print "Thinktime is: " + str(thinktime)
                                if thinktime > timeout:
                                    print "Not able to add profile in alloted time"
                                    raise "Unable to add profile in alloted time."
                                    #status = False 
                elif str(profile_build).strip() == '0':
                    print "Profile is not required to build."
                    status = False

                return addbase
            
            else:
                build_progress = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase), values, headers)['results'][0]['vm_bases_progress']
                print "Base image status is: " + str(image_status) + " " + str(build_progress) + "%"
                time.sleep(20)
                thinktime = thinktime + 20
                #print "Thinktime is: " + str(thinktime)
                if thinktime > timeout:
                    print "Not able to add base image in alloted time"
                    status = False

    def addiso_post_23(self, url, key, name, iso_type, token, timeout):
        a = casutilities()
        values = {"product_key":key, "url":url, "display_name": name, "iso_type": iso_type}
        headers = {"X-API-TOKEN":token}
        print "1"
        addbase = a.httpcall("POST", "/rapi/system/vm/bases/post_iso?queue_if_busy=1&finalize=1&build_profile=1&activate_and_build_profile=1", values=values, headers=headers)['results'][0]['vm_bases_vmb_id']
        print addbase
        "print 2"
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
                print "Waiting for profile to be created successfully."
                ### Get profile ID ####
                g = a.getprofileid(addbase, token)
                for x in g:
                    while status == True:
                        pro_status = a.httpcall("GET", "/rapi/system/vm/profiles/"+str(x), values, headers)['results'][0]['vm_profiles_status']
                        if pro_status == "Ready":
                            print "Profile is also ready"
                            status = False
                        else:
                            pro_progresss = a.httpcall("GET", "/rapi/system/vm/profiles/"+str(x), values, headers)['results'][0]['vm_profiles_progress']
                            print "Profile status is: " + str(pro_status) + " " + str(pro_progresss) + "%"
                            time.sleep(20)
                            thinktime = thinktime + 20
                            print "Thinktime is: " + str(thinktime)
                if thinktime > timeout:
                                print "Not able to add profile in alloted time"
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

     
    def getsample_resourceid(self, sample_id, token):
        a = casutilities()
        values = {'sample_id': sample_id}
        headers = {'X-API-TOKEN': token}
        for x in a.httpcall("GET", "/rapi/samples/"+str(sample_id), values, headers)['results'][0]['sample_resources']:
            h =x.strip();    
        resource_id = a.httpcall("GET", "/rapi/samples/"+str(sample_id), values, headers)['results'][0]['sample_resources'][h]['sample_resources_resource_id']
        return resource_id
    
    def download_sample(self, sample_id, token):
        a = casutilities()
        resourceid = a.getsample_resourceid(sample_id)
        url = 'https://'+cas_ip+'/rapi/samples/resources/'+str(resourceid)+'/bin'
        r = requests.get(url, verify=False)
               
    def check_task_resource(self, taskid,token):
        a = casutilities()
        values = {'task_id':taskid}
        headers = {'X-API-TOKEN': token}
        for x in itertools.count():
            try:
                f = a.httpcall("GET", "/rapi/tasks/"+str(taskid)+"/resources", values, headers)['results'][x]['task_resources_file_name'] 
            except IndexError:
                print "NO"
                result = "NO"
                return result
                break
            if str(f).startswith("vm_at_vm_reset") and str(f).endswith(".png"): 
                print "BSOD"
                result = "BSOD"
                return result
                break
            else:
                pass
    
    def gettask_logs(self, taskid, token):
        a = casutilities()
        '''check if task id exist or not '''
        for x in itertools.count():
            values={}
            headers={'x-api-token': token}
            resultcount = a.httpcall("GET","/rapi/tasks?limit=100000",values,headers)['results_count']
            taskidlist=[]
            for x in range(resultcount):
                taskid_list = a.httpcall("GET","/rapi/tasks?limit=100000",values,headers)['results'][x]['tasks_task_id']
                taskidlist.append(taskid_list)
            if taskid in taskidlist:
                break
            else:
                print "Task ID: " + str(taskid) + " does not exist."
                sys.exit()
                
                
        values = {'task_id':taskid}
        headers = {'X-API-TOKEN': token}
        for x in itertools.count():
            try:
                f = a.httpcall("GET", "/rapi/tasks/"+str(taskid)+"/resources", values, headers)['results'][x]['task_resources_file_name']    
            except IndexError:
                print "Task ID present but it does contain any log file."
                sys.exit()
            if str(f).startswith("task") and str(f).endswith(".log"):
                resource_id = a.httpcall("GET", "/rapi/tasks/"+str(taskid)+"/resources", values, headers)['results'][x]['task_resources_resource_id']
                break
            else:
                pass
                #print "Task ID present but it does contain any log file."
                #sys.exit()
        
        values = {}
        headers = {'X-API-TOKEN': token}
        rapi_call="/rapi/resources/"+str(resource_id)+"/bin"
        url = "https://" +cas_ip+ rapi_call
        tasklogs = requests.get(url, data=values, headers = headers, verify=False )
        log = open ("../tasklogs/"+str(taskid)+"_task.txt", "w")
        log.write(str(tasklogs.text))
        log.close()
        print tasklogs.text
        
    
    def create_url_task(self, url, profileid,plugin, token):
        sample_id_list = []
        values = {'url': url, 'owner': 'admin'}
        headers = {'X-API-TOKEN': token}
        sample_id = casutilities.httpcall(self,"post", "/rapi/samples/url", values, headers)['results'][0]['samples_sample_id']
        sample_id_list.append(sample_id)
        for sample_id in sample_id_list:
            casutilities.create_task(self, sample_id,profileid,plugin,token)
            
    def cas_systeminfo(self,cas_ip, token):
        url = "https://" +cas_ip+"/rapi/system/version_info"
        values = {}
        headers = {'X-API-TOKEN': token}
        r = requests.get(url, data=values, headers=headers, verify=False)
        if r.status_code == 200:
            response = r.text
            fdata = json.loads(response)
            maa_version = fdata['results']['mag2_version']
            protocol_buffer_revision = fdata['results']['protocol_buffer_revision']
            system_platform = fdata['results']['system_product_name']
            serial_number = fdata['results']['system_serial_number']
            pattern_version= fdata['results']['patterns_version']
            print "Pattern version on "+str(cas_ip)+ " is "+ str(pattern_version)
            print "MA version on "+str(cas_ip)+ " is "+ str(maa_version)
            print "Protocol buffer revision on "+str(cas_ip)+ " is "+ str(protocol_buffer_revision)
            print "System Platform on "+str(cas_ip)+ " is "+ str(system_platform)
            print "Serial number of the appliance "+str(cas_ip)+ " is "+ str(serial_number)
        else:
            print r.status_code
            print "Unable to get System Info"
        
    def create_task(self,sample_id, profileid, plugin, token):
        a = casutilities()
        if plugin == "":
            #,'tp_IVM.SMART_DETONATION':1
            values = {'sample_id': sample_id, 'env': 'ivm', 'primary_resource_name':'', 'tp_IVM.FIREWALL':3, 'tp_DEF.log_task':1,'vmp_id':profileid,'tp_DEF.ivm_plugin':'_SYSTEM_:', 'tp_IVM.GET_DROPPED_FILES':1}
        else:
            values = {'sample_id': sample_id, 'env': 'ivm', 'primary_resource_name':'_SYSTEM_:'+str(plugin), 'tp_DEF.log_task':1,'tp_IVM.FIREWALL':3, 'vmp_id':profileid, 'tp_IVM.GET_DROPPED_FILES':1}
        headers = {'X-API-TOKEN': token}
        taskid = a.httpcall("post", "/rapi/tasks", values, headers)['results'][0]['tasks_task_id']
        print "Task id is: " +str(taskid)
        return taskid
        
    
    def wait_for_task_complete(self,taskid, timeout_wait,token):
        print "\nWait for the task to to complete.." + str(taskid)
        a = casutilities()
        timeout = 0
        state = ""
        while (state != "CORE_COMPLETE"):
            values = {}
            headers = {'X-API-TOKEN': token }
            url = "https://"+cas_ip+"/rapi/tasks/"+str(taskid)
            r = requests.get(url, data=values, headers=headers,verify=False)
            if r.status_code in [200,201]:
                data = r.text
                fdata = json.loads(data)
                state= fdata['results'][0]['task_state_state']
                print state
                if state == "CORE_COMPLETE":
                    print "Task has completed successfully."
                elif state == "CORE_ERROR":
                    print "Task has completed successfully but goes in error state."
                    state = "CORE_COMPLETE"
                else:
                    #print "Task state for task id " + str(taskid) + " is: " + str(state)
                    time.sleep(10)
                    timeout = timeout + 10
                    if timeout > timeout_wait:
                        print "Failed to complete task in alloted time."
                        print "Task state for task id " + str(taskid) + " is: " + str(state)
                        state = "CORE_COMPLETE"
            else:
                print "Manual investigation required. Some issue in getting the task state"
                
    def get_task_riskscore(self,taskid,token):
        a = casutilities()
        values = {}
        headers = {'X-API-TOKEN': token }
        url = "https://"+cas_ip+"/rapi/tasks/"+str(taskid)
        r = requests.get(url,data=values,headers=headers, verify=False)
        data = r.text
        fdata = json.loads(data)
        risk_score= fdata['results'][0]['tasks_global_risk_score']
        #print "\nRisk Score for the task id "+ str(taskid)+ " is "+ str(risk_score)
        print risk_score
        return risk_score
    
    def get_sample_id(self,taskid,token):
        a = casutilities()
        values = {}
        headers = {'X-API-TOKEN': token }
        url = "https://"+cas_ip+"/rapi/tasks/"+str(taskid)
        r = requests.get(url,data=values,headers=headers, verify=False)
        data = r.text
        fdata = json.loads(data)
        sample_id= fdata['results'][0]['tasks_sample_id']
        #print str(sample_id) + " is the sample id for task " + str(taskid) 
        #print sample_id
        return sample_id
        
    def get_dropped_file(self, filename, taskid,token):
        a = casutilities()
        values = {'task_id':taskid}
        headers = {'X-API-TOKEN': token}
        for x in itertools.count():
            try:
                f = a.httpcall("GET", "/rapi/tasks/"+str(taskid)+"/resources", values, headers)['results'][x]['task_resources_file_name']    
            except IndexError:
                print "Task ID present but it does contain any file: " + str(filename)
                sys.exit()
            if filename in f:
                resource_id = a.httpcall("GET", "/rapi/tasks/"+str(taskid)+"/resources", values, headers)['results'][x]['task_resources_resource_id']
                break
            else:
                pass
        values = {}
        headers = {'X-API-TOKEN': token}
        rapi_call="/rapi/resources/"+str(resource_id)+"/bin"
        url = "https://" +cas_ip+ rapi_call
        dropfile = requests.get(url, data=values, headers = headers, verify=False )
        log = open (str(taskid)+"_"+str(filename), "w")
        log.write(str(dropfile.text))
        log.close()
        return dropfile.text
        os.remove(str(taskid)+"_"+str(filename))
    
    def upload_samples_dir(self,cas_ip, token):
        try:
            sampleidfile = os.path.join(os.getcwd(), "sampleid.txt")
            os.remove(sampleidfile)
        except:
            pass
        fp = os.path.join(os.getcwd(),"../samples")
        sampleid = []
        for root, directories, filenames in os.walk(fp): 
            for filename in filenames: 
                file2 = os.path.join(root,filename)
                url = "https://"+ cas_ip +  "/rapi/samples/basic"
                samples = {'file': open(file2, 'rb')}
                values = {'owner': 'admin'}
                headers = {'X-API-TOKEN': token}
                r = requests.post(url, files=samples, data=values, headers=headers, verify=False)
                sample_response=r.text
                if r.status_code in [200,201]:       
                    data = json.loads(sample_response)
                    global sample_id
                    sample_id = data['results'][0]['samples_sample_id']
                    sample_resourceid = data['results'][0]['samples_basic_resource_id']
                    a = str(sample_resourceid).strip()
                    sample_md5 = data['results'][0]['sample_resources'][a]['sample_resources_md5']
                    print sample_md5                
                    f = open ('sampleid.txt', 'a')
                    f.write ( str(sample_id) + '\n' )
                    f.close()
                    print "Sample ID is: " + str(sample_id)
                    sampleid.append(sample_id)
                else:
                    print r.status_code
                    print sample_response
                    print "Unable to upload sample"
        return sampleid
    
    def upload_sample_single(self,cas_ip, sample_name, token):
        try:
            sampleidfile = os.path.join(os.getcwd(), "sampleid.txt")
            os.remove(sampleidfile)
        except:
            pass
        fp = os.path.join(os.getcwd(),"../samples/"+sample_name)
        url = "https://"+ cas_ip +  "/rapi/samples/basic"
        samples = {'file': open(fp, 'rb')}
        values = {'owner': 'admin'}
        headers = {'X-API-TOKEN': token}
        r = requests.post(url, files=samples, data=values, headers=headers, verify=False)
        sample_response=r.text
        if r.status_code in [200,201]:       
            data = json.loads(sample_response)
            global sample_id
            sample_id = data['results'][0]['samples_sample_id']
            sample_resourceid = data['results'][0]['samples_basic_resource_id']
            a = str(sample_resourceid).strip()
            sample_md5 = data['results'][0]['sample_resources'][a]['sample_resources_md5']
            print sample_md5        
            f = open ('sampleid.txt', 'a')
            f.write ( str(sample_id) + '\n' )
            f.close()
            print "Sample ID is: " + str(sample_id)
            return sample_id
        else:
            print r.status_code
            print sample_response
            print "Unable to upload sample"
                        
    def upload_sample_create_task_get_task_state_getriskscore_getpatternhits(self, cas_ip, profile_id, token):
        ''' Upload sample present under samples directory '''
        fp = os.path.join(os.getcwd(),"../samples")
        sampleid=[]
        taskid=[]
        for root, directories, filenames in os.walk(fp):
            for filename in filenames:
                file2 = os.path.join(root,filename)
                print file2
                url = "https://"+ cas_ip +  "/rapi/samples/basic"
                samples = {'file': open(file2, 'rb')}
                values = {'owner': 'admin'}
                headers = {'X-API-TOKEN': token }
                r = requests.post(url, files=samples, data=values, headers = headers, verify=False)       
                sample_response=r.text # JSON RESPONSE FOR THE SAMPLE
                data = json.loads(sample_response)
                sample_id = data['results'][0]['samples_sample_id']
                sample_resourceid = data['results'][0]['samples_basic_resource_id']
                a = str(sample_resourceid).strip()
                sample_md5 = data['results'][0]['sample_resources'][a]['sample_resources_md5']
                sampleid.append(sample_id)
         
        '''create tasks '''       
        for sample_id in sampleid:
            url = "https://"+ cas_ip +  "/rapi/tasks"
            #values = {'sample_id': sample_id, 'env': 'ivm', 'ivm_profile': 'windows-7-64-bit', 'tp_DEF.log_task':1 }
            values = {'sample_id': sample_id, 'env': 'ivm', 'vmp_id': profile_id, 'tp_DEF.log_task':1 }
            headers = {'X-API-TOKEN': token }
            r = requests.post(url, data=values, headers = headers,  verify=False)
            task_response=r.text
            data = json.loads(task_response)
            global task_id
            task_id = data['results'][0]['tasks_task_id']
            task_id = str(task_id).strip()
            taskid.append(task_id)
            print "Sampple ID is: " + str(sample_id) + " and task ID is: " + str(task_id)
            
        '''get task state'''
        for task_id in taskid:
            task_id = str(task_id).strip()
            state = ""
            while (state != "CORE_COMPLETE"):
                values = {}
                headers = {'X-API-TOKEN': token }
                url = "https://"+cas_ip+"/rapi/tasks/"+str(task_id)
                r = requests.get(url, data=values, headers=headers,verify=False)
                if r.status_code in [200,201]:
                    data = r.text
                    fdata = json.loads(data)
                    state= fdata['results'][0]['task_state_state']
                    if state == "CORE_COMPLETE":
                        print "Task state for task id " + task_id + " is: " + str(state)
                        ''' get risk score '''
                        values = {}
                        headers = {'X-API-TOKEN': token }
                        url = "https://"+cas_ip+"/rapi/tasks/"+str(task_id)
                        r = requests.get(url,data=values,headers=headers, verify=False)
                        data = r.text
                        fdata = json.loads(data)
                        risk_score= fdata['results'][0]['tasks_global_risk_score']
                        print "\nRisk Score for the task id "+ task_id+ " is "+ str(risk_score)
                        ''' get pattern hits'''
                        values = {}
                        headers = {'X-API-TOKEN': token }
                        url = "https://"+cas_ip+"/rapi/tasks/"+str(task_id)+"/patterns"
                        r = requests.get(url, data=values, headers=headers, verify=False)
                        if r.status_code in [200,201]:
                            data = r.text
                            print "\nPattern Hits are:"
                            for value in json.loads(data)['results'][0]['hits']:
                                pattern_hit_name = json.loads(data)['results'][0]['hits'][value]['pattern_group_name']
                                pattern_risk_score = json.loads(data)['results'][0]['hits'][value]['pattern_group_risk_score']
                                print str(pattern_hit_name) + ": " + str(pattern_risk_score)
                            print "\n"
                        else:
                            print "Failed to get pattern updates."
                            print r.text
                            print r.status_code
                         
                    else:
                        print "Task state for task id " + str(task_id) + " is: " + str(state)
                        time.sleep(10)
                        pass
                else:
                    print "Task not created for some reason."
                    print r.text
                    print r.status_code

    def delete_all_samples(self,cas_ip, token):
        a = casutilities()
        values = {}
        headers = {"User-Agent":"python", 'X-API-TOKEN':token}
#         sample_id = []
        status = True
        while True:
            f = a.httpcall("GET", "/rapi/samples?limit=1000", values, headers)['results_count']
            if f == 0:
                print "No samples exist"
                status = False
                break
            
            print "Total number of samples found: " + str(f)
            g = a.httpcall("GET", "/rapi/samples?limit="+str(f),values, headers)
            sample_id = []
            for x in range(f):
                sampleid = g['results'][x]['samples_sample_id']
                sample_id.append(sampleid)
            print sample_id    
            for x in sample_id:
                delsample = a.httpcall("DELETE", "/rapi/samples/"+str(x), values, headers)
                if "Not Found" in delsample:
                    pass
                else:
                    print "Sample with sample ID:"+ str(x) + " deleted successfully"

    def deletetasks(self,task_id_start, task_id_end, timeout ):
        a = casutilities()
        token = a.generate_token()
        task_id_end = task_id_end + 1
        for task_id in range(task_id_start, task_id_end):
            values = {}
            headers = {'X-API-TOKEN': token}
            deletetask = a.httpcall("DELETE", "/rapi/tasks/"+str(task_id), values, headers)
            if "404: Not Found" in deletetask:
                print "VM task id "+str(task_id)+" does not exist."
            
            if "504" in deletetask:          
                status = True
                thinktime = 0
                while status == True:
                    status_code = [200, 202]
                    deletetask = a.httpcall("DELETE", "/rapi/tasks/"+str(task_id), values, headers)
                    if "200" or "202" not in deletetask:
                        thinktime = thinktime + 1
                        print "thinktime: " + str(thinktime)
                        time.sleep(1)
                        if thinktime >=timeout:
                            print "Unable to delete the task in specified time: " + str(timeout) + " seconds"
                            status = False
                        pass
                    
                    else:
                        print "Task id "+str(task_id)+" deleted successfully."
                        status = False
            print "task id deleted: " + str(task_id)

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
                print "504"          
                status = True
                thinktime = 0
                while status == True:
                    status_code = [200, 202]
                    deleteprofile = a.httpcall("DELETE", "/rapi/system/vm/profiles/"+str(profile_id), values, headers)
                    if "200" or "202" not in deleteprofile:
                        thinktime = thinktime + 1
                        print "thinktime: " + str(thinktime)
                        time.sleep(1)
                        if thinktime >=timeout:
                            print "Unable to delete the profile in specified time: " + str(timeout) + " seconds"
                            status = False
                        pass
                    
                    else:
                        print "VM profile id "+str(profile_id)+" deleted successfully."
                        status = False                   
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
#                         status = False
                    
                ### Now wait for the profile to build in given timeout value
#                 print "CHECKPOINT 1:"
#                 url = "https://" + str(cas_ip) + str("/rapi/system/vm/profiles/"+str(x))
#                 values = {}
#                 headers = {'X-API-TOKEN': token}
#                 status = True
#                 thinktime = 0
#                 while status == True:
#                     r = requests.get(url, data=values, headers=headers, verify=False)
#                     if r.status_code in [200, 201]:
#                         profile_state = json.loads(r.text)['results'][0]['vm_profiles_status']
#                         profile_progress = json.loads(r.text)['results'][0]['vm_profiles_progress']
#                         profile_state = str(profile_state).lower()
#                         if "failed" in profile_state or "error" in profile_state:
#                             print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
#                             assert False, profile_state
#                             
#                         elif profile_state != "ready" and profile_progress != 100:
#                             print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
#                             time.sleep(30)
#                             thinktime = thinktime + 30
#                             print "thinktime value" + str(thinktime)
#                             if thinktime > timeout:
#                                 print "Profile not re-builded in given time: "+ str(timeout) + " seconds"
#                                 assert False, profile_state
#                                  
#                         elif profile_state == "ready" and profile_progress == 100:
#                             print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
#                             print "Profile build-ed successfully." + "\n"
#                             print "End time: " + str(time.ctime()) + "\n"
#                             status = False
                                 
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
#                         status = True
#                         while status == True:
#                             url = "https://" + str(cas_ip) + str("/rapi/system/vm/profiles/"+str(x))
#                             values = {}
#                             headers = {'X-API-TOKEN': token}
#                             r = requests.get(url, data=values, headers=headers, verify=False)
#                             profile_state = json.loads(r.text)['results'][0]['vm_profiles_status']
#                             profile_progress = json.loads(r.text)['results'][0]['vm_profiles_progress']
#                             profile_state = str(profile_state).lower()
#                             if "failed" in profile_state or "error" in profile_state:
#                                 print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
#                                 assert False, profile_state
#                             elif profile_state == "ready" and profile_progress == 100:
#                                 pass
#                             elif profile_state != "ready" and profile_progress != 100:
#                                 print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
#                                 status = False
#                         ### Now wait for the profile to build in given timeout value
#                         url = "https://" + str(cas_ip) + str("/rapi/system/vm/profiles/"+str(x))
#                         values = {}
#                         headers = {'X-API-TOKEN': token}
#                         status = True
#                         thinktime = 0
#                         while status == True:
#                             r = requests.get(url, data=values, headers=headers, verify=False)
#                             if r.status_code in [200, 201]:
#                                 profile_state = json.loads(r.text)['results'][0]['vm_profiles_status']
#                                 profile_progress = json.loads(r.text)['results'][0]['vm_profiles_progress']
#                                 profile_state = str(profile_state).lower()
#                                 if profile_state != "ready" and profile_progress != 100:
#                                     print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
#                                     time.sleep(30)
#                                     thinktime = thinktime + 30
#                                     print "thinktime value" + str(thinktime)
#                                     if thinktime > timeout:
#                                         print "Profile not re-builded in given time: "+ str(timeout) + " seconds"
#                                         assert False, profile_state
#                                 elif "failed" in profile_state or "error" in profile_state:
#                                     print "Profile build process failed with error" + str(profile_state)
#                                     assert False, profile_state
#                                     #assert False, "Failed to build profile"
#                                     #break
#                                 elif profile_state == "ready" and profile_progress == 100:
#                                     print "Profile ID: " + str(x) + ", Profile state: "+ str(profile_state) + ", Profile build progress: "+ str(profile_progress)
#                                     print "Profile build-ed successfully."
#                                     print "End time: " + str(time.ctime()) + "\n"
#                                     status = False 
