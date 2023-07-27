#################################################################
# Program to create a user using RAPI                           #
# Author: Rajiv Bhalla                                          #                  
# Prerequisite: User with username rbhalla does not exist.      #
#                                                               #
#################################################################

#!/usr/bin/python

import os, time

print "#### Generating the token"
os.system('curl -k -s -X POST -d "username=admin&password=admin" https://192.168.3.39/rapi/auth/session > token.txt') ## output store to retrieve the token
os.system("token=`cat token.txt | grep token | awk '{print $2}' | cut -d ',' -f1` && echo -n $token | tail -c +2 | head -c -1 > api_key") ## saved the key to a file
  
print "\n#### Creating a user with username 'rbhalla'"
os.system('curl -k -s -X POST -d "username=rbhalla&ui_password=bluecoat&ui_roles=administrator" https://192.168.3.39/rapi/system/users?token=`cat api_key` > uid.txt') ## create user "rbhalla" 
  
print "\n#### Adding the email ID to the user created above."
os.system("uid=`cat uid.txt | grep users_uid | awk '{print $2}' | cut -d ',' -f1` && curl -k -s -X POST -d "'email=rajiv.bhalla@bluecoat.com'" https://192.168.3.39/rapi/system/users/$uid?token=`cat api_key`") ## add email id
  
print "\n #### Getting the existing users list"
os.system('curl -k -s -X GET https://192.168.3.39/rapi/system/users?token=`cat api_key` | tee usercreate.txt') ## get users list    
 
time.sleep(2)
fo = open("usercreate.txt", "r+")
  
if ('"users_username": "rbhalla"' in fo.read()):
    print "\n\nUser with username rbhalla created successfully."
else:
    print "Failed to create user with username 'rbhalla'"
fo.close()
 
#### Remove the files created during this task
 
os.remove("token.txt")
os.remove("api_key")
os.remove("uid.txt")
os.remove("usercreate.txt")