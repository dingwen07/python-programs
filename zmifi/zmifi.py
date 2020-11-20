from typing import Any
import xml.etree.ElementTree as ET
import requests
import time
import hashlib
import math
import sys
import random
import codecs


hex_md5 = lambda string : hashlib.md5(string.encode()).hexdigest()
current_milli_time = lambda: int(round(time.time() * 1000))
cmt = current_milli_time

def get_val(string: str) -> str:
    string = string.split('=')[1]
    index1 = string.index('"')
    index2 = string.index('"', index1 + 1)
    return string[index1 + 1:index2]


class zmifi(object):
    def __init__(self, host: str, username: str, password: str, login: bool=True) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login(login)
    
    def login(self, login: bool=True) -> bool:
        login_url = 'http://{}/login.cgi?{}'.format(self.host, '{}')
        try:
            login_param_response = self.session.get(login_url.format('_={}'.format(str(cmt()))))
        except (ConnectionError, requests.exceptions.ConnectionError) as e:
            exception_message = 'Unable to connect to the specified host'
            raise ConnectionError(exception_message).with_traceback(sys.exc_info()[2])
        login_param = login_param_response.headers['WWW-Authenticate']
        login_param_array = login_param.split(' ')
        self.authrealm = get_val(login_param_array[1])
        self.nonce = get_val(login_param_array[2])
        self.auth_qop = get_val(login_param_array[3])
        if not login:
            return False
        HA1 = hex_md5(self.username+ ":" + self.authrealm + ":" + self.password)
        HA2 = hex_md5('GET' + ':' + '/cgi/protected.cgi')
        rand = math.floor(random.random()*100001)
        date = cmt()
        salt = str(rand) + str(date)
        auth_cnonce = hex_md5(salt)[0:16]
        digest_res = hex_md5(HA1 + ':' + self.nonce + ':' + '00000001' + ':' + auth_cnonce + ':' + self.auth_qop + ':' + HA2)
        request_url =  login_url.format('Action=Digest&username=' + self.username + '&realm=' + self.authrealm + '&nonce=' + self.nonce + '&response=' + digest_res + '&qop=' + self.auth_qop + '&cnonce=' +auth_cnonce + '&temp=marvell&_=' + str(cmt()))
        headers = {}
        authorization = self._get_auth_header('GET')
        headers['Authorization'] = authorization
        '''
        headers['Expires'] = '-1'
        headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        headers['Pragma'] = 'no-cache'
        '''
        try:
            login_response = self.session.get(request_url, headers=headers)
            login_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            exception_message = ''
            if e.response.status_code == 500:
                exception_message = 'Login failed, probably because the username or password is incorrect'
            raise ValueError(exception_message) from e
            # raise ValueError(exception_message).with_traceback(sys.exc_info()[2]) from e
            # e.args = (exception_message, *e.args)
            # raise
        if login_response.status_code == 200:
            return True
        elif login_response.status_code == 500:
            raise requests.exceptions.HTTPError
        else:
            raise requests.exceptions.HTTPError

    def reboot(self) -> None:
        universal_url = 'http://{}/xml_action.cgi?method=get&module=duster&file=reset'
        self._http_get(universal_url)

    def poweroff(self) -> None:
        universal_url = 'http://{}/xml_action.cgi?method=get&module=duster&file=poweroff'
        self._http_get(universal_url)
    
    def device_data(self) -> dict:
        universal_url = 'http://{}/xml_action.cgi?method=get&module=duster&file=device_management'
        response = self._http_get(universal_url)
        root = ET.fromstring(response.text)
        known_devices_list = []
        for item in root.iterfind('device_management/known_devices_list/Item'):
            device = item.attrib
            for tag in item:
                device[tag.tag] = tag.text
            known_devices_list.append(device)
        client_list = []
        for item in root.iterfind('device_management/client_list/Item'):
            client = item.attrib
            for tag in item:
                client[tag.tag] = tag.text
            client_list.append(client)
        device_data = {
            'known_devices_list': known_devices_list,
            'client_list': client_list
        }
        return device_data
    
    def wps_push(self) -> None:
        universal_url = 'http://{}/xml_action.cgi?method=set&module=duster&file=uapxb_wlan_security_settings'
        headers = {}
        headers['Connection'] = 'keep-alive'
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        data = '''<?xml version="1.0" encoding="US-ASCII"?> <RGW><wlan_security><WPS><connect_method>1</connect_method></WPS></wlan_security></RGW>'''
        self._http_post(universal_url, data, headers)

    def block(self, mac_addr: str) -> None:
        universal_url = 'http://{}/xml_action.cgi?method=set&module=duster&file=device_management'
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        data = '''<?xml version=`"1.0`" encoding=`"US-ASCII`"?> <RGW><device_management><device_control><action>2</action><mac>{}</mac></device_control></device_management></RGW>'''
        data = data.format(mac_addr)
        self._http_post(universal_url, data, headers)

    def ublock(self, mac_addr: str) -> None:
        universal_url = 'http://{}/xml_action.cgi?method=set&module=duster&file=device_management'
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        data = '''<?xml version=`"1.0`" encoding=`"US-ASCII`"?> <RGW><device_management><device_control><action>3</action><mac>{}</mac></device_control></device_management></RGW>'''
        data = data.format(mac_addr)
        self._http_post(universal_url, data, headers)

    def _http_get(self, universal_url: str, headers: dict={}) -> requests.models.Response:
        request_url = universal_url.format(self.host)
        authorization = self._get_auth_header('GET')
        headers['Authorization'] = authorization
        try:
            response = self.session.get(request_url, headers=headers)
        except (ConnectionError, requests.exceptions.ConnectionError) as e:
            exception_message = 'Unable to connect to the specified host'
            raise ConnectionError(exception_message).with_traceback(sys.exc_info()[2])
        return response
    
    def _http_post(self, universal_url: str, data: Any, headers: dict={}) -> requests.models.Response:
        request_url = universal_url.format(self.host)
        authorization = self._get_auth_header('POST')
        headers['Authorization'] = authorization
        try:
            response = self.session.post(request_url, data, headers=headers)
        except (ConnectionError, requests.exceptions.ConnectionError) as e:
            exception_message = 'Unable to connect to the specified host'
            raise ConnectionError(exception_message).with_traceback(sys.exc_info()[2])
        return response

    def _get_auth_header(self, request_type: str) -> str:
        HA1 = hex_md5(self.username+ ':' + self.authrealm + ':' + self.password)
        HA2 = hex_md5(request_type + ':' + '/cgi/xml_action.cgi')
        rand = math.floor(random.random()*100001)
        date = cmt()
        salt = str(rand) + str(date)
        auth_cnonce_f = hex_md5(salt)[0:16]
        temp = "0000000000" + '1'
        authcount = temp[len(temp)-8:]
        digest_res = hex_md5(HA1 + ':' + self.nonce + ':' + authcount + ':' + auth_cnonce_f  + ':' + self.auth_qop + ':' + HA2)
        str_auth_header = 'Digest ' + 'username="' + self.username + '", realm="' + self.authrealm + '", nonce="' + self.nonce + '", uri="' + "/cgi/xml_action.cgi" + '", response="' + digest_res + '", qop=' + self.auth_qop + ', nc=' + authcount + ', cnonce="' + auth_cnonce_f  + '"' 
        return str_auth_header

if __name__ == "__main__":
    l = zmifi('192.168.21.1', 'admin', 'password')
    import json
    # print(json.dumps(l.device_data()))
    # l.poweroff()
    # l.ublock('mac_addr')
    l.wps_push()
