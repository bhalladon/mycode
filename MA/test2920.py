'''Author: Rajiv Bhalla'''

import httplib, urllib, time, paramiko, sys, select
import simplejson as json
import ssl
import socket

ma_ip = "10.138.128.2"
ma_adminuser = "admin"
ma_adminpass = "admin"
ma_sshuser = "g2"
ma_sshpass = "password"
backupfile_location = "~/mag2.conf_bak"

''' Before executing the script, make sure to take a backup of the "/etc/mag2/mag2.conf" file, so that if any issue occurs than
the backup file can be used to revert the changes '''


def exec_cmd(ma_ip,ma_sshuser,ma_sshpass,command):
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
            #print "Connected to %s" % ma_ip
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


def generate_token(ma_ip):
    values = {'username': ma_adminuser, 'password': ma_adminpass}
    headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
    values = urllib.urlencode(values)
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
    print "Generated token is: " + token
    conn.close()
   
def post_data_with_quotes(test_data):
    if "base.win7.memory" in test_data:
        config = "ivm"
        print "[IVM]"
    if "master" in test_data:
        config = "bootstrap"
        print "\n[BOOTSTRAP]"
    if "sandbox_def" in test_data:
        config = "main"
        print "\n[MAIN]"
    if "mag2_backend_server" in test_data:
        config = "network"
        print "\n[NETWORK]"
    if "database_partition" in test_data:
        config = "mag2w"
        print "\n[MAG2W]"
    if "mag2w_debug" in test_data:
        config = "mag2w_constants"
        print "\n[MAG2W_CONSTANTS]"
    if "pause_processing" in test_data:
        config = "environments"
        print "\n[ENVIRONMENTS]"
    if "read_config" in test_data:
        config = "rapi"
        print "\n[RAPI]"
    if "log_insert_stats" in test_data:
        config = "debug"
        print "\n[DEBUG]"
    if "update_period" in test_data:
        config = "vtopd"
        print "\n[VTOPD]"  
    if "company_name" in test_data:
        config = "brand"
        print "\n[BRAND]"
    if "auto_download" in test_data:
        config = "updates"
        print "\n[UPDATES]"
    if "keep_interval" in test_data:
        config = "cleanup"
        print "\n[CLEANUP]"
    if "gpb_storage_class" in test_data:
        config = "defaults"
        print "\n[DEFAULTS]"
    if "manufacturer" in test_data:
        config = "system"
        print "\n[SYSTEM]"
    if "state" in test_data:
        config = "health"
        print "\n[HEALTH]"
    if "adb_path" in test_data:
        config = "android"
        print "\n[ANDROID]"
    if "refresh_interval" in test_data:
        config = "webpulse"
        print "\n[WEBPULSE]"
    if "file_reputation.enabled" in test_data:
        config = "analytics"
        print "\n[ANALYTICS]"
    if "emet.enable" in test_data:
        config = "ivmservice"
        print "\n[IVMSERVICE]"
    if "ivm.tp_IVM.TIMEOUT" in test_data:
        config = "task-defaults"
        print "\n[TASK-DEFAULTS]"
    if "stage" in test_data:
        config = "wizard"
        print "\n[WIZARD]"                
    if "servers" in test_data:
        config = "ntp"
        print "\n[NTP]"
    if "community" in test_data:
        config = "snmp"
        print "\n[SNMP]"        
    if "timeout" in test_data:
        config = "ivm_watchdog"
        print "\n[IVM_WATCHDOG]"
    if "vbox.enabled" in test_data:
        config = "nse"
        print "\n[NSE]"
    if "url" in test_data:
        config = "telemetry"
        print "\n[TELEMETRY]"        
        
                    
    values = {}
    headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
    values = urllib.urlencode(values)
    try:
        conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
    except AttributeError:
        conn = httplib.HTTPSConnection(ma_ip)
        
    for df in test_data:
        time.sleep(1)
        conn.request("GET", "/rapi/system/config/"+config+"."+str(df)+"?token="+token, values, headers)
        response = conn.getresponse()
        data = response.read()
        #print data
        if response.status == 200:
            fdata =json.loads(data)
            old_value = fdata['results'][0]['value']
        ''' POST new value '''
        #values = {"value": '"'+old_value+'"', "token":token}
        values = {"value": old_value+'"\'', "token":token}
        values = urllib.urlencode(values)
        try:
            conn.request("POST", "/rapi/system/config/"+config+"."+str(df), values, headers)
        except socket.error:
            pass
        response = conn.getresponse()
        if response.status == 200:
            values = {}
            values = urllib.urlencode(values)
            try:
                conn = httplib.HTTPSConnection(ma_ip, context=ssl._create_unverified_context())
            except AttributeError:
                conn = httplib.HTTPSConnection(ma_ip)
            time.sleep(1)
            conn.request("GET", "/rapi/system/config/"+config+"."+str(df)+"?token="+token, values, headers)
            response = conn.getresponse()
            data = response.read()
            #print data
            fdata =json.loads(data)
            new_value = fdata['results'][0]['value']
            print "For " + df +" Old Value is: " + old_value + " and new value is: " + new_value
            if old_value == new_value:
                print df
            ''' check whether df-config-mgr still running or not '''
            command =  "if [ `df-config-mgr --dump | grep -i \"unhandled exception\"\
                         | wc -l` -eq 1 ]; then echo \"FAIL\"; else :; fi"
            
            exec_cmd(ma_ip, ma_sshuser, ma_sshpass,command)
            ''' revert the changes '''
            command = "cp "+ backupfile_location + " /etc/mag2/mag2.conf"
            exec_cmd(ma_ip, ma_sshuser, ma_sshpass,command)
            
        elif response not in [200]:
            data = response.read()
            print df + data
        
        conn.close()    
                
def declare_config_values():

    generate_token(ma_ip)
    
    ivm = ["base.win7.memory",\
              "base.win7.name",\
              "base.win7.os_type",\
              "base.win7.path",\
              "base.win7x64.arch",\
              "base.win7x64.memory",\
              "base.win7x64.name",\
              "base.win7x64.os_type",\
              "base.win7x64.path",\
              "base.win8x64.arch",\
              "base.win8x64.memory",\
              "base.win8x64.name",\
              "base.win8x64.os_type",\
              "base.win8x64.path",\
              "base.winxp.memory",\
              "base.winxp.name",\
              "base.winxp.os_type",\
              "base.winxp.path",\
              "customize.pagefile.enable",\
              "customize.port_forwarding",\
              "drivers.profile-win7x64",\
              "drivers.profile-win7x86",\
              "drivers.profile-win8x64",\
              "drivers.profile-winxp",\
              "fakedisksize.enable",\
              "fakememorysize.enable",\
              "fileprotection.enable",\
              "hideprocesses.enable",\
              "hidereg.enable",\
              "ivmservice.dllinject.enable",\
              "ivmservice.enable",\
              "ivmservice.stacklimits.enable",\
              "limit_events",\
              "max_py_rss",\
              "monitorwmi.enable",\
              "proxy_server",\
              "sharkd.max_fs_size",\
              "sharkd.max_net_size",\
              "sharkd.max_reg_size",\
              "sharkd.max_sys_size"]
    
    bootstrap = ["master", "loglevel"]
    main1 = ["sandbox_def",\
                 "sandbox_bin",\
                "mqhost",\
                "rapi_templates",\
                "store_samples",\
                "tmp",\
                "samples_http",\
                "store_rsrcs",\
                "tcpdump",\
                "virus_total_key",\
                "local_storage",\
                "aws_key",\
                "aws_secret",\
                "aws_s3_bucket",\
                "system_type",\
                "mq_delivery_mode_persist",\
                "event_count_overflow",\
                "event_cache_expire",\
                "yara_enabled",\
                "yara_rule_file",\
                "admin_sql_path",\
                "sql_path",\
                "ivm_count",\
                "ivm_user",\
                "processors",\
                "sbx_count",\
                "enforce_console_password",\
                "yara_max_filesize",\
                "mvm_count",\
                "proxy_server",\
                "proxy_userinfo",\
                "mq_consume_events_count",\
                "accepted_eula",\
                "cascade_delete_profiles"]
    
    network_data = ["mag2_backend_server", "backend_if_name",\
                    "backend_if_mode","backend_if_address",\
                    "backend_if_netmask","backend_if_gateway",\
                    "internet_if_name","internet_if_mode",\
                    "internet_if_address","internet_if_netmask",\
                    "internet_if_gateway","dns_server",\
                    "external_ports","redirect_http",\
                    "ipv6.enabled","ipv6.backend_if_cidr",\
                    "ipv6.backend_if_gateway"]
    
    mag2w_data = ["database_partition","sample_storage",\
                  "json_host","json_rapi",\
                  "json_path_queues","json_user",\
                  "json_passwd","include_norm_stats",\
                  "log_level","mysql_username",\
                  "mysql_password","mysql_host",\
                  "mysql_database","mysql_sample_username",\
                  "mysql_sample_password","mysql_sample_host",\
                  "mysql_sample_database"]
    
    mag2w_constants = ["mag2w_debug","mag2w_session_name",\
                       "mag2w_session_timeout","mag2w_log_prefix",\
                       "mag2w_tpl_dir","mag2w_smarty_path",\
                       "mag2w_tpl_compile_dir","mag2w_tpl_cache_dir",\
                       "mag2w_json_temp","mag2w_simpletest_path",\
                       "mag2w_simpletest_url"]

    environments_data = ["pause_processing"]
    rapi_data = ["read_config","write_config","enable_authentication","session_duration"]
    debug_data = ["log_insert_stats","vbox4ivm"]

    vtopd_data = ["update_period","capture_frame_buffer","resize_frame_buffer"]
    
    brand_data = ["company_name","company_name_color",\
                  "product_name","product_name_short","example_host"]
    
    updates_data = ["auto_download","enabled","telemetry_url",\
                    "download_url","proxy_server","action_disruptive",\
                    "action_passive","passive_threshold","receive_beta",\
                    "no_versioncheck","update_url"]
    
    cleanup_data = ["keep_interval","min_interval","keep_score",\
                    "min_score","task_count","fifo",\
                    "score_before_age","yellow_limit",\
                    "red_limit","percentage_override"]
    
    defaults_data = ["gpb_storage_class","ivm.insomnia.enable",\
                    "ivm.pagefault.enable","ivm.paranormal.enable"]
    
    system_data = ["manufacturer","product_name","version",\
                    "serial_number","uuid","hw_addr"]
    
    health_data = ["state"]
    
    android_data = ["adb_path","emulator_path","emulator_args",\
                    "base_port","env_variables","netns_prefix",\
                    "blacklookup_path"]
    
    webpulse_data = ["refresh_interval","enabled",\
                     "lookup_timeout","online_lookups"]
    
    analytics_data = ["file_reputation.enabled","file_reputation.cache_hashes",\
                      "file_reputation.lookup_host","file_reputation.lookup_timeout",\
                      "file_reputation.cache_expire"]
    
    ivmservice_data = ["emet.enable"]
    
    taskdefaults_data = ["ivm.tp_IVM.TIMEOUT","ivm.tp_ANALYTICS.PCAP.CREATE_HAR",\
                          "ivm.primary_resource_id"]
    
    wizard_data = ["stage"]
    #ntp_data = ["servers","enabled"]
    #ntp_data = ["servers"]
    
    snmp_data = ["community","enabled"]
    
    ivm_watchdog_data = ["timeout","sleep"]
    
    nse_data = ["vbox.enabled","enabled","sbx.enabled","drd.enabled"]
    
    telemetry_data = ["url","enable"]

#     post_data_with_quotes(ivm)
#     post_data_with_quotes(main1)
#     post_data_with_quotes(network_data)
#     post_data_with_quotes(mag2w_data)
#     post_data_with_quotes(mag2w_constants)
#     post_data_with_quotes(environments_data)
#     post_data_with_quotes(debug_data)
#     post_data_with_quotes(vtopd_data)
    ##post_data_with_quotes(brand_data)
#     post_data_with_quotes(updates_data)
#     post_data_with_quotes(cleanup_data)
#     post_data_with_quotes(defaults_data)
#     post_data_with_quotes(system_data)
#     post_data_with_quotes(health_data)
#     post_data_with_quotes(android_data)
#     post_data_with_quotes(webpulse_data)
#     post_data_with_quotes(analytics_data)
#     post_data_with_quotes(ivmservice_data)
#     post_data_with_quotes(taskdefaults_data)
#     post_data_with_quotes(wizard_data)
# #     post_data_with_quotes(ntp_data)
#     post_data_with_quotes(snmp_data)
#     post_data_with_quotes(ivm_watchdog_data)
#     post_data_with_quotes(nse_data)
#     post_data_with_quotes(telemetry_data)
    ##post_data_with_quotes(bootstrap)
    post_data_with_quotes(rapi_data)
#     
declare_config_values()   
        
        