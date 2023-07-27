rajifrom casmarapi.__init__ import *
#import zipfile,io
#from setuptools.unicode_utils import filesys_decode


class test_systeminfo(unittest.TestCase):

    def setUp(self):
        global a
        a = casutilities()
        global token
        token = a.generate_token()
    
    @unittest.skipIf(skiptest=="true", "kuch bhi chalega")      
    def test_a_getsysteminfo(self):
        import csv
        print token


#         f = a.upload_samples_dir(cas_ip, token)
#         for x in f:
#             a.create_task(x, 1, plugin, token)

        
        #values={'set_default':1} 
        #headers={'X-API-TOKEN':token}
        #f = a.httpcall("POST", "/rapi/system/vm/profiles/2", values, headers)
        #print f   
        #f = a.sshcmd_cli_upgrade(cas_ip_no_port, "no", "installed-systems load http://10.199.97.67/casma/build/casma_main_coe4/casma_main_coe4-244015.debug.bcsi")
#         f = a.sshcmd_cli_upgrade(cas_ip_no_port, "no", "installed-systems view")
#         if "244015" in f:
#             print "yes123"
#         else:
#             print "chakde"
        #print f
        #         for x in range(total_results):
#             version = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase)+"/iso_selection", values, headers)['results'][x]['display_name']
#             version = str(version).replace(' ', '')
#             print "version after removing spaces: " + str(version)
#             if version == win10_version:
#                 print "ghus gaya"
#                 global get_index
#                 get_index = a.httpcall("GET", "/rapi/system/vm/bases/"+str(addbase)+str("/iso_selection"), values, headers)['results'][x]['index']
#                 break  
        #f = a.sshcmd(cas_ip_no_port, "sed -n '/Setting state: 3/,/Setting state: 4/p' /opt/mag2/log/updater-daemon.log")
        #print f
        ##win7###
#         f = a.addiso_pull_23("http://10.199.97.67/casma/iso_import/base_img_bundle/WIN7-x17-58517-39134fad6ccc6292a5e81a5dcedc4d13.iso",\
#                                "6HFGF-GV9FD-6P7YM-XBTK9-VD8DV" , "win7x64", "win7x64-sp1", token, 3000, 1, "True")
        #Win10###
#         g = a.addiso_pull_23("http://10.199.97.67/casma/iso_import/Win10_1809Oct_v2_English_x64.iso",\
#                              "T2VNX-38V77-JFYKW-9WWVT-MKMQB" , "win10", "win10x64", token, 3000, 1, "True")
        # WinXp ###
#         h = a.addiso_pull_23("http://10.199.97.67/casma/iso_import/base_img_bundle/WINXP-X14-73315.iso",\
#                              "B8WXQ-F84RR-TFM2D-MTXRR-TM88D" , "winxpbase1", "winxp-sp3", token, 3000, 1, "False")

        
        #a.sshcmd_cli_sg(proxy_ip, "no", "show appliance-name")
#         a.download_license()
        #f = a.upload_samples_dir(cas_ip, token)
#         threads = list()
        '''>>>>>>>> Code for creating tasks using multi threads >>>>>>>>'''
#         for x in range(35,206):
#             #a.create_task(x, 1, plugin, token)
#             x = threading.Thread(target=a.create_task, args=(x, 1, plugin, token))
#             threads.append(x)
#             x.start()
#             if len(threads) % 100 == 0:
#                 while x.isAlive():
#                     pass
#         x.join()
#         print "All tasks created successfully"
        '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
#         for i in range(1001,1075):
#             x = threading.Thread(target=a.deletetasks, args=(i,i,10))
#             threads.append(x)
#             x.start()
#             if len(threads) % 100 == 0:
#                 while x.isAlive():
#                     pass
#         for x in threads:
#             x.join(10)
            
        

        #a.buildvmprofile(1, 1, token, 1200)
        #f = a.sshcmd_cli(cas_ip_no_port, config = "no",command='web-management browser-inactivity-timeout 180')
        #f = a.sshcmd_cli(cas_ip_no_port, config = "no",command='web-management browser-inactivity-timeout')
        #print f
        #a.addbaseimage(win7, win7_key, token, 20000)
        #a.addbaseimage(win10_old, win10_key_old, token, 20000)s
       
        a.addbaseimage_23(win7_new, token, 20000)
        #a.addbaseimage_23(win7_new_ipv6, token, 20000)
        a.addbaseimage_23(win10_new, token, 20000)
        #a.addbaseimage_23(win10_new_ipv6, token, 20000)
        #a.addiso_pull_23(win7_iso, win7_iso_key, 'win7x64', iso_type_win7, token, 7200,skip_activation="False")
        #a.addbaseimage_23(winxp, token, 20000)

        
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #Automted script for BSOD issue on XP
#         headers=['sample_id','task_id','risk_score','bsod_state','core_events','rk_events']
#         with open('csvfile.csv','wb') as file:
#             csv.writer(file,delimiter=',',lineterminator='\n')
#             for x in headers:
#                 file.write(x)
#                 file.write(',')
#         with open('csvfile.csv','a') as file:
#             csv.writer(file,delimiter=',',lineterminator='\n')
#             f = a.upload_samples_dir(cas_ip, token)
#             print "Samples uploaded successfully"
#             taskid_list=[]
#             for sample_id in f:
#             #for sample_id in [11995,16059]:
#                 chakde = a.create_task(sample_id, 3, plugin, token)
#                 taskid_list.append(chakde)
#             print "Tasks created successfully for each sample"
#             #taskid_list = [10174,10175]
#             for x in taskid_list:
#                 a.wait_for_task_complete(x, 1000, token)
#                 sample_id = a.get_sample_id(x, token)
#                 risk_score = a.get_task_riskscore(x, token)
#                 bsod_state = a.check_task_resource(x, token)
#                 event_count_core = a.gettaskevents(x,'CORE', token)
#                 event_count_rk = a.gettaskevents(x,'RK', token)
#                   
#                 #print sample_id
#                 #print risk_score
#                 #print bsod_state
#                 #print event_count_core
#                 #print event_count_rk
#                 ## write result into a new csv file ####
#                 file.write('\n')
#                 file.write(str(sample_id).strip())
#                 file.write(',')
#                 file.write(str(x).strip())
#                 file.write(',')
#                 file.write(str(risk_score).strip())
#                 file.write(',')
#                 file.write(str(bsod_state).strip())
#                 file.write(',')
#                 file.write(str(event_count_core).strip())
#                 file.write(',')
#                 file.write(str(event_count_rk).strip())
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            
        
if __name__ == '__main__':
    unittest.main() 