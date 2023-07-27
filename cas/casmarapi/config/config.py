#cas_ip="[fd00:651::ac7:6e47]:8082"
cas_ip="10.199.110.31:8082"
cas_ip_no_port="10.199.107.17"
cas_adminuser="admin"
cas_adminpass="admin123"
cas_https_ip="https://10.199.107.17:8082"
cas_http_ip="http://10.199.110.71:8081"
proxy_ip="10.199.117.134"
skiptest="false"

### Preactivated base image urls ####
win7="http://10.199.97.68/casma/activated_base_image/138.11/kvm0.4/128.18/activated.qcow2.bundle"
win7_key="H6DQC-94G22-4QWK6-93R8Y-H8Q7B"
win10_old="http://10.199.97.68/casma/activated_base_image/128.18/win10x64/activated.qcow2.bundle"
win10_new="http://10.199.97.68/casma/exported_base_img_profile/win10x64.b7ccf912d6e34a8410859da4a9eab86f.TY8RT-VNF79-8Q78W-TK32Q-7T9R8.base"
win10_new_ipv6="http://[fd00:601::ac7:6144]/casma/exported_base_img_profile/win10x64.b7ccf912d6e34a8410859da4a9eab86f.TY8RT-VNF79-8Q78W-TK32Q-7T9R8.base"
win10_key_old="MD6N3-XJ9JM-Y2QYD-HHKP4-2KCJW"
#win7_new="http://10.199.97.68/casma/exported_base_img_profile/win7x64.39134fad6ccc6292a5e81a5dcedc4d13.6HFGF-GV9FD-6P7YM-XBTK9-VD8DV.base"
win7_new="http://10.199.97.68/casma/exported_base_img_profile/Rajiv/win7_baseImage_profile_automation/win7x64-sp1-base.bundle"
win7_new_ipv6="http://[fd00:601::ac7:6144]/casma/exported_base_img_profile/Rajiv/win7_baseImage_profile_automation/win7x64-sp1-base.bundle"
win10_key="MD6N3-XJ9JM-Y2QYD-HHKP4-2KCJW"
win10_key_trial="TRIAL"
win7_key_trial="TRIAL"
''' ### 2.3 config ### '''
win7_iso="http://10.199.97.67/casma/iso_import/base_img_bundle/WIN7-x17-58517-39134fad6ccc6292a5e81a5dcedc4d13.iso"
win7_activated_bundle="http://10.199.97.68/casma/activated_base_image/128.18/2.3/win7x64.39134fad6ccc6292a5e81a5dcedc4d13.6HFGF-GV9FD-6P7YM-XBTK9-VD8DV.bundle"
iso_type_win7="win7x64-sp1"
win7_iso_key="6HFGF-GV9FD-6P7YM-XBTK9-VD8DV"
winxp="http://10.199.97.68/casma/exported_base_img_profile/Rajiv/winxp-sp3-01D6F71EJZJYQ7C30XTEJ9AM59_B8WXQ-F84RR-TFM2D-MTXRR-TM88D.base"
winxp_3_0="http://10.199.97.68/casma/exported_base_img_profile/Rajiv/XP_3_0_1_0_239934/winxp-sp3-01DGC5KVZT1SQYG0328BCNC26E.bundle"
winxp_key="B8WXQ-F84RR-TFM2D-MTXRR-TM88D"

plugin="ghost_user.py"


### TASK SETTINGS #### (ghost = ghost_user.py, ie= run-iexplore.py, no_plugin='')
#
task_settings = { 'plugin':'ghost_user.py',
                  'ma_ip':'10.138.129.45', 
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

supported_lang = {'french_canada': 'fr-CA',
                  'french_france':'fr-FR',
                  'japanese':'ja-JP',
                  'American English': 'en-US',
                  'Spanish':'es-ES',
                  'portu':'pt-PT' 
                    }
