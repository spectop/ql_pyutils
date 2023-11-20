import os
import time
import json
import requests


class BaseAPI:

    def __init__(self, host, port, token):
        self.__host = host
        self.__port = port
        self.__token = token

    def _make_request(self, method, api, params=None, data=None):
        url = f'http://{self.__host}:{self.__port}{api}'

        headers = {
            'Accept': 'application/json',
            'authorization': f'Bearer {self.__token}',
            'Content-Type': 'application/json;charset=UTF-8'
        }

        params = params or {}
        params['t'] = int(round(time.time() * 1000))

        res = requests.request(method, url, headers=headers, params=params, json=data)

        if res.status_code != 200:
            raise Exception('请求失败')
        
        return res.json()
    

class EnvAPI(BaseAPI):

    def getEnvs(self, searchText=None):
        params = {}
        if searchText:
            params['searchValue'] = str(searchText)

        return self._make_request('GET', '/api/envs', params).get('data', [])
    
    def addEnv(self, name, value, remarks):
        data = [{
            'name': name,
            'value': value,
            'remarks': remarks
        }]

        return self._make_request('POST', '/api/envs', data=data).get('code') == 200
    
    def updateEnv(self, eid, name, value, **kwargs):
        data = {
            'id': eid,
            'name': name,
            'value': value
        }
        data.update(kwargs)

        return self._make_request('PUT', '/api/envs', data=data).get('code') == 200


class SystemAPI:

    def __init__(self, host='127.0.0.1', port=5700):
        self.host = host
        self.port = port

        self.__token = None

        self.__init_token()
        self.__init_api()
    
    def __init_token(self):
        auth_file = '/ql/data/config/auth.json'
        if not os.path.exists(auth_file):
            auth_file = '/ql/config/auth.json'
        if not os.path.exists(auth_file):
            raise Exception('未找到 auth.json 文件')
        
        with open(auth_file, 'r') as f:
            auth = json.load(f)

            token = auth.get('token')
            if not token:
                raise Exception('未找到 token')
            
            self.__token = token
    
    def __init_api(self):
        self.env = EnvAPI(self.host, self.port, self.__token)

        
__all__ = ['SystemAPI']