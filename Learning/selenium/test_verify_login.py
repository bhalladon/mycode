from commonfunctions import *

class login_test(unittest.TestCase):

    def setUp(self):
        global a
        a = selenium_framework()
        self.driver = webdriver.Chrome()
        global b
        b = self.driver
        b.get("https://"+str(ma_ip))
        b.maximize_window()
        
    def test_a(self):
        print "test1"
        a.login(b,"admin", "admin")
    
    def tearDown(self):
        b.close()       
