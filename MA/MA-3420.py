import requests, httplib, urllib, json, unittest, time, sys, select, paramiko, requests
import os
import ssl

#from settings import *
ma_ip = "10.138.128.2"
ssh_user = "g2"
ssh_password = "password"





def sshpara(ma_ip, cmd, ssh_user, ssh_password ):
    for i in range(1, 31):
        while True:
            print "Trying to connect to %s (%i/30)" % (ma_ip, i)
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ma_ip, username=ssh_user,password=ssh_password)
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
                    print "hello"
                    print stdout.channel.recv(1024),
        
        #
        # Disconnect from the host
        #
        #print "Command done, closing SSH connection"
        ssh.close()
        
def powerstate(timeout):
    i = 0
    while (i < timeout):
        cmd = "supervisorctl status | grep web-router:web-router-443 | grep -i running | wc -l"
        sshpara(ma_ip, cmd, ssh_user, ssh_password)
        fp = open ("ssh.txt", "r").read()
        if "1" in fp:
            print "Machine is up and running"
            break
        else:
            i+=1
    if (i >= timeout):
        print "Machine is not up after reverting and waiting for " + str(timeout) + " seconds."    
        print "Manual investigation is requied."

### Check power state ###
powerstate("120")