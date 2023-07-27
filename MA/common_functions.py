#!/usr/bin/python

import httplib, urllib, unittest, time, sys, select, paramiko, os
import simplejson as json
from settings import *
import requests.packages.urllib3
import ssl
import socket
import itertools

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
requests.packages.urllib3.has_memoryview = False


class mautilities():
    
    def httpcall(self, call_method, rapicall, values, headers):
        a = mautilities()
        token = a.generate_token(ma_ip)
        if '?' in rapicall:
            url = "https://" +ma_ip+ rapicall+"&token="+str(token)
        else:
            url = "https://" +ma_ip+ rapicall+"?token="+str(token)
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
            print "Unable to process the request " + str(rapicall)
            print "HTTP error code is: " + str(r.status_code)
            print r.text
    
    def rapiget(self, rapi_call):
        url = "https://"+ ma_ip + "/rapi" + rapi_call + "?token=" + token
        values = {}
        r = requests.get(url, data=values, verify=False)
        if r.status_code == 200:
            print "HTTP " + str(r.status_code) + " OK"
            fdata = json.dumps(r.text)
            fdata1 = json.loads(fdata)
            return fdata1
        
        elif r.status_code != 200:
            print "HTTP " + str(r.status_code) + " Error"
            print r.text
            print "Manual investigation required. Couldn't execute RAPI"
    
    def rapipost(self, rapi_call, values, headers):
        url = "https://"+ ma_ip + "/rapi" + rapi_call + "?token=" + token
        r = requests.post(url, data=values, headers=headers, verify=False)
        if r.status_code == 200:
            print "HTTP " + str(r.status_code) + " OK"
            fdata = json.dumps(r.text)
            fdata1 = json.loads(fdata)
            return fdata1
            
        elif r.status_code != 200:
            print "HTTP " + str(r.status_code) + " Error"
            print r.text
            print "Manual investigation required. Couldn't execute RAPI"
                                
    def generate_token(self,ma_ip):
        values = {'username': ma_adminuser, 'password': ma_adminpass}
        headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
        values = urllib.urlencode(values)
        #r = mautilities.rapipost("/auth/session", values, headers)
        #f = json.loads(r)
        #token = f['results']['session_token_string']
        #print "Generated token is: " + str(token)
        try:
            conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
        except AttributeError:
            conn = httplib.HTTPSConnection(ma_ip)
        try:
            conn.request("POST", "/rapi/auth/session", values, headers)
        except socket.error:
            pass
        try:
            conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
        except AttributeError:
            conn = httplib.HTTPSConnection(ma_ip)
        conn.request("POST", "/rapi/auth/session", values, headers)
        response = conn.getresponse()
        data = response.read()
        fdata =json.loads(data)
        global token
        token = fdata['results']['session_token_string']
        #print "Generated token is: " + token
        return token
        conn.close()
                
    def exec_cmd(self,ma_ip,ma_sshuser,ma_sshpass,command):
        i = 1
    
        #
        # Try to connect to the host.
        # Retry a few times if it fails.
        #
        while True:
            #print "Trying to connect to %s (%i/30)" % (ma_ip, i)
        
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ma_ip, username=ma_sshuser,password=ma_sshpass)
                print "Connected to %s" % ma_ip
                break
            except paramiko.AuthenticationException:
                print "Authentication failed when connecting to %s" % ma_ip
                sys.exit(1)
            except:
                print "Could not SSH to %s, waiting for it to start" % ma_ip
                i += 1
                time.sleep(2)
        
            # If we could not connect within time limit
            if i == 30:
                print "Could not connect to %s. Giving up" % ma_ip
                sys.exit(1)
        
        # Send the command (non-blocking)
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Wait for the command to terminate
        while not stdout.channel.exit_status_ready():
            # Only print data if there is data to read in the channel
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    # Print data from stdout
                    print stdout.channel.recv(1024),
        #
        # Disconnect from the host
        #
        #print "Command done, closing SSH connection"
        ssh.close()
      
    def create_user(self, role):
        time.sleep(2)
        uniquekey = str(int(time.time()))
        user =  "rbhalla"+uniquekey
        values = {'username': user, 'ui_password': 'norman', 'ui_roles': role, 'token' : token}
        headers = {'User-Agent':  'python','Content-type': "application/x-www-form-urlencoded"}
        values = urllib.urlencode(values)
        try:
            conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
        except AttributeError:
            conn = httplib.HTTPSConnection(ma_ip)
        conn.request("POST","/rapi/system/users", values, headers)
        response = conn.getresponse()
        data = response.read()
        if response.status == 200:
            fdata = json.loads(data)
            global uid
            global username
            uid = fdata['results'][0]['users_uid']
            uid = str(uid).strip()
            username = fdata['results'][0]['users_username']
            username = str(username).strip()
            print "User created: " + str(username)
        elif response.status not in [200]:
            print "User with role " + role + " not created. Manual Investigation required."
    
        conn.close()
            
    def systeminfo(self,ma_ip):
        #values = {'token' : token}
        #headers = {'User-Agent': 'python', 'Content-type': "application/x-www-form-urlencoded"}
        #values = urllib.urlencode(values)
        conn = httplib.HTTPSConnection(ma_ip)
        conn.request("GET", "/rapi/system/version_info?token="+token)
        response =conn.getresponse()
        data = response.read()
        fdata = json.loads(data)
        maa_version = fdata['results']['mag2_version']
        protocol_buffer_revision = fdata['results']['protocol_buffer_revision']
        system_platform = fdata['results']['system_product_name']
        serial_number = fdata['results']['system_serial_number']
        pattern_version= fdata['results']['patterns_version']
        print "Pattern version on "+str(ma_ip)+ " is "+ str(pattern_version)
        print "MA version on "+str(ma_ip)+ " is "+ str(maa_version)
        print "Protocol buffer revision on "+str(ma_ip)+ " is "+ str(protocol_buffer_revision)
        print "System Platform on "+str(ma_ip)+ " is "+ str(system_platform)
        print "Serial number of the appliance "+str(ma_ip)+ " is "+ str(serial_number)
        
        conn.close()
    
    def get_vmp_id(self, ma_ip):
        try:
            conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
        except AttributeError:
            conn = httplib.HTTPSConnection(ma_ip)
        conn.request("GET", "/rapi/system/vm/profiles?token="+token)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            fdata = json.loads(data)
            num_profiles = fdata['results_count']
            global vmp_id_list
            vmp_id_list = []
            for x in range(num_profiles):
                vmp_id = fdata['results'][x]['vm_profiles_vmp_id']
                vmp_id_list.append(vmp_id)
            return vmp_id_list
        
    def gettaskevents(self,taskid,type,token):
        conn = httplib.HTTPSConnection(ma_ip,context=ssl._create_unverified_context() )

        try:
            conn.request("GET", "/rapi/tasks/"+str(taskid)+"/events?token="+token)['results'][type]
            response=conn.getresponse()
            data = response.read()
            fdata= json.loads(data)
        #task_events = json.dumps(task_events)
            item_dict = fdata
            print len(item_dict)
            return fdata
        except TypeError:
            print "Task Error"
        conn.close()
        
    def gettaskriskscore(self,taskid_start, taskid_end):
        conn = httplib.HTTPSConnection(ma_ip,context=ssl._create_unverified_context() )
        taskid_end = (taskid_end + 1)
        for i in range(taskid_start, taskid_end):
            conn.request("GET", "/rapi/tasks/"+str(i)+"?token="+token)
            response =conn.getresponse()
            data = response.read()
            fdata = json.loads(data)
            risk_score= fdata['results'][0]['tasks_global_risk_score']
            #print "Risk Score for the task id "+ str(i)+ " is "+ str(risk_score)
            print risk_score
        conn.close()
    
    
    def getpatternhits(self,taskid):
        conn = httplib.HTTPSConnection(ma_ip)
        conn.request("GET", "/rapi/tasks/"+taskid+"/patterns?token="+token)
        response =conn.getresponse()
        data = response.read()
        print "Pattern Hits are:"
        for value in json.loads(data)['results'][0]['hits']:
            pattern_hit_name = json.loads(data)['results'][0]['hits'][value]['pattern_group_name']
            print pattern_hit_name
        conn.close()
    
        
    #if __name__ == '__main__':
    #    unittest.main()
              
    '''#def createnewsample(self):
        #exec_cmd(self,ma_ip, ma_sshuser, ma_sshpass, 'curl -X POST --form upload=@foo.txt --form \"owner=admin\" --form \"extension=jpg\" localhost/rapi/samples/basic')'''
    
    def get_build_version(self):
        version = ''
        app_url = "https://" + str(ma_ip)
        values = {'username' : ma_adminuser,'password' : ma_adminpass}
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
        print version   
        #return version
        
    def vtdown(self):
        params = {'apikey': '8b8165456d6e506f02d564b4e8fae77df589204856bf98b77a666e10c2404178', 'hash': '44cda81782dc2a346abd7b2285530c5f'}
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/download', params=params)
        downloaded_file = response.content
        
    def create_task(self,sample_id, vmp_id):
        url = "https://"+ ma_ip +  "/rapi/tasks?token="+str(token)
        headers = {'X-API-TOKEN':'9959dd1c03fa43d2b261742d6d831644'}
        values = {'sample_id': sample_id, 'env': 'ivm', 'vmp_id': vmp_id}
        r = requests.post(url, data=values, headers=headers, verify=False)
        if r.status_code in [200,201]:
            task_id = json.loads(r.text)['results'][0]['tasks_task_id']
            print "Task for sample id " +str(sample_id) + " created successfully with task id: " + str(task_id)
        else:
            print "Task not created."
            print r.text
        
        
    def upload_samples(self,ma_ip):
        try:
            sampleidfile = os.path.join(os.getcwd(), "sampleid.txt")
            os.remove(sampleidfile)
        except:
            print "File does not exist."
        fp = os.path.join(os.getcwd(),"samples")
        file1 =  os.listdir(fp)
        sample_id1 = []
        for root, directories, filenames in os.walk(fp): 
            for filename in filenames: 
                file2 = os.path.join(root,filename)
        #for entry in file1:
            #file2 = fp+"/"+entry
            #print file2
                url = "https://"+ ma_ip +  "/rapi/samples/basic"
                samples = {'file': open(file2, 'rb')}
                values = {'owner': 'admin','token' : token}
                #values = {'owner': 'admin','extension' : 'exe','token' : token}
                r = requests.post(url, files=samples, data=values, verify=False)       
                sample_response=r.text # JSON RESPONSE FOR THE SAMPLE
                data = json.loads(sample_response)
                #print data
                global sample_id
                sample_id = data['results'][0]['samples_sample_id']
                sample_id1.append(sample_id)
                sample_resourceid = data['results'][0]['samples_basic_resource_id']
                a = str(sample_resourceid).strip()
                sample_md5 = data['results'][0]['sample_resources'][a]['sample_resources_md5']
                print sample_md5                
                #f = open ('sampleid.txt', 'a')
                #f.write ( str(sample_id) + '\n' )
                #f.close()
                #print "Sample ID is: " + str(sample_id)
        
        return sample_id1
    
    def get_taskstate(self,task_id):
        state = ""
        while (state != "CORE_COMPLETE"):
            conn = httplib.HTTPSConnection(ma_ip,context=ssl._create_unverified_context())
            conn.request("GET", "/rapi/tasks/"+str(task_id)+"?token="+token)
            response =conn.getresponse()
            data = response.read()
            fdata = json.loads(data)
            state= fdata['results'][0]['task_state_state']
            if state == "CORE_COMPLETE":
                print "Task state for task id " + str(task_id) + " is: " + str(state)
            elif state == "CORE_ERROR":
                print "Task state for task id " + str(task_id) + " is: " + str(state)
                state = "CORE_COMPLETE"
            else:
                print "Task state for task id " + str(task_id) + " is: " + str(state)
                pass
            conn.close()
    
    def installpattern(self,md5):
        values = {'token': token}
        headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
        values = urllib.urlencode(values)
        conn = httplib.HTTPSConnection(ma_ip)
        conn.request("POST", "/rapi/system/updates/check", values, headers)
        response = conn.getresponse()
        data = response.read()
        print data
        fdata =json.loads(data)
        current_version = fdata['results'][1]['components_version']
        print "Current pattern version installed is: " + str(current_version)
        update_version = fdata['results'][1]['updates_version_str_to']
        print "Pattern version available is: " + str(update_version)
        if str(current_version).strip() == str(update_version).strip():
            print "Pattern version (current and update) are same. No need to update patterns."
        else:
            print "Pattern update is available"
            ### Get the md5 of the pattern version available ###
            md5 = fdata['results'][1]['updates_md5']
            print md5.strip()
    
    def get_install_patternversion(self,ma_ip):
        values = {'token': token}
        headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
        values = urllib.urlencode(values)
        try:
            conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
        except AttributeError:
            conn = httplib.HTTPSConnection(ma_ip)
        conn.request("POST", "/rapi/system/updates/check", values, headers)
        response = conn.getresponse()
        data = response.read()
        print data
        fdata =json.loads(data)
        resultcount = fdata['results_count']
        if resultcount == 0:
            print "No updates available"
            pass
        elif resultcount >= 1: 
            for i in range(0,resultcount):
                componentname = fdata['results'][i]['components_name']
                names = [componentname]
                if "patterns" in names:
                    print "Pattern update available"
                    current_version = fdata['results'][i]['components_version']
                    print "Current pattern version installed is: " + str(current_version)
                    update_version = fdata['results'][i]['updates_version_str_to']
                    print "Pattern version available is: " + str(update_version)
                    if str(current_version).strip() == str(update_version).strip():
                        print "Pattern version (current and update) are same. No need to update patterns."
                    else:
                        md5 = fdata['results'][i]['updates_md5']
                        print md5.strip()
                        conn.close()
                        print "Download new pattern version: " + str(update_version)
                        values = {'md5': md5, 'install': '1', 'token': token }
                        headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
                        values = urllib.urlencode(values)
                        try:
                            conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
                        except AttributeError:
                            conn = httplib.HTTPSConnection(ma_ip)
                        conn.request("POST", "/rapi/system/updates/download", values, headers)
                        response = conn.getresponse()
                        data = response.read()
                        print data
                        print "Wait for the pattern to get installed."
                        for i in range(0,1000):
                            time.sleep(10)
                            try:
                                conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
                            except AttributeError:
                                conn = httplib.HTTPSConnection(ma_ip)
                            conn.request("GET", "/rapi/system/version_info?token="+token)
                            response =conn.getresponse()
                            data = response.read()
                            print data
                            fdata = json.loads(data)
                            pattern_version= fdata['results']['patterns_version']
                            if str(pattern_version).strip() == str(update_version).strip():
                                print "Pattern update "+ str(pattern_version) + " installed successfully."
                                break
                            else: 
                                pass
                            
                        conn.close()                    
                else:
                    if i == resultcount - 1:
                        print "Pattern update not available"
                    if (i < resultcount):
                        pass
                    
        conn.close()
        
    def downloadpdfs(self):
        os.mkdir(os.path.join(os.getcwd(),"task_reports_"+execution_id))
        
    def upload_sample_create_task_get_task_state_getriskscore_getpatternhits(self, ma_ip):
        ''' Upload sample present under samples directory '''
        try:
            if os.path.exists("taskid.txt"):
                os.remove("taskid.txt")
        except:
            pass
        try:
            sampleidfile = os.path.join(os.getcwd(), "sampleid.txt")
            os.remove(sampleidfile)
        except:
            pass
            
        fp = os.path.join(os.getcwd(),"samples")
        file1 =  os.listdir(fp)
        for root, directories, filenames in os.walk(fp): 
            for filename in filenames: 
                file2 = os.path.join(root,filename)
                #file2 = fp+"/"+entry
                #print "\n" + file2
                url = "https://"+ ma_ip +  "/rapi/samples/basic"
                samples = {'file': open(file2, 'rb')}
                values = {'owner': 'admin','token' : token}
                r = requests.post(url, files=samples, data=values, verify=False)       
                sample_response=r.text # JSON RESPONSE FOR THE SAMPLE
                data = json.loads(sample_response)
                #print data
                global sample_id
                sample_id = data['results'][0]['samples_sample_id']
                sample_resourceid = data['results'][0]['samples_basic_resource_id']
                a = str(sample_resourceid).strip()
                sample_md5 = data['results'][0]['sample_resources'][a]['sample_resources_md5']
                print sample_md5
                #for a in sample_md5:
                #        print a
                #        print data['results'][0]['sample_resources'][a]['sample_resources_md5']   
                        #print "test"
                #print sample_md5
                
                f = open ('sampleid.txt', 'a')
                f.write ( str(sample_id) + '\n' )
                f.close()
                print "Sample ID is: " + str(sample_id)
                ''' create tasks'''
                ### First get the number of profiles and thier profile ID's
                mautilities.get_vmp_id(self, ma_ip)
                for x in vmp_id_list:
                    url = "https://"+ ma_ip +  "/rapi/tasks"
                    if plugin == None:
                        values = {'sample_id': sample_id,\
                              'env': env_type,\
                              'vmp_id': x,\
                               'tp_IVM.TIMEOUT': timeout,\
                                'tp_IVM.GET_DROPPED_FILES': dropped_files,\
                                 'tp_IVM.enable_ddna': ddna,\
                                 'tp_IVM.FIREWALL': firewall,\
                                 'tp_DEF.log_task': task_log,\
                                  'token' : token}
                    else:
                        values = {'sample_id': sample_id,\
                              'env': env_type,\
                              'vmp_id': x,\
                               'tp_IVM.TIMEOUT': timeout,\
                                'tp_IVM.GET_DROPPED_FILES': dropped_files,\
                                 'tp_IVM.enable_ddna': ddna,\
                                 'tp_IVM.FIREWALL': firewall,\
                                 'tp_DEF.log_task': task_log,\
                                 'tp_DEF.ivm_plugin':plugin,\
                                  'token' : token}
                        
                    r = requests.post(url, data=values, verify=False)
                    task_response=r.text
                    data = json.loads(task_response)
                    global task_id
                    task_id = data['results'][0]['tasks_task_id']
                    task_id = str(task_id).strip()
                    f = open ('taskid.txt', 'a')
                    f.write (task_id + "\n")
                    f.close()
                    print "Task ID is: " + str(task_id)
            
        '''get task state'''
        f = open ('taskid.txt', 'r')
        for task_id in f:
            task_id = str(task_id).strip()
            state = ""
            while (state != "CORE_COMPLETE"):
                try:
                    conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
                except AttributeError:
                    conn = httplib.HTTPSConnection(ma_ip)
                #try:
                conn.request("GET", "/rapi/tasks/"+task_id+"?token="+token)    
                #except socket.error:
                #    print "socket error1"    
                response = conn.getresponse()
                data = response.read()
                fdata = json.loads(data)
                state= fdata['results'][0]['task_state_state']
                if state == "CORE_COMPLETE":
                    print "Task state for task id " + task_id + " is: " + str(state)
                    ''' get risk score '''
                    #try:
                    conn.request("GET", "/rapi/tasks/"+task_id+"?token="+token)
                    #except socket.error:
                    #    print "socket error2"
                    response =conn.getresponse()
                    data = response.read()
                    fdata = json.loads(data)
                    risk_score= fdata['results'][0]['tasks_global_risk_score']
                    print "\nRisk Score for the task id "+ task_id+ " is "+ str(risk_score)
                    ''' get pattern hits'''
                    #try:
                    conn.request("GET", "/rapi/tasks/"+task_id+"/patterns?token="+token)
                    #except socket.error:
                    #    print "socket error3"
                    response =conn.getresponse()
                    data = response.read()
                    print "\nPattern Hits are:"
                    for value in json.loads(data)['results'][0]['hits']:
                        pattern_hit_name = json.loads(data)['results'][0]['hits'][value]['pattern_group_name']
                        print pattern_hit_name + "|"
                    conn.close()
                     
                else:
                    print "Task state for task id " + str(task_id) + " is: " + str(state)
                    time.sleep(10)
                    pass
                conn.close()
        
    def check_dir_permissions(self):
        url_list = ["https://"+ma_ip+"/css/",\
                     "https://"+ma_ip+"/images/",\
                      "https://"+ma_ip+"/icons/",\
                       "https://"+ma_ip+"/images/brand/",\
                        "https://"+ma_ip+"/js/",\
                         "https://"+ma_ip+"/js/app/",\
                          "https://"+ma_ip+"/js/jquery_jstree/_lib/",\
                           "https://"+ma_ip+"/js/jquery_jstree/themes/",\
                            "https://"+ma_ip+"/js/jquery_jstree/themes/default/",\
                             "https://"+ma_ip+"/js/lib/",\
                              "https://"+ma_ip+"/partials/",\
                               "https://"+ma_ip+"/partials/directives/",\
                                "https://"+ma_ip+"/partials/profiles/"]
        values = {'token': token}
        headers = {}
        values = urllib.urlencode(values)
        conn = httplib.HTTPSConnection(ma_ip)
        for i in url_list: 
            conn.request("GET", i, values, headers)
            response = conn.getresponse()
            data = response.read()
            #print data
            try:
                outputfile = os.path.join(os.getcwd(), "output.txt")
                os.remove(outputfile)
            except:
                pass
            f = open("output.txt", "a")
            f.write(data.lower() + "\n")
            f.close()
            
            try:
                f = open("output.txt")
                if "you don't have permission to access" in f.read():
                    print "[Passed] - User don't have permission to access: "+ str(i)
                else:
                    print "fail"
            except:
                f.close()
            finally:
                f.close()
             
    def get_task_events(self, task_id):
        url = "https://"+ma_ip+"/rapi/tasks/"+str(task_id).strip()+"/events?token="+token
        conn =  httplib.HTTPSConnection(ma_ip)
        conn.request("GET", url)
        response = conn.getresponse()
        data = response.read()
        #print data
        fdata = json.loads(data)
        test = fdata['results']['CORE']
        for a in test:       
            newte = fdata['results']['CORE'][a]
            temp = json.loads(json.dumps(newte))
            print temp
            for b in temp[0][0]:
                print b
                
            #ip = temp['IP_Connect']
            #print ip
        
        conn.close()
                
    def ma3074(self, ma_ip):
        print "Test for creating a user, and then create API keys with different roles and automatically test \
                their privileges"
        
        uniquekey = str(int(time.time()))
        user = "rbhalla"+str(uniquekey)
        values = {'username': user, 'ui_password': 'bluecoat', 'ui_roles': 'administrator', 'token' : token}
        headers = {'User-Agent':  'python','Content-type': "application/x-www-form-urlencoded", 'SESSTOK':token}
        values = urllib.urlencode(values)
        try:
            conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
        except AttributeError:
            conn = httplib.HTTPSConnection(ma_ip)
        conn.request("POST","/rapi/system/users", values, headers)
        response = conn.getresponse()
        data = response.read()
        print data
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
             
        ''' Now create api keys with different roles '''
         
        roles_types = ["guest", "observer", "analyst", "super-analyst", "sysconfig", "administrator"]
         
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
            if roles == "guest":
                api_key_guest = str(roles_api_key).strip()
                print "API key with guest role access is: " + api_key_guest
            elif roles == "observer":
                api_key_observer = str(roles_api_key).strip()
                print "API key with observer role access is: " + api_key_observer
            if roles == "analyst":
                api_key_analyst = str(roles_api_key).strip()
                print "API key with analyst role access is: " + api_key_analyst
            if roles == "super-analyst":
                api_key_sanalyst = str(roles_api_key).strip()
                print "API key with super-analyst role access is: " + api_key_sanalyst
            if roles == "sysconfig":
                api_key_sysconfig = str(roles_api_key).strip()
                print "API key with sysconfig role access is: " + api_key_sysconfig
            if roles == "administrator":
                api_key_administrator = str(roles_api_key).strip()
                print "API key with administrator role access is: " + api_key_administrator

    def delete_users(self, uid_start, uid_end):
        uid_end = uid_end + 1
        try:
            conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
        except AttributeError:
            conn = httplib.HTTPSConnection(ma_ip)
        
        #token="bbe6ad1421ee4e068090bd50c52489d3"
        for userid in range(uid_start, uid_end):
            conn.request("DELETE", "/rapi/system/users/"+str(userid)+"?token="+token)
            response =conn.getresponse()
            data = response.read()
            print data
            #time.sleep(1)
        conn.close()
    
    def delete_tasks(self, taskid_start, taskid_end):
        taskid_end = taskid_end + 1
        conn = httplib.HTTPSConnection(ma_ip)
        for taskid in range(taskid_start, taskid_end):
            conn.request("DELETE", "/rapi/tasks/"+str(taskid)+"?token="+token)
            response =conn.getresponse()
            data = response.read()
            print data
        conn.close()   
    
    def deletesample(self,sample_id_start, sample_id_end ):
        sample_id_end = sample_id_end + 1
        conn = httplib.HTTPSConnection(ma_ip)
        for sample_id in range(sample_id_start, sample_id_end):
            try:
                conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
            except AttributeError:
                conn = httplib.HTTPSConnection(ma_ip)
            conn.request("DELETE", "/rapi/samples/"+str(sample_id)+"?token="+token)
            response =conn.getresponse()
            data = response.read()
            print data
            conn.close()
    
    def deletepatterns(self,pattern_id_start, pattern_id_end ):
        pattern_id_end = pattern_id_end + 1
        conn = httplib.HTTPSConnection(ma_ip)
        for pattern_id in range(pattern_id_start, pattern_id_end):
            try:
                conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
            except AttributeError:
                conn = httplib.HTTPSConnection(ma_ip)
            conn.request("DELETE", "/rapi/pattern_groups/"+str(pattern_id)+"?token="+token)
            response =conn.getresponse()
            data = response.read()
            print data
            conn.close()
    
    def create_pattern(self):
        uniquekey = str(int(time.time()))
        name = "test"+str(uniquekey)
        values = {"description": "No description",\
                  "is_enabled": "1",\
                   "is_global": "0",\
                    "owner": "admin",\
                     "name":name,\
                      "risk_score": "1",\
                       "type": "simple",\
                        "mode": "any_of"}
        headers = {'User-Agent': 'python',\
                   'Content-type': "application/json"}
        values = json.dumps(values)
        conn = httplib.HTTPSConnection(ma_ip)
        conn.request("POST", "/rapi/pattern_groups?token=e706ab59c4ad4cd1820813fbd608f545", values, headers)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            fdata = json.loads(data)
            pattern_id = fdata['results']
            pattern_id = str(pattern_id).replace('[', '').replace(']','').strip()
            print "Pattern created with pattern group id: " + str(pattern_id)
        
        elif response.status == 403:
            data = response.read()
            print data
            print "Pattern not created."
   
    def deletevmprofile(self,profile_id_start, profile_id_end, timeout ):
        profile_id_end = profile_id_end + 1
        try:
            conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
        except AttributeError:
            conn = httplib.HTTPSConnection(ma_ip)
        for profile_id in range(profile_id_start, profile_id_end):
            conn.request("DELETE", "/rapi/system/vm/profiles/"+str(profile_id)+"?token="+token)
            response =conn.getresponse()
            #print response.read()
            if "404: Not Found" in response.read():
                print "VM profile id "+str(profile_id)+" does not exist."
            
            elif response.status == 200:
                print "VM profile id "+str(profile_id)+" deleted successfully."
            
            elif response.status == 202:
                print "VM profile id "+str(profile_id)+" deleted successfully."
            
            
            if response.status == 504:
                status = True
                thinktime = 0
                while status == True:
                    #time.sleep(5)
                    status_code = [200, 202]
                    try:
                        conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
                    except AttributeError:
                        conn = httplib.HTTPSConnection(ma_ip)
                    
                    conn.request("DELETE", "/rapi/system/vm/profiles/"+str(profile_id)+"?token="+token)
                    response = conn.getresponse()
                    #print response.read()
                    #print response.status
                    if response.status == 200:
                        #print response.read()
                        print "VM profile id "+str(profile_id)+" deleted successfully."
                        conn.close()
                        status = False
                        
                    elif response.status == 202:
                        print "VM profile id "+str(profile_id)+" deleted successfully."
                        conn.close()
                        status = False
                    
                    elif response.status not in status_code:
                        thinktime = thinktime + 1
                        print "thinktime: " + str(thinktime)
                        time.sleep(1)
                        if thinktime >=timeout:
                            print "Unable to delete the profile in specified time: " + str(timeout) + " seconds"
                            status = False
                        pass
                        
        conn.close()
    
    
    def createvmprofile(self, baseid, howmanyprofiles):
        profileid = []
        for x in range(howmanyprofiles):
            uniquekey = str(int(time.time()))
            newprofilename = "test"+str(uniquekey)
            shortname = "short"+str(uniquekey) 
            try:
                conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
            except AttributeError:
                conn = httplib.HTTPSConnection(ma_ip)
            values = {'vmb_id':baseid, 'name':newprofilename,'short_name':shortname, 'token': token}
            values = urllib.urlencode(values)
            headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
            print "hello"
            try:
                conn.request("POST", "/rapi/system/vm/profiles", values, headers)
            except socket.error:
                pass 
            response = conn.getresponse()
            
            if response.status == 400:
                print response.read()
                print "[Failed] Unable to create a vm profile needed to perform delete function. Need Manual investigation."
                print self.fail("Failed")
                
            if response.status == 403:
                print "[Failed] Unable to create a vm profile needed to perform delete function. Need Manual investigation."
            
            elif response.status == 200:
                data = response.read()
                fdata = json.loads(data)
                profile_id = fdata['results'][0]['vm_profiles_vmp_id']
                print "profile id is: " + str(profile_id)
                profileid.append(profile_id)
                time.sleep(2)
                conn.close()
            
            elif response.status == 504:
                status = True
                while status == True:
                    time.sleep(5)
                    try:
                        conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
                    except AttributeError:
                        conn = httplib.HTTPSConnection(ma_ip)
                    try:
                        conn.request("POST", "/rapi/system/vm/profiles", values, headers)
                    except socket.error:
                        pass
                    response = conn.getresponse()
                    
                    if response.status == 200:
                        data = response.read()
                        fdata = json.loads(data)
                        profile_id = fdata['results'][0]['vm_profiles_vmp_id']
                        print "profile id is: " + str(profile_id)
                        profileid.append(profile_id)
                        conn.close()
                        status = False
                        
                    if response.status == 500:
                        print response.read()
                    
                    conn.close()
                    
    def enable_yara(self):
        values = {'value': 'False'}
        headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
        values = json.dumps(values)
        conn = httplib.HTTPSConnection(ma_ip + ":443")
        conn.request("POST", "/rapi/system/config/main.yara_enabled?token=cb256fc919674ee6ad75883a6e19ee5f", values, headers)
        response = conn.getresponse()
        data = response.read()
        print data
        fdata =json.loads(data)
        #global token
        #token = fdata['results']['session_token_string']
        #print "Generated token is: " + token
        conn.close()
        
    def encode_lic(self):
        from sys import argv
        filename = os.path.join(os.getcwd(), "ct4vt-aiid3-2ditm-s2r8h-bd6gt.ndf_old")
        txt = open(filename)
        a = txt.read()
        print a.encode('zlib').encode('base64')
        
    def create_url_task(self, profileid):
        test_urls = ["http://www.google.co.in",\
                      "https://www.google.com.my",\
                       "https://www.facebook.com",\
                        "https://www.gmail.com",\
                        "https://www.wwe.com",\
                        "https://www.virustotal.com"]
        for urls in test_urls:
            rapi_url = "https://"+ ma_ip +  "/rapi/samples/url"
            values = {'url': urls, 'owner': 'admin', 'token' : token}
            r = requests.post(rapi_url, data=values, verify=False)
            if r.status_code == 200:
                data = json.loads(r.text)
                sample_id = data['results'][0]['samples_sample_id']
                print "Sample id for url "+ str(urls) + " is: " + str(sample_id)
                url = "https://"+ ma_ip +  "/rapi/tasks"
                values = {'sample_id': sample_id, 'env': 'ivm', 'vmp_id': profileid, 'token' : token}
                r = requests.post(url, data=values, verify=False)
                if r.status_code == 200:
                    data = json.loads(r.text)
                    task_id = data['results'][0]['tasks_task_id']
                    print "Task id for url " + str(urls) + " is: " + str(task_id) + "\n"
                elif r.status_code != 200:
                    print "Sample id for url "+ str(urls) + " is: " + str(sample_id)
                    print "Task not created for url " + str(urls) + ", Manual invetigation required."
            
            elif r.status_code != 200:
                print "Sample not created for url " + str(urls) + ", Manual investigation required."

        
    def buildvmprofile(self, profile_id_start, profile_id_end):
        profile_id_end = profile_id_end + 1
        for x in range(profile_id_start, profile_id_end):
            try:
                conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
            except AttributeError:
                conn = httplib.HTTPSConnection(ma_ip)
            values = {'token': token}
            #values = {}
            values = urllib.urlencode(values)
            headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded", 'X-API-TOKEN': "2823f0ab9b0c474eb8b272d72bfcbd11"}
            print "hello" + str(x)
            try:
                conn.request("POST", "/rapi/system/vm/profiles/"+str(x)+"/build", values, headers)
            except socket.error:
                pass 
            response = conn.getresponse() 
            if response.status in [200, 203]:
                data = response.read()
                print data
                fdata = json.loads(data)
                time.sleep(30)
                try:
                    values = {}
                    conn.request("GET", "/rapi/system/vm/profiles/"+str(x)+"?token="+token, values, headers)
                except socket.error:
                    print "socket error1"
                    pass
                response = conn.getresponse()
                data = response.read()
                fdata = json.loads(data)
                profile_state = fdata['results'][0]['vm_profiles_status']
            
                if profile_state == "Ready":
                    print profile_state
                    break
                elif profile_state != "Ready":
                    for i in itertools.count():
                        try:
                            time.sleep(30)
                            values = {}
                            #values = urllib.urlencode(values)
                            conn.request("GET", "/rapi/system/vm/profiles/"+str(x)+"?token="+token, values, headers)
                            response = conn.getresponse()
                            data = response.read()
                            fdata = json.loads(data)
                            profile_state = fdata['results'][0]['vm_profiles_status']
                            profile_progress = fdata['results'][0]['vm_profiles_progress']
                            if profile_state == "Ready":
                                break
                            else:
                                print profile_state + str(profile_progress)
                                pass
                        except socket.error:
                            print "Socket error"
                            pass
                
        conn.close()
                                
    
    
    def customize_buildvmprofile(self, profile_id_start, profile_id_end):                                 
        profile_id_end = profile_id_end + 1
        #starttime = 0
        for x in range(profile_id_start, profile_id_end):
            #starttime = starttime + 1
            #if starttime >= thinktime:
            #    print "Timeout."
            #    break
            def waitnbuild():
                for i in itertools.count():
                    try:
                        time.sleep(30)
                        values = {}
                        headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
                        conn.request("GET", "/rapi/system/vm/profiles/"+str(x)+"?token="+token, values, headers)
                        response = conn.getresponse()
                        data = response.read()
                        fdata = json.loads(data)
                        profile_progress = fdata['results'][0]['vm_profiles_progress']
                        profile_state = fdata['results'][0]['vm_profiles_status']
                        if profile_progress == 100:
                            print "\nCustomization process completed."
                            ### Build profile ###
                            print "Building Profile with ID: " + str(x)
                            values = {'token': token}
                            values = urllib.urlencode(values)
                            headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
                            try:
                                conn.request("POST", "/rapi/system/vm/profiles/"+str(x)+"/build", values, headers)
                            except socket.error:
                                pass 
                            response = conn.getresponse() 
                            if response.status in [200, 203]:
                                #print "Build process started with HTTP status " + str(response.status)
                                data = response.read()
                                #print data
                                fdata = json.loads(data)
                                time.sleep(30)
                                try:
                                    values = {}
                                    conn.request("GET", "/rapi/system/vm/profiles/"+str(x)+"?token="+token, values, headers)
                                except socket.error:
                                    print "socket error1"
                                    pass
                                response = conn.getresponse()
                                data = response.read()
                                fdata = json.loads(data)
                                profile_state = fdata['results'][0]['vm_profiles_status']
                             
                                if profile_state == "Ready":
                                    print profile_state + str(profile_progress)
                                    break
                                elif profile_state != "Ready":
                                    for z in itertools.count():
                                        try:
                                            time.sleep(30)
                                            values = {}
                                            #values = urllib.urlencode(values)
                                            conn.request("GET", "/rapi/system/vm/profiles/"+str(x)+"?token="+token, values, headers)
                                            response = conn.getresponse()
                                            data = response.read()
                                            fdata = json.loads(data)
                                            profile_state = fdata['results'][0]['vm_profiles_status']
                                            profile_progress = fdata['results'][0]['vm_profiles_progress']
                                            if profile_state == "Ready":
                                                print profile_state + str(profile_progress)
                                                break
                                            else:
                                                print profile_state + str(profile_progress)
                                                pass
                                    
                                        except socket.error:
                                            print "Socket error"
                                            pass
                                        
                                        #finally:
                                        #    print "break"
                                        #    break
                            elif response.status not in [200, 203]:
                                data = response.read()
                                print "There is a error while building a profile. Manual Investigation required."
                                print "Error code is: HTTP " + str(response.status) 
                                print data
                                
                        elif profile_progress != 100:
                            print "Customization of profile progress" + str(profile_progress)
                            waitnbuild()
                        
                    except socket.error:
                        print "Socket error"
                        pass
                    break            
             
            try:
                conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
            except AttributeError:
                conn = httplib.HTTPSConnection(ma_ip)
            values = {'token': token}
            values = urllib.urlencode(values)
            headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
            try:
                print "Customizing profile with ID: "  + str(x)
                conn.request("POST", "/rapi/system/vm/profiles/"+str(x)+"/customize", values, headers)  
            except socket.error:
                pass 
            response = conn.getresponse() 
            if response.status in [200, 203]:
                data = response.read()
                fdata = json.loads(data)
                time.sleep(30)
                try:
                    values = {}
                    conn.request("GET", "/rapi/system/vm/profiles/"+str(x)+"?token="+token, values, headers)
                except socket.error:
                    print "socket error1"
                    pass
                response = conn.getresponse()
                if response.status in [200, 203]:
                    data = response.read()
                    fdata = json.loads(data)
                    profile_progress = fdata['results'][0]['vm_profiles_progress']
             
                    if profile_progress == 100:
                        waitnbuild()
                        
                    elif profile_progress != 100:
                        waitnbuild()    
                        
            if response.status not in [200, 203]:
                data = response.read()
                print "There is a problem while customizing a profile. Manual Investigation required."
                print "Error code is HTTP: " + str(response.status)
                print data
        conn.close()
        
        
    def sshpara(self,host, cmd, user, password1 ):
        i = 1
        
        while True:
            print "Trying to connect to %s (%i/30)" % (host, i)
        
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, username=user,password=password1)
                print "Connected to %s" % host
                break
            except paramiko.AuthenticationException:
                print "Authentication failed when connecting to %s" % host
                sys.exit(1)
            except:
                print "Could not SSH to %s, waiting for it to start" % host
                i += 1
                time.sleep(2)
        
            # If we could not connect within time limit
            if i == 30:
                print "Could not connect to %s. Giving up" % host
                sys.exit(1)
        
        # Send the command (non-blocking)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Wait for the command to terminate
        while not stdout.channel.exit_status_ready():
            # Only print data if there is data to read in the channel
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    # Print data from stdout
                    fp = open("ssh.txt", "w")
                    fp.write(stdout.channel.recv(1024))
                        #print stdout.channel.recv(1024),
        
        #
        # Disconnect from the host
        #
        #print "Command done, closing SSH connection"
        ssh.close()        
        
    def powerstate(self,timeout):
        i = 0
        while (i < timeout):
            cmd = "supervisorctl status | grep web-router:web-router-443 | grep -i running | wc -l"
            mautilities.sshpara(self, ma_ip, cmd, ma_sshuser, ma_sshpass)
            fp = open ("ssh.txt", "r").read()
            if "1" in fp:
                print "Machine is up and running"
                break
            else:
                i+=1
        if (i >= timeout):
            print "Machine is not up after reverting and waiting for " + str(timeout) + " seconds."    
            print "Manual investigation is requied."        

    def gettask_logs(self, taskid):
        a = mautilities()
        values = {'task_id':taskid}
        headers = {'X-API-TOKEN': token}
        f = a.rapiget("/tasks/"+str(taskid)+"/resources")
        return f
    
    def delete_all_samples(self,ma_ip):
        a = mautilities()
        values = {}
        headers = {"User-Agent":"python"}
        sample_id = []
        status = True
        while True:
            f = a.httpcall("GET", "/rapi/samples?limit=1000", values, headers)['results_count']
            if f == 0:
                print "No samples exist"
                status = False
                break
            
            print "Total number of samples found: " + str(f)
            g = a.httpcall("GET", "/rapi/samples?limit="+str(f),values, headers)
            for x in range(f):
                sampleid = g['results'][x]['samples_sample_id']
                sample_id.append(sampleid)
            print sample_id    
            for x in sample_id:
                delsample = a.httpcall("DELETE", "/rapi/samples/"+str(x), values, headers)
                print delsample
                if 404 in delsample:
                    pass
                else:
                    print "Sample with sample ID:"+ str(x) + " deleted successfully"

        
        
