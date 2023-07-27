#from tqdm import tqdm
import urllib2,time
import requests.packages.urllib3
from time import sleep
import os
import re
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import httplib, urllib
from requests.api import request
import ConfigParser
requests.packages.urllib3.disable_warnings()
import ssl
from httplib import HTTPConnection, HTTPS_PORT
import socket


ma_ip = "10.199.110.71:8082"
adminuser = "admin"
adminpassword = "admin123"

xapitoken = ""
ma_token= ""
token = ""
api_version = ""
CASMA = True

class CASRAPI(object):
    def __init__(self, username=adminuser, password=adminpassword):
        self.username = username
        self.password = password
        self.host = str(ma_ip)
        self.service_name = 'http://localhost:8447/avenger/j_spring_cas_security_check'
        self._cookies = None
        self.tgt_url = None


    def __request(self, method, endpoint, **kwargs):
        if not 'verify' in kwargs:
            kwargs['verify'] = False
 
        if self._cookies is not None:
            kwargs['cookies'] = self._cookies
 
            tmp = {}
            if 'params' in kwargs:
                tmp.update(kwargs['params'])
            tmp['_dc'] = str(int(time.time()))
            kwargs['params'] = tmp
 
            tmp = {}
            if 'headers' in kwargs:
                tmp.update(kwargs['headers'])
            tmp['accept'] = 'application/json'
            kwargs['headers'] = tmp
 
        if re.match('https?://', endpoint):
            url = endpoint
        else:
            url = 'https://{}/{}'.format(self.host, endpoint.lstrip('/'))
 
        r = getattr(requests, method)(url, **kwargs)
        if 'set-cookie' in r.headers:
            self._cookies = r.cookies
        return r
 
# 
    def _request(self, method, endpoint, **kwargs):
        if self._cookies is None:
            self.service_ticket = self.get_ticket(self.service_name)
 
            self._cookies = dict(
                JSESSIONID='EDA135BB06545A5081B6174F84C1948C'  # ToDo: Use random?
            )
 
            # Call REST service with ST to retrieve cookie
            params = dict(ticket=self.service_ticket)
            r = self.__request('get', '/avenger/j_spring_cas_security_check', params=params, allow_redirects=False)
            r.raise_for_status()
 
        return self.__request(method, endpoint, **kwargs)
# 
# 
    def get(self, endpoint, **kwargs):
        return self._request('get', endpoint, **kwargs)
 
 
    def put(self, endpoint, **kwargs):
        return self._request('put', endpoint, **kwargs)
 
 
    def put_json(self, endpoint, data, **kwargs):
        headers = {}
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs = {k: v for k, v in kwargs.items() if k != 'headers'}
        headers['Content-Type'] = 'application/json'
        return self._request('put', endpoint, data=json.dumps(data), headers=headers, **kwargs)
 
 
    def post(self, endpoint, **kwargs):
        return self._request('post', endpoint, **kwargs)
 
 
    def post_json(self, endpoint, data, **kwargs):
        headers = {}
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs = {k: v for k, v in kwargs.items() if k != 'headers'}
        headers['Content-Type'] = 'application/json'
        return self._request('post', endpoint, data=json.dumps(data), headers=headers, **kwargs)
 
 
    def delete(self, endpoint, **kwargs):
        return self._request('delete', endpoint, **kwargs)
 
 
    def get_ticket(self, service):
        # Authenticate and get TGT (Ticket Granting Ticket)
        if self.tgt_url is None:
            r = self.__request('post', '/cas/v1/tickets', data=dict(username=self.username, password=self.password))
            if not r.ok:
                print '*** START OF ERROR OUTPUT ***'
                print r.text
                print '*** END OF ERROR OUTPUT ***'
            r.raise_for_status()
            self.tgt_url = r.headers['location']
 
        # Use TGT to get a ST (Service Ticket)
        r = self.__request('post', self.tgt_url, data=dict(service=service))
        r.raise_for_status()
        service_ticket = r.text.strip()
        if not service_ticket.startswith('ST-'):
            raise Exception('Unknown response: {}'.format(service_ticket))
 
        return service_ticket
 
def raw_request(method, endpoint, **kwargs):
    func = getattr(requests, method)
 
    for i in range(3):
        try:
            return func(endpoint, proxies=None, **kwargs)
        except Exception as e:
            if i < 2 and 'No route to host' in str(e):
                print '*** ERROR: %s (trying again in 10 seconds)' % e
                time.sleep(10)
                continue
            raise
    return None  # Impossible
     

def cas_token():

    cas = CASRAPI(adminuser, adminpassword)
    service_ticket = cas.get_ticket('urn:malware-analysis')
    response = raw_request('post', 'https://' + ma_ip + '/rapi/auth/cas',
                                 data=dict(ticket=service_ticket),
                                 verify=False)
    token = response.json()['results']['session_token_string']
    return token

def upload_pattern(sample_name):
    #print "Submitting Sample: " + sample_name
    app_url = "https://" + str(ma_ip)
    global api_version
    try:   
            fp = os.path.join(os.getcwd(),sample_name)
            #### UPLOAD FILE
            url = app_url +  "/rapi/system/updates"
            if (api_version != ""):
                url = app_url +  "/rapi/v"+str(api_version)+"/system/updates"
            #files = {'file': open(fp, 'rb')}
            files = open(fp,'rb').read()
            
            if(CASMA):
                values = {'owner': 'admin','x-api-token': xapitoken}
                r = requests.post(url, data=files, verify=False,headers = {'x-api-token': xapitoken})
            else:
                values = {'owner': 'admin','token' : ma_token()}
                r = requests.post(url, files=files, data=values, verify=False)       
            sample_response=r.text  # JSON RESPONSE FOR THE SAMPLE
            #data = json.loads(sample_response)
            #print "Sample Id:" + str(sample_uid) 
    except Exception, e:
            print("Error: %s" % e)

    return sample_response

def install_pattern(md5sum):
    #print "Submitting Sample: " + sample_name
    app_url = "https://" + str(ma_ip)
    global api_version
    try:   
            #fp = os.path.join(os.getcwd(),sample_name)
            #### UPLOAD FILE
            url = app_url +  "/rapi/system/updates/install"
            if (api_version != ""):
                url = app_url +  "/rapi/v"+str(api_version)+"/system/updates/install"
            #files = {'file': open(fp, 'rb')}
            #files = open(fp,'rb').read()
            
            if(CASMA):
                values = {'md5': md5sum,'x-api-token': xapitoken}
                r = requests.post(url, data=values, verify=False,headers = {'x-api-token': xapitoken})       
            sample_response=r.text  # JSON RESPONSE FOR THE SAMPLE
            #data = json.loads(sample_response)
            #print "Sample Id:" + str(sample_uid) 
    except Exception, e:
            print("Error: %s" % e)

    return sample_response
    
def check_nse_version():
    app_url = "https://" + str(ma_ip)
    global api_version
    try:   
            #fp = os.path.join(os.getcwd(),sample_name)
            #### UPLOAD FILE
            url = app_url +  "/rapi/system/version_info"
            if(CASMA):
                values = {'x-api-token': xapitoken}
                r = requests.get(url, data=values, verify=False,headers = {'x-api-token': xapitoken})       
            sample_response=r.text
    except Exception, e:
            print("Error: %s" % e)
    return sample_response


xapitoken = ""
xapitoken = cas_token()
#print xapitoken
print upload_pattern("1258.ca.def.gpg")
#print install_pattern("1387f9d6ede6c8061cb7eef117c5af47")
#print check_nse_version()
