from json import loads, dumps
from pprint import PrettyPrinter
import requests
class Informatica(object):
    def __init__(self):
        self.sessionID = ""
        self.serverURL = ''
        self.heads = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.authenticated = False

    def login(self, name=None, passw=None):
        if name==None:
            name = "username"
        if passw == None:
            passw = "password"
        url="https://app.informaticaondemand.com/ma/api/v2/user/login"
        heads = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        params = {'@type': 'login',
                 'password': passw,
                  'username': name
                  }
        response = requests.post(url,headers=heads,json=params)
        if response.status_code == 200 : 
            self.authenticated = True
            self.user = response.json()
            self.heads['icSessionId'] = self.user['icSessionId']
            self.serverURL = self.user['serverUrl']
        else:
            self.user = None
            self.error = response.json()
            
    def _API_Call(self, apiURL,uid=None):
        if uid== None:
            r = requests.get(self.serverURL+apiURL,headers =self.heads)
            return r.json()
        else:
            r = requests.get(self.serverURL+apiURL+uid,headers =self.heads)
            return r.json()
    def getAgent(self, uid = None):
       agentAPI = '/api/v2/agent/'
       return self._API_Call(agentAPI,uid)
    def getSchedule(self, uid = None):
       scheduleURL = '/api/v2/schedule/'
       return self._API_Call(scheduleURL,uid)
    def getConnection(self, uid=None):
       connectionURL = '/api/v2/connection/'
       return self._API_Call(connectionURL,uid)
    def upConnection(self, uid, changes): 
       connectionURL = '/api/v2/connection/'
       r = requests.post(self.serverURL + connectionURL + uid, headers=self.heads, json=changes)
       return r.json()
    def getTask(self,uid = None):
       taskAPI = '/api/v2/mttask'
       return self._API_Call(taskAPI,uid)

def test():
    I = Informatica()
    if I.authenticated == False:
        print( I.error)
    else:
        print(I.user)
if __name__ == '__main__':
    test()
