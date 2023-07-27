import unittest,requests,json,threading,os
#import requests.packages.urllib3

cas_ip ="10.199.107.17:8082"
#cas_ip=os.getenv("MAG2HOST")
cas_adminuser="admin"
#cas_adminuser=os.getenv("MAG2_ADMINUSER")
cas_adminpass="admin123"
#cas_adminpass=os.getenv("MAG2_ADMINPASS")

# try:
#     requests.packages.urllib3.disable_warnings()
# except:
#     pass
# requests.packages.urllib3.has_memoryview = False

class casutilities():
        
    def httpcall(self, call_method, rapicall, values, headers):
        url = "https://" +str(cas_ip)+ str(rapicall)
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
                print r.text
                return r.text
                return r.status_code
        
            
    def generate_token(self):
        a = casutilities()
        values = {"username":cas_adminuser, "password":cas_adminpass}
        headers = {"User-Agent":"python"}
        token = a.httpcall("POST", "/rapi/auth/session", values, headers)['results']['session_token_string']
        return token   

    def delete_sample(self,sample_id):
        a = casutilities()
        values = {}
        headers = {"User-Agent":"python", 'X-API-TOKEN':token}
        delsample = a.httpcall("DELETE", "/rapi/samples/"+str(sample_id), values, headers)
        if "Not Found" in delsample:
            pass
        else:
            print "Sample with sample ID:"+ str(sample_id) + " deleted successfully"
    
    def delete_all_samples(self,cas_ip, token):
        a = casutilities()
        values = {}
        headers = {"User-Agent":"python", 'X-API-TOKEN':token}
#         sample_id = []
        status = True
        while True:
            f = a.httpcall("GET", "/rapi/samples?limit=1000", values, headers)['results_count']
            if f == 0:
                print "No samples exist"
                status = False
                break
            
            print "Total number of samples found: " + str(f)
            g = a.httpcall("GET", "/rapi/samples?limit="+str(f),values, headers)
            sample_id = []
            try:
                for x in range(f):
                    sampleid = g['results'][x]['samples_sample_id']
                    sample_id.append(sampleid)
            except IndexError:
                pass     
            print sample_id
            threads=list()
            for x in sample_id:
                x = threading.Thread(target=a.delete_sample, args=(x, ))
                threads.append(x)
                x.start()
                if len(threads) % 100 == 0:
                    while x.isAlive():
                        pass
            for x in threads:
                x.join(timeout=20)
            print "All samples deleted successfully"
    
class test_systeminfo(unittest.TestCase):

    def setUp(self):
        global a
        a = casutilities()
        global token
        token = a.generate_token()
        print token
    
    def test_a_delete(self):
        a.delete_all_samples(cas_ip, token)
    


if __name__ == '__main__':
    unittest.main() 
