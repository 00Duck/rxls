import configparser
import sys
import requests
import json

class ServiceNowConnector:
    def __init__(self, env):
        self.session = requests.Session()
        self.endpoint = ''
        self.user = ''
        self.verb = ''
        self.env = env
        self.sn_url = f'https://{env}.service-now.com'
        self.headers = {'Content-Type': 'application/json'}
        self.loadConnectionDetails()
        self.testConnection()

    def testConnection(self):
        try:
            resp = self.session.post(url=f'{self.sn_url}/api/now/table/sys_user?sysparm_query=user_name={self.user}', headers=self.headers)
            if resp.status_code != 201:
                print(f"Failed connection test to {self.env}. Check connection.conf to ensure the credentials specified are correct.")
                sys.exit()
            else:
                print(f"Successful connection test to {self.env}.")
        except Exception as err:
            print(f'Error testing error: {err}')
            sys.exit()

    def loadConnectionDetails(self):
        try:
            conf = configparser.ConfigParser()
            conf.read("connection.conf")
            self.endpoint = conf.get(self.env, option="endpoint")
            self.user = conf.get(section=self.env, option="user")
            self.session.auth = (self.user,
                                 conf.get(section=self.env, option="pass"))
            try:
                self.verb = conf.get(section=self.env, option="verb").upper()
            except:
                print("Setting verb to POST as none was specified.")
                self.verb = 'POST'
        except Exception as err:
            print(f'Error loading connection details: {err}')
            sys.exit()

    def call(self, inputData: dict) -> requests.Response:
        try:
            resp = ''
            url = f'{self.sn_url}{self.endpoint}'
            data = json.dumps(inputData)
            if self.verb in ["POST", "GET", "PUT", "PATCH", "DELETE"]:
                resp = self.session.request(self.verb, url=url, data=data, headers=self.headers)
            else:
                print(f"\nHTTP verb not recognized: {self.verb}")
                sys.exit()
            return resp
        except Exception as err:
            print(f"\nREST error: {err}")
            sys.exit()
