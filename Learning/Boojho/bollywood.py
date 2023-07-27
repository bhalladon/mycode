#!/usr/bin/PYTHON

import httplib, urllib, socket

values = {}
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36','Content-type': "text/html; charset=UTF-8", 'cookie': "_huid=29df9717e8f15343a5cc3a84d456b1cc; PHPSESSID=nim2rtnac95eauhvto58k83r74; _ga=GA1.2.165297524.1469672217; bhlang=a%3A2%3A%7Bs%3A8%3A%22langabbr%22%3Bs%3A2%3A%22en%22%3Bs%3A6%3A%22langid%22%3Bs%3A1%3A%221%22%3B%7D"}
values = urllib.urlencode(values)
url = "/movies/alphalist/char/a/"
host = socket.gethostbyname("www.bollywoodhungama.com")
conn = httplib.HTTPConnection(host)
conn.request("GET", url, values, headers)
response = conn.getresponse()
data = response.read()
print data

conn.close()

