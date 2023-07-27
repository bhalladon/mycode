import unittest,time,paramiko,requests,json,sys
from paramiko_expect import SSHClientInteraction
from code import interact
cas_ip="10.199.107.17:8082"
cas_ip_no_port="10.199.107.17"
cas_adminuser="admin"
cas_adminpass="admin123"
upgrade_path=["http://10.199.97.67/casma/build/casma_main_coe4/casma_main_coe4-244538.debug.bcsi",\
              "http://10.199.97.67/casma/build/casma_main_coe4/casma_main_coe4-244475.debug.bcsi"]

class upgradetest():
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
        a = upgradetest()
        values = {"username":cas_adminuser, "password":cas_adminpass}
        headers = {"User-Agent":"python"}
        token = a.httpcall("POST", "/rapi/auth/session", values, headers)['results']['session_token_string']
        return token
    
    def sshcmd_port22(self,cas_ip_no_port):
        file1 = open("testlog.txt","w")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(cas_ip_no_port, 22, username="admin", password="admin123")
        interact = SSHClientInteraction(ssh,timeout=10,display=True)
        interact.expect('.*CAS>.*')
        interact.send('en')
        interact.expect('.*Password:.*')
        interact.send('admin')
        interact.expect('.*CAS#.*')
        interact.send('installed-systems view')
        interact.expect('.*Version.*')
        result = file1.write(interact.current_output)
        ssh.close()
        #file1.close()
        #print result

    def reboot(self,cas_ip_no_port):
        file1 = open("testlog.txt","w")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(cas_ip_no_port, 22, username="admin", password="admin123")
        interact = SSHClientInteraction(ssh,timeout=10,display=True)
        interact.expect('.*CAS>.*')
        interact.send('en')
        interact.expect('.*Password:.*')
        interact.send('admin')
        interact.expect('.*CAS#.*')
        interact.send('restart')
        interact.expect('.*no,yes.*')
        interact.send('yes')
        result = file1.write(interact.current_output)
        ssh.close()

    def wait_for_reboot(self,cas_ip_no_port):
        try:
            file1 = open("testlog.txt","w")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(cas_ip_no_port, 22, username="admin", password="admin123")
            interact = SSHClientInteraction(ssh,timeout=10,display=True)
            interact.expect('.*CAS>.*')
            interact.send('en')
            interact.expect('.*Password:.*')
            interact.send('admin')
            interact.expect('.*CAS#.*')
            interact.send('ping google.com')
            interact.expect('.*bytes.*')
            file1.write(interact.current_output)
            ssh.close()
            file1.close()
        except:
            pass
    
    def sshcmd_port2024(self,cas_ip_no_port,command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(cas_ip_no_port, 2024, username="clpdebug", password="12345678")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        return (ssh_stdout.read().decode('ascii')).strip()
        
    def sshcmd_cli_upgrade(self,cas_ip_no_port,image_path):
        file1 = open("testlog.txt","w")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(cas_ip_no_port, 22, username="admin", password="admin123")
        interact = SSHClientInteraction(ssh,timeout=10,display=True)
        interact.expect('.*CAS>.*')
        interact.send('en')
        interact.expect('.*Password:.*')
        interact.send('admin')
        interact.expect('.*CAS#.*')
        interact.send('installed-systems load '+str(image_path))
        #print (ssh_stdout.read().decode('ascii')).strip()            #try:
            #interact.send('ma-actions profiles imports download validate_cert 0 url http://10.199.97.68/casma/exported_base_img_profile/Rajiv/Win7_base_profile_withoffice2016/bin')
            #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command,timeout=10)
            #except socket.timeout:
            #return (ssh_stdout.read().decode('ascii')).strip()
            #return (ssh_stdout.read().decode('ascii')).strip()
            #interact.send(command)
        time.sleep(2)
            
        file1.write(interact.current_output)
        ssh.close()


class test_systeminfo(unittest.TestCase):

    def setUp(self):
        global a
        a = upgradetest()
        global token
        token = a.generate_token() 
    
          
    def test_a_getsysteminfo(self):
        count_upgrade_path_len = len(upgrade_path)
        for x in range(count_upgrade_path_len):
            if (count_upgrade_path_len - x) == 1:
                ''' Configure old appliance before upgrading to final image'''
                print "Configure appliance"
                
                print "Upload final base image"
                get_build_number = str(upgrade_path[x]).split('debug')[0].split('-')[1].replace('.','').strip()
                print "build number is: " + str(get_build_number)
                a.sshcmd_cli_upgrade(cas_ip_no_port, upgrade_path[x])
                ''' wait for image to upload successfully'''
                status = True
                timeout = 0
                while status == True:
                    a.sshcmd_port22(cas_ip_no_port)
                    file1 = open("testlog.txt","r")
                    for line in file1:
                        if get_build_number in line:
                            print "Image uploaded successfully"
                            status = False
                        else:
                            time.sleep(4)
                            timeout +=4
                            if timeout >=1800:
                                print "Failed to upload image. Manual investigation required."
                                status = False
                print "rebooting appliance"
                a.reboot(cas_ip_no_port)
                status = True
                timeout = 0
                while status ==True:
                    a.wait_for_reboot(cas_ip_no_port)
                    file1 = open("testlog.txt","r")
                    for line in file1:
                        if "bytes" in line:
                            print "Box is up and running successfully after reboot."
                            status = False
                        else:
                            time.sleep(4)
                            timeout +=4
                            if timeout >=900:
                                print "Box not reachable after reboot. Manual Investigation required."
                                status = False
                
                print "Verify Configuration After upgrade"
                        
            else:
                get_build_number = str(upgrade_path[x]).split('debug')[0].split('-')[1].replace('.','').strip()
                print "build number is: " + str(get_build_number)
                a.sshcmd_cli_upgrade(cas_ip_no_port, upgrade_path[x])
                ''' wait for image to upload successfully'''
                status = True
                timeout = 0
                while status == True:
                    a.sshcmd_port22(cas_ip_no_port)
                    file1 = open("testlog.txt","r")
                    for line in file1:
                        if get_build_number in line:
                            print "Image uploaded successfully"
                            status = False
                        else:
                            time.sleep(4)
                            timeout +=4
                            if timeout >=1800:
                                print "Failed to uplaod image. Manual investigation required."
                                status = False
                print "rebooting appliance"
                a.reboot(cas_ip_no_port)
                '''wait for system to reboot'''
                status = True
                timeout = 0
                while status ==True:
                    a.wait_for_reboot(cas_ip_no_port)
                    file1 = open("testlog.txt","r")
                    for line in file1:
                        if "bytes" in line:
                            print "Box is up and running successfully after reboot."
                            status = False
                        else:
                            time.sleep(4)
                            timeout +=4
                            if timeout >=900:
                                print "Box not reachable after reboot. Manual Investigation required."
                                status = False
    
   
if __name__ == '__main__':
    unittest.main() 