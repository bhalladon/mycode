from common_functions import *
import threading

def generate_token(self,ma_ip):
    values = {'username': 'admin', 'password': 'admin'}
    headers = {'User-Agent': 'python','Content-type': "application/x-www-form-urlencoded"}
    values = urllib.urlencode(values)
    conn = httplib.HTTPSConnection(ma_ip + ":443")
    conn.request("POST", "/rapi/auth/session", values, headers)
    response = conn.getresponse()
    data = response.read()
    fdata =json.loads(data)
    global token
    token = fdata['results']['session_token_string']
    print "Generated token is: " + token
    conn.close()


for ty in range(1,10):
    class myThread1 (threading.Thread):
        def __init__(self, threadID, name):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
        def run(self):
            #print "Starting " + self.name
            deletesample1(6585580, 2097662)
            #print "Exiting " + self.name

    def deletesample1(sample_id_start, sample_id_end ):
        sample_id_end = sample_id_end + 1
        conn = httplib.HTTPSConnection(ma_ip)
        for sample_id in range(sample_id_start, sample_id_end):
            conn.request("DELETE", "/rapi/samples/"+str(sample_id)+"?token="+token)
            response =conn.getresponse()
            data = response.read()
            print data
            conn.close()
        
thread1 = myThread1(1, "Execution -1")
thread1.start()