settings_dict = { 'ma_ip':'10.138.129.45', 
				  'ssh_user':'root',
				  'ssh_password': 'norman',
				  'ma_adminuser': 'admin',
				  'ma_password': 'admin',
				  'marootpassword': 'norman',
				  'sample_dir': 'samples',
				  'mysql_user': 'root',
				  'mysql_pass': 'mysql',
				  'database': 'result',
				  'execution_id': 'newtest',
				  'task_report_folder': 'task_report_'
			    }

### Profiles short names####

profiles = { 'win8': 'win8x64', 'winxp':'winxp', 'win7':'windows-7', 'win7x64':'win7x64' }

### MAchine ID and Snapshot Restore ID from ESXI machine#####
machine_id="102"
MA425_restore_id="16"
MA426_restore_id="10"
MA427_restore_id="11"
MA428_restore_id="12"
MA429_restore_id="13" 

##### TASK Settings #####
env="ivm"
timeout="60"
firewall=3 ##1=isolated 2 = Limited 3=Unlimited
plugin="ghost_user.py"
tasklog=1 ## 1=ON
getdropfiles=1 ## 1=ON
captureall=1 ## ON (Detailed Capture)
###############################

