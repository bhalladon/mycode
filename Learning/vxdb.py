import requests

headers = {}
r = requests.get("https://vxdb.io/")
print r.status_code
response = r.text

