import xmlrunner
import unittest
import json
import sampling
import requests
import os

       
class Mass_Test(unittest.TestCase):

    def test_submit_dir_test(self):                          
   
        try:            
            a = sampling
            try:
            #Submit Sample
                sample_id            = 6
                print "Sample Id: " + str(sample_id)      
        
                for x in range(1,100000):                 
                ## Create Task
                    data                 = json.loads(a.create_task(sample_id, "ivm", a.get_ivm_id("win7","x86")))
                    task_id              = data['results'][0]['tasks_task_id']
                    print "Task Id: " + str(task_id)
        
        
            except Exception, e:
                print "ERROR: %s" % e
                    
             
        except Exception, e:
            self.fail("Case Status: [Failed]%s" % e)
    
    
if __name__ == "__main__":
    runner = xmlrunner.XMLTestRunner(output='reports')
    unittest.main(testRunner=runner)
