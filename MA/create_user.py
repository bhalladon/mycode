from common_functions import *
import json

class test_createuser(unittest.TestCase):
        
    def setUp(self):        
        global a
        a = mautilities()
        global token
        token = a.generate_token(ma_ip)
        
    
    def test_a_create_user(self):
        #f = a.upload_samples(ma_ip)
        #for x in range(12348,22348):
        #a.get_task_events(x)
        f = a.rapiget("tasks/12348/events")
        print len(f)
        #a.gettaskriskscore(12348, 22347)
        #for sample_id in range(2416,12416):
        #   a.create_task(sample_id, 1)
        #a.delete_all_samples(ma_ip)
        #a.gettaskriskscore(131, 347)