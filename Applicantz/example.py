import requests
import json

f = requests.head("https://www.google.com")
if f.status_code == 200:
    h = f.headers
    s1 = json.dumps(dict(h))
    d1 = json.loads(s1)
    for keys in d1:
        print(keys)
else:
    print(f.status_code)


