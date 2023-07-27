import requests, httplib, urllib, json, unittest, time, sys, select, paramiko, requests
import os
import ssl

from settings import *
from settings import settings_dict

################## Common Functions ######################

def revert(maversion):
	if maversion == "4.2.5.20150622-RELEASE":
		cmd='vim-cmd vmsvc/snapshot.revert 102 16 suppressPowerOff; vim-cmd vmsvc/power.on 102'
		sshpara("10.138.128.185", cmd, "rajiv", "!Q@W#E$R%T12345")
		## check power state ####
		powerstate("120")
	
	elif maversion == "4.2.6.20150714-RELEASE":
				cmd='vim-cmd vmsvc/snapshot.revert 102 17 suppressPowerOff; vim-cmd vmsvc/power.on 102'
				sshpara("10.138.128.185", cmd, "rajiv", "!Q@W#E$R%T12345")
				## check power state ####
				powerstate("120")
	
	elif maversion == "4.2.7.20150924-RELEASE":
				cmd='vim-cmd vmsvc/snapshot.revert 102 18 suppressPowerOff; vim-cmd vmsvc/power.on 102'
				sshpara("10.138.128.185", cmd, "rajiv", "!Q@W#E$R%T12345")
				## check power state ####
				powerstate("120")
				
	elif maversion == "4.2.8.20160219-RELEASE":
				cmd='vim-cmd vmsvc/snapshot.revert 102 19 suppressPowerOff; vim-cmd vmsvc/power.on 102'
				sshpara("10.138.128.185", cmd, "rajiv", "!Q@W#E$R%T12345")
				## check power state ####
				powerstate("120")
				
	elif maversion == "4.2.9":
				cmd='vim-cmd vmsvc/snapshot.revert 102 20 suppressPowerOff; vim-cmd vmsvc/power.on 102'
				sshpara("10.138.128.185", cmd, "rajiv", "!Q@W#E$R%T12345")
				## check power state ####
				powerstate("120")

def get_install_patternversion(ma_ip):
	values = {'token': token}
	headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
	values = urllib.urlencode(values)
	try:
		conn = httplib.HTTPSConnection(ma_ip,context = ssl._create_unverified_context())
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
						conn = httplib.HTTPSConnection(ma_ip,context = ssl._create_unverified_context())
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
								conn = httplib.HTTPSConnection(ma_ip,context = ssl._create_unverified_context())
							except AttributeError:
								conn = httplib.HTTPSConnection(ma_ip)
							conn.request("GET", "/rapi/system/version_info?token="+token)
							response =conn.getresponse()
							data = response.read()
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

def download_pdfs(task_id):
	### Create a directory to save the task reports ###
	try:
		os.mkdir(os.path.join(os.getcwd(), os.path.join(settings_dict["task_report_folder"]+settings_dict["execution_id"])))
	except:
		pass
	try:
		conn = httplib.HTTPSConnection(settings_dict["ma_ip"],context = ssl._create_unverified_context())
	except AttributeError:
		conn = httplib.HTTPSConnection(settings_dict["ma_ip"])
	conn.request("GET", "/rapi/widgets/task_report/"+ str(task_id) + "?output=pdf&token=" + token)
	response =conn.getresponse()
	data = response.read()
	report = open(os.path.join(os.getcwd(), str(settings_dict["task_report_folder"]) + str(settings_dict["execution_id"])+"/" + "taskreport_"+str(task_id)+".pdf"), "w")
	report.write(data)
	report.close()
	
def sshpara(host, cmd, user, password1 ):
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

def powerstate(timeout):
	i = 0
	while (i < timeout):
		cmd = "supervisorctl status | grep web-router:web-router-443 | grep -i running | wc -l"
		sshpara(settings_dict["ma_ip"], cmd, settings_dict["ssh_user"], settings_dict["ssh_password"])
		fp = open ("ssh.txt", "r").read()
		if "1" in fp:
			print "Machine is up and running"
			break
		else:
			i+=1
	if (i >= timeout):
		print "Machine is not up after reverting and waiting for " + str(timeout) + " seconds."	
		print "Manual investigation is requied."

def check_power():
	cmd = "vim-cmd vmsvc/power.getstate 102"
	sshpara("10.138.128.185", cmd, "rajiv", "!Q@W#E$R%T12345")
	fp = open ("ssh.txt", "r").read()
	if "Powered off" in fp:
		print "Machine is powered off. Need to turn it on."
		cmd = "vim-cmd vmsvc/power.on 102"
		sshpara("10.138.128.185", cmd, "rajiv", "!Q@W#E$R%T12345")
		powerstate("120")			
	elif "Powered on" in fp:
		print "Machine is already powered on. Proceeding with the script."
			
def generate_token(ma_ip):
	values = {'username': settings_dict["ma_adminuser"], 'password': settings_dict["ma_password"]}
	headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
	values = urllib.urlencode(values)
	try:
		conn = httplib.HTTPSConnection(settings_dict["ma_ip"],context = ssl._create_unverified_context())
	except AttributeError:
		conn = httplib.HTTPSConnection(settings_dict["ma_ip"])
	conn.request("POST", "/rapi/auth/session", values, headers)
	response = conn.getresponse()
	data = response.read()
	fdata =json.loads(data)
	global token
	token = fdata['results']['session_token_string']
	print "Generated token is: " + token
	conn.close()
	
def getmaversion(ma_ip):
	#values = {'token' : token}
	#headers = {'User-Agent': 'python', 'Content-type': "application/x-www-form-urlencoded"}
	#values = urllib.urlencode(values)
	try:
		conn = httplib.HTTPSConnection(settings_dict["ma_ip"],context = ssl._create_unverified_context())
	except AttributeError:
		conn = httplib.HTTPSConnection(settings_dict["ma_ip"])
	conn.request("GET", "/rapi/system/version_info?token="+token)
	response =conn.getresponse()
	data = response.read()
	fdata = json.loads(data)
	global check_version
	check_version = fdata['results']['mag2_version']
	protocol_buffer_revision = fdata['results']['protocol_buffer_revision']
	system_platform = fdata['results']['system_product_name']
	serial_number = fdata['results']['system_serial_number']
	pattern_version= fdata['results']['patterns_version']
	#print "Pattern version on "+str(ma_ip)+ " is "+ str(pattern_version)
	print "MA version on "+str(ma_ip)+ " is "+ str(check_version)
	#print "Protocol buffer revision on "+str(ma_ip)+ " is "+ str(protocol_buffer_revision)
	#rint "System Platform on "+str(ma_ip)+ " is "+ str(system_platform)
	#print "Serial number of the appliance "+str(ma_ip)+ " is "+ str(serial_number)
	conn.close()

def create_task(ivmprofile, sample_id):
	global task_id
	if ivmprofile == "":
		for ivmprofile in profiles.itervalues():
			print ivmprofile
			url = "https://"+ settings_dict["ma_ip"] +  "/rapi/tasks"
			values = {'sample_id': sample_id, 'env': env, 'ivm_profile': ivmprofile, 'tp_IVM.TIMEOUT': timeout, 'tp_FILTER.SET.V1.FULL': captureall, 'tp_DEF.log_task': tasklog, 'token' : token}
			r = requests.post(url, data=values, verify=False)
			task_response=r.text
			#print task_response
			data = json.loads(task_response)
			task_id = data['results'][0]['tasks_task_id']
			f = open ('taskid.txt', 'a')
			f.write ( str(task_id) + '\n' )
			f.close()
			print "Task ID is: " + str(task_id)
	else:
		url = "https://"+ settings_dict["ma_ip"] +  "/rapi/tasks"
		values = {'sample_id': sample_id, 'env': env, 'ivm_profile': ivmprofile, 'tp_IVM.TIMEOUT': timeout, 'tp_FILTER.SET.V1.FULL': captureall, 'tp_DEF.log_task': tasklog, 'token' : token}
		r = requests.post(url, data=values, verify=False)
		task_response=r.text
		#print task_response
		data = json.loads(task_response)
		#global task_id
		task_id = data['results'][0]['tasks_task_id']
		f = open ('taskid.txt', 'a')
		f.write ( str(task_id) + '\n' )
		f.close()
		print "Task ID is: " + str(task_id)
		
def gettaskriskscore(task_id):
	#f = task_id.strip()
	try:
		conn = httplib.HTTPSConnection(settings_dict["ma_ip"],context = ssl._create_unverified_context())
	except AttributeError:
		conn = httplib.HTTPSConnection(settings_dict["ma_ip"])
	conn.request("GET", "/rapi/tasks/"+ str(task_id) +"?token=" + token)
	response =conn.getresponse()
	data = response.read()
	fdata = json.loads(data)
	risk_score= fdata['results'][0]['tasks_global_risk_score']
	print "Risk Score for the task id "+ str(task_id) + " is "+ str(risk_score)
	riskscore = open("riskscorefile.txt", "a")
	riskscore.write("Risk Score for the task id "+ str(task_id) + " is "+ str(risk_score)+"\n")
	riskscore.close()
	conn.close()

def get_taskstate(task_id):
	state = ""
	while (state != "CORE_COMPLETE"):
		try:
			conn = httplib.HTTPSConnection(settings_dict["ma_ip"],context = ssl._create_unverified_context())
		except AttributeError:
			conn = httplib.HTTPSConnection(settings_dict["ma_ip"])
		conn.request("GET", "/rapi/tasks/"+str(task_id)+"?token="+token)
		response =conn.getresponse()
		data = response.read()
		fdata = json.loads(data)
		state= fdata['results'][0]['task_state_state']
		if state == "CORE_COMPLETE":
			print "Task state for task id " + str(task_id) + " is: " + str(state)
			download_pdfs(task_id)
			gettaskriskscore(task_id)
		else:
			print "Task state for task id " + str(task_id) + " is: " + str(state)
			time.sleep(10)
			pass
		conn.close()
		
def upload_samples(ivmprofile):
	try:
		if os.path.exists("sampleid.txt"):
			os.remove("sampleid.txt")
		if os.path.exists("output.txt"):
			os.remove("output.txt")
		if os.path.exists("taskid.txt"):
			os.remove("taskid.txt")
		if os.path.exists("riskscorefile.txt"):
			os.remove("riskscorefile.txt")
		if os.path.exists("ssh.txt"):
			os.remove("ssh.txt")
	except:
		print "File does not exist."
	fp = os.path.join(os.getcwd(),"samples")
	file1 =  os.listdir(fp)
	for entry in file1:
		file2 = fp+"/"+entry
		print file2
		url = "https://"+ settings_dict["ma_ip"] +  "/rapi/samples/basic"
		#print url
		samples = {'file': open(file2, 'rb')}
		values = {'owner': 'admin','extension' : 'exe','token' : token}
		r = requests.post(url, files=samples, data=values, verify=False)       
		sample_response=r.text # JSON RESPONSE FOR THE SAMPLE
		data = json.loads(sample_response)
		sample_id = data['results'][0]['samples_sample_id']
		f = open ('sampleid.txt', 'a')
		f.write ( str(sample_id) + '\n' )
		f.close()
		print "Sample ID is: " + str(sample_id)
		create_task(ivmprofile,sample_id)
	f = open ('taskid.txt')
	for task_id in f:
		task_id = task_id.strip()
		get_taskstate(task_id)
		
def list_profiles(maversion):
	print "Please select the profile from the list below where you would like to execute the sample:"
	print "1) Windows7 32-bit"
	print "2) Windows7 64-bit"
	print "3) Windows XP"
	print "4) Windows 8 64-bit"
	print "5) all"
	profile_selected = str(raw_input("Please enter your choice as 1,2,3,4, or 5: "))
	
	check_power()
	if profile_selected == "1":
		generate_token(settings_dict["ma_ip"])
		getmaversion(settings_dict["ma_ip"])
		ivmprofile = profiles["win7"]
		global timeout
		global captureall
		global tasklog
		if check_version == maversion:
			print "MA box is running on the same selected version. No need to revert"
			print "Check pattern version updated or not"
			get_install_patternversion(settings_dict["ma_ip"])
			print "done"
			print "Uploading the samples..."
			upload_samples(ivmprofile)
			with open("riskscorefile.txt", 'r') as fin:
				print fin.read()
			try:
				if os.path.exists("sampleid.txt"):
					os.remove("sampleid.txt")
				if os.path.exists("output.txt"):
					os.remove("output.txt")
				if os.path.exists("taskid.txt"):
					os.remove("taskid.txt")
				if os.path.exists("riskscorefile.txt"):
					os.remove("riskscorefile.txt")
				if os.path.exists("ssh.txt"):
					os.remove("ssh.txt")
			except:
				pass
		else:
			print "MA box is not running on "+ maversion
			print "So reverting the box to "+ maversion
			revert(maversion)
			generate_token(settings_dict["ma_ip"])
			print "Check pattern version updated or not"
			get_install_patternversion(settings_dict["ma_ip"])
			upload_samples(ivmprofile)
			with open("riskscorefile.txt", 'r') as fin:
				print fin.read()
			try:
				if os.path.exists("sampleid.txt"):
					os.remove("sampleid.txt")
				if os.path.exists("output.txt"):
					os.remove("output.txt")
				if os.path.exists("taskid.txt"):
					os.remove("taskid.txt")
				if os.path.exists("riskscorefile.txt"):
					os.remove("riskscorefile.txt")
				if os.path.exists("ssh.txt"):
					os.remove("ssh.txt")
			except:
				print "File does not exist."
	
	elif profile_selected == "2":	
		generate_token(settings_dict["ma_ip"])
		getmaversion(settings_dict["ma_ip"])
		ivmprofile = profiles["win7x64"]
		global timeout
		global captureall
		global tasklog

		if check_version == maversion:
			print "MA box is running on the same selected version. No need to revert"
			print "Check pattern version updated or not"
			get_install_patternversion(settings_dict["ma_ip"])
			print "done"
			print "Uploading the samples..."
			upload_samples(ivmprofile)
			with open("riskscorefile.txt", 'r') as fin:
				print fin.read()
			try:
				if os.path.exists("sampleid.txt"):
					os.remove("sampleid.txt")
				if os.path.exists("output.txt"):
					os.remove("output.txt")
				if os.path.exists("taskid.txt"):
					os.remove("taskid.txt")
				if os.path.exists("riskscorefile.txt"):
					os.remove("riskscorefile.txt")
				if os.path.exists("ssh.txt"):
					os.remove("ssh.txt")
			except:
				pass
		else:
			print "MA box is not running on "+ maversion
			print "So reverting the box to "+ maversion
			### Revert the machine to the selected version of MA #####
			generate_token(settings_dict["ma_ip"])
			print "Check pattern version updated or not"
			get_install_patternversion(settings_dict["ma_ip"])
			upload_samples(ivmprofile)
			with open("riskscorefile.txt", 'r') as fin:
				print fin.read()
			try:
				if os.path.exists("sampleid.txt"):
					os.remove("sampleid.txt")
				if os.path.exists("output.txt"):
					os.remove("output.txt")
				if os.path.exists("taskid.txt"):
					os.remove("taskid.txt")
				if os.path.exists("riskscorefile.txt"):
					os.remove("riskscorefile.txt")
				if os.path.exists("ssh.txt"):
					os.remove("ssh.txt")
			except:
				print "File does not exist."

	elif profile_selected == "3":	
		generate_token(settings_dict["ma_ip"])
		getmaversion(settings_dict["ma_ip"])
		ivmprofile = profiles["winxp"]
		global timeout
		global captureall
		global tasklog

		if check_version == maversion:
			print "MA box is running on the same selected version. No need to revert"
			print "Check pattern version updated or not"
			get_install_patternversion(settings_dict["ma_ip"])
			print "done"
			print "Uploading the samples..."
			upload_samples(ivmprofile)
			with open("riskscorefile.txt", 'r') as fin:
				print fin.read()
			try:
				if os.path.exists("sampleid.txt"):
					os.remove("sampleid.txt")
				if os.path.exists("output.txt"):
					os.remove("output.txt")
				if os.path.exists("taskid.txt"):
					os.remove("taskid.txt")
				if os.path.exists("riskscorefile.txt"):
					os.remove("riskscorefile.txt")
				if os.path.exists("ssh.txt"):
					os.remove("ssh.txt")
			except:
				pass
		else:
			print "MA box is not running on "+ maversion
			print "So reverting the box to "+ maversion
			### Revert the machine to the selected version of MA #####
			revert(maversion)
			generate_token(settings_dict["ma_ip"])
			print "Check pattern version updated or not"
			get_install_patternversion(settings_dict["ma_ip"])
			upload_samples(ivmprofile)
			with open("riskscorefile.txt", 'r') as fin:
				print fin.read()
			try:
				if os.path.exists("sampleid.txt"):
					os.remove("sampleid.txt")
				if os.path.exists("output.txt"):
					os.remove("output.txt")
				if os.path.exists("taskid.txt"):
					os.remove("taskid.txt")
				if os.path.exists("riskscorefile.txt"):
					os.remove("riskscorefile.txt")
				if os.path.exists("ssh.txt"):
					os.remove("ssh.txt")
			except:
				print "File does not exist."
				
	elif profile_selected == "4":	
		generate_token(settings_dict["ma_ip"])
		getmaversion(settings_dict["ma_ip"])
		ivmprofile = profiles["win8"]
		global timeout
		global captureall
		global tasklog

		if check_version == maversion:
			print "MA box is running on the same selected version. No need to revert"
			print "Check pattern version updated or not"
			get_install_patternversion(settings_dict["ma_ip"])
			print "done"
			print "Uploading the samples..."
			upload_samples(ivmprofile)
			with open("riskscorefile.txt", 'r') as fin:
				print fin.read()
			try:
				if os.path.exists("sampleid.txt"):
					os.remove("sampleid.txt")
				if os.path.exists("output.txt"):
					os.remove("output.txt")
				if os.path.exists("taskid.txt"):
					os.remove("taskid.txt")
				if os.path.exists("riskscorefile.txt"):
					os.remove("riskscorefile.txt")
				if os.path.exists("ssh.txt"):
					os.remove("ssh.txt")
			except:
				pass
		else:
			print "MA box is not running on "+ maversion
			print "So reverting the box to "+ maversion
			### Revert the machine to the selected version of MA #####
			revert(maversion)
			generate_token(settings_dict["ma_ip"])
			print "Check pattern version updated or not"
			get_install_patternversion(settings_dict["ma_ip"])
			upload_samples(ivmprofile)
			with open("riskscorefile.txt", 'r') as fin:
				print fin.read()
			try:
				if os.path.exists("sampleid.txt"):
					os.remove("sampleid.txt")
				if os.path.exists("output.txt"):
					os.remove("output.txt")
				if os.path.exists("taskid.txt"):
					os.remove("taskid.txt")
				if os.path.exists("riskscorefile.txt"):
					os.remove("riskscorefile.txt")
				if os.path.exists("ssh.txt"):
					os.remove("ssh.txt")
			except:
				print "File does not exist."
				
	elif profile_selected == "5":
		generate_token(settings_dict["ma_ip"])
		getmaversion(settings_dict["ma_ip"])
		global timeout
		global captureall
		global tasklog

		if check_version == maversion:
			print "MA box is running on the same selected version. No need to revert"
			print "Check pattern version updated or not"
			get_install_patternversion(settings_dict["ma_ip"])
			print "done"
			print "Uploading the samples..."
			ivmprofiles = ""
			upload_samples(ivmprofiles)
			with open("riskscorefile.txt", 'r') as fin:
				print fin.read()
			try:
				if os.path.exists("sampleid.txt"):
					os.remove("sampleid.txt")
				if os.path.exists("output.txt"):
					os.remove("output.txt")
				if os.path.exists("taskid.txt"):
					os.remove("taskid.txt")
				if os.path.exists("riskscorefile.txt"):
					os.remove("riskscorefile.txt")
				if os.path.exists("ssh.txt"):
					os.remove("ssh.txt")
			except:
				pass
		else:
			print "MA box is not running on "+ maversion
			print "So reverting the box to "+ maversion
			revert(maversion)
			generate_token(settings_dict["ma_ip"])
			print "Check pattern version updated or not"
			get_install_patternversion(settings_dict["ma_ip"])
			upload_samples(ivmprofile)
			with open("riskscorefile.txt", 'r') as fin:
				print fin.read()
			try:
				if os.path.exists("sampleid.txt"):
					os.remove("sampleid.txt")
				if os.path.exists("output.txt"):
					os.remove("output.txt")
				if os.path.exists("taskid.txt"):
					os.remove("taskid.txt")
				if os.path.exists("riskscorefile.txt"):
					os.remove("riskscorefile.txt")
				if os.path.exists("ssh.txt"):
					os.remove("ssh.txt")
			except:
				print "File does not exist."
