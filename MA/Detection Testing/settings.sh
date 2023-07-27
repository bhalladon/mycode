#!/bin/bash

########### TEST DATA #########
ma="10.138.128.2"
ma_adminuser="admin"
ma_password="admin"
sample_dir="samples"
mysql_user="root"
mysql_pass="mysql"
database="result"
execution_id="chakde"
hashfile="hash.txt"

case "$ma" in
		"10.138.128.2")
		win8="windows-8-64-bit"
		winxp="windowsxpsp3"
		win7="win732bitsp1"
		win7x64="win7x64sp1"
		;;
		
		"10.138.128.180")
		win8="windows-8-64-bit"
		win7="win7-sp1-32bit"
		;;
		
		"10.138.128.35"|"10.138.128.36"|"10.138.128.66"|"10.138.128.67"|"10.138.128.68")
		win8="windows-8-64-bit"
		winxp="windows-xp"
		win7="windows-7"
		win7x64="windows-7-64-bit"
		;;
		
		"10.138.128.4")
		win8="windows8x64"
		winxp="windowsxp"
		win7="windows7"
		win7x64="windows7x64"
		;;
		
		"10.138.129.46")
		win7x64="win7x64"
		;;
esac

#win7x64="win7x64"
##### TASK Settings #####
envtype="ivm"
timeout="60"
firewall=3 ##1=isolated 2 = Limited 3=Unlimited
plugin=""
#plugin="ghost_user.py"

tasklog=1 ## 1=ON
getdropfiles=1 ## 1=ON
captureall=1 ## ON (Detailed Capture)
###############################
