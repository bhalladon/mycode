
import httplib

conn = httplib.HTTPSConnection("192.168.3.39")
conn.request("GET", "/index.html")
r1 = conn.getresponse()
print r1.status, r1.reason
#200 OK
data1 = r1.read()
conn.request("GET", "/rapi/system/version_info")
r2 = conn.getresponse()
print r2.status, r2.reason
#404 Not Found
data2 = r2.read()
conn.close()
