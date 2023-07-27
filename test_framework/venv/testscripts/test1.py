from venv.__init__ import *

class test_systeminfo(unittest.TestCase):

    def setUp(self):
        global a
        a = casutilities()
        #global token
        #token = a.generate_token()


    def test_a_getsysteminfo(self):
        print("chakde")
        # values={}
#         # headers={'X-API-TOKEN': token}
#         # f = a.httpcall("GET", "/rapi/system/version_info", values, headers)['results']['mag2_version']
#         # if f.startswith("2.4"):
#         # print "chakde"
#         # elif f.startswith("2.1") or f.startswith('2.2') or f.startswith('2.3'):
#         # print "india"ney