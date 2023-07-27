import requests,json,paramiko,time,os,unittest,threading
import requests.packages.urllib3
from unittest.case import SkipTest
#cas_ip=os.getenv("MAG2_RAPI")
#cas_ip_no_port=str(os.getenv("MAG2_RAPI")).strip(":8082")
cas_ip="10.199.107.17:8082"
cas_adminuser="admin"
cas_adminpass="admin123"

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
requests.packages.urllib3.has_memoryview = False

class casutilities():

    def setUp(self):
        global a
        a = casutilities()
        global token
        token = a.generate_token()

    
    def httpcall(self, call_method, rapicall, values, headers):
        url = str("https://") +str(cas_ip)+ str(rapicall)
        call_method = call_method.lower()
        if call_method ==  "get":
            r = requests.get(url, data=values, headers=headers, verify=False)
        if call_method == "post":
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
                return r.text
                return r.status_code
        
            
    def generate_token(self):
        a = casutilities()
        values = {"username":cas_adminuser, "password":cas_adminpass}
        headers = {"User-Agent":"python"}
        token = a.httpcall("POST", "/rapi/auth/session", values, headers)['results']['session_token_string']
        return token
    
    def get_sample_list(self,cas_ip, token):
        try:
            sampleidfile = os.path.join(os.getcwd(), "sampleid.txt")
            os.remove(sampleidfile)
        except:
            pass
        fp = os.path.join(os.getcwd(),"../samples")
        sample_list_new = []
        for root, directories, filenames in os.walk(fp): 
            for filename in filenames: 
                file2 = os.path.join(root,filename)
                sample_list = sample_list_new.append(file2)

        return sample_list_new
        #return sampleid
    
    def upload_samples_dir(self,cas_ip,sample_file,token):
        a = casutilities()
        url = "https://"+ cas_ip +  "/rapi/samples/basic"
        samples = {'file': open(sample_file, 'rb')}
        values = {'owner': 'admin'}
        headers = {'X-API-TOKEN': token}
        r = requests.post(url, files=samples, data=values, headers=headers, verify=False)
        sample_response=r.text
        if r.status_code in [200,201]:       
            data = json.loads(sample_response)
            sample_id = data['results'][0]['samples_sample_id']
            print "Sample ID is: " + str(sample_id)
            sampleid.append(sample_id)
        else:
            print r.status_code
            print sample_response
            print "Unable to upload sample"
    
    def create_task(self,sample_id, profileid, plugin, token):
        a = casutilities()
        if plugin == "":
            #,'tp_IVM.SMART_DETONATION':1
            values = {'sample_id': sample_id, 'env': 'ivm', 'primary_resource_name':'', 'tp_IVM.FIREWALL':3, 'tp_DEF.log_task':1,'vmp_id':profileid,'tp_DEF.ivm_plugin':'_SYSTEM_:', 'tp_IVM.GET_DROPPED_FILES':1}
        else:
            values = {'sample_id': sample_id, 'env': 'ivm', 'primary_resource_name':'_SYSTEM_:'+str(plugin), 'tp_DEF.log_task':1,'tp_IVM.FIREWALL':3, 'vmp_id':profileid, 'tp_IVM.GET_DROPPED_FILES':1}
        headers = {'X-API-TOKEN': token}
        taskid = a.httpcall("post", "/rapi/tasks", values, headers)['results'][0]['tasks_task_id']
        print "Task id is: " +str(taskid)
        #return taskid
        
class test_samples_upload(unittest.TestCase):
    def setUp(self):
        global a
        a = casutilities()
        global token
        token = a.generate_token()
        global sampleid
        sampleid=[]
        
    def test_get_sample_list(self):
        f = a.get_sample_list(cas_ip, token)
        threads=list()
        for x in f:
            x = threading.Thread(target=a.upload_samples_dir, args=(cas_ip,x,token, ))
            threads.append(x)
            x.start()
            if len(threads) % 100 == 0:
                while x.isAlive():
                    pass
        for x in threads:
            x.join(timeout=12)
        print "All samples uploaded successfully."
        print sampleid 

        for x in sampleid:
            x = threading.Thread(target=a.create_task(x, 297, "ghost_user.py", token, ))
            threads.append(x)
            x.start()
            if len(threads) % 100 == 0:
                while x.isAlive():
                    pass
        for x in threads:
            x.join(timeout=12)
        print "All tasks created successfully."


if __name__ == '__main__':
    unittest.main() 
