
import thread
import time

# Define a function for the thread

    def generate_token(self,ma_ip):
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

def deletesamples( threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print "%s: %s" % ( threadName, time.ctime(time.time()) )
        
# Create two threads as follows
try:
    thread.start_new_thread( print_time, ("Thread-1", 2, ) )
    thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
    print "Error: unable to start thread"

while 1:
    pass