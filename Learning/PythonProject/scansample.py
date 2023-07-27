#!/usr/bin/python

from common_functions import *
ma_ip = "10.138.128.2"
ssh_user = "g2"
ssh_password = "password"


def selectmaversion():	
	print "Please select the MA version from the list below where you would like to execute the sample:"
	print "1) 4.2.5.20150622-RELEASE"
	print "2) 4.2.6.20150714-RELEASE"
	print "3) 4.2.7.20150924-RELEASE"
	print "4) 4.2.8.20160219-RELEASE"
	print "5) 4.2.9.20160219-RELEASE"
	user_input = str(raw_input("Please enter your choice as 1,2,3,4, or 5: "))
	
	if user_input == "1": 
		maversion="4.2.5.20150622-RELEASE"	
		list_profiles(maversion)
	elif user_input == "2":
		maversion="4.2.6.20150714-RELEASE"
		list_profiles(maversion)
	elif user_input == "3":
		maversion="4.2.7.20150924-RELEASE"
		list_profiles(maversion)
	elif user_input == "4":		
		maversion="4.2.8.20160219-RELEASE"
		list_profiles(maversion)
	elif user_input == "5":
		maversion="4.2.9.20160520-RELEASE"
		list_profiles(maversion)
	else:
		print "please enter a valid choice:"
		selectmaversion()

selectmaversion()
powerstate("120")
