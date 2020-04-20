import requests
import json
import time
from lxml import etree

DEBUG = False
VIEWSTATE = '/wEPDwUKLTM2OTg5MjUwNg9kFgRmDxYCHgtfIUl0ZW1Db3VudAIBFgJmD2QWAmYPFQcBMQQyMDE2ATgCMTBLRWFzeSB0ZXN057ea5LiK5a2457+S5ris6amX5bmz5Y+w5bey57aT5bu6572u5a6M5oiQ77yM5q2h6L+O6Li06LqN5L2/55So44CCATEQPHA+5aaC6aGM44CCPC9wPmQCAQ8WAh8AAgkWEmYPZBYCZg8VAyRDb3Vyc2VzL25ld190b2VpYy9zYW1wbGUuYXNweD90aWQ9MDABOxFUT0VJQ+aooeaTrOa4rOmpl2QCAQ9kFgJmDxUDJG9ubGluZV90ZXN0L2V0ZXN0L3NhbXBsZS5hc3B4P3RpZD0wMAE7GOWFqOawkeiLseaqouaooeaTrOa4rOmpl2QCAg9kFgJmDxUDDUNvdXJzZXMvdG9lZmwBOxVpQlTmiZjnpo/mqKHmk6zmuKzpqZdkAgMPZBYCZg8VAxBvbmxpbmVfdGVzdC9KTFBUATsQSkxQVOaooeaTrOa4rOmpl2QCBA9kFgJmDxUDEW9ubGluZV90ZXN0L2lvdmxzDGNvbG9yOmdyZWVuOxjoi7HmloflvbHpn7PkupLli5XoqrLnqItkAgUPZBYCZg8VAyNvbmxpbmVfdGVzdC93b3JkX2V4YW1pbmUvaW5kZXguYXNweAxjb2xvcjpncmVlbjsS5Zau5a2X5a2457+S57O757WxZAIGD2QWAmYPFQMXb25saW5lX3Rlc3QvamxwdF9jb3Vyc2UMY29sb3I6Z3JlZW47EuaXpeaWh+WtuOe/kuiqsueoi2QCBw9kFgJmDxUDEG9ubGluZV90ZXN0LzUwanAMY29sb3I6Z3JlZW47FeaXpeiqnuS6lOWNgemfs+iqsueoi2QCCA9kFgJmDxUDD2xlYXJuX21vcmUuYXNweAxjb2xvcjpncmVlbjsS5YW25LuW5a2457+S6LOH5rqQZGSx1S0XOJrB4vkGPlB3t7o6WMxeXgHdo15XaI9CihH18w=='
VIEWSTATEGENERATOR = '90059987'
EVENTVALIDATION = '/wEdAARQ6fCua7Qf37k3ap59rCnAvTa/V+SDY9mI55q1kXnays9ldyoHj2aNupFanuLi5LBMirLtENmb6ez0f81TBHESVgOaWvUDhC22tXuDDoa4fJC9V1V2db5peDTWecDXbKw='

class requestLib():
    def __init__(self):
        self.URL = 'https://easytest.ncut.edu.tw/'
        self.SESSION = requests.Session()
        self.SESSION.headers.update({
            'authority': 'easytest.ncut.edu.tw'
        })

    def __request(self, method, node='', **kwargs):
        resp = self.SESSION.request(method, self.URL + node, **kwargs)
        if DEBUG:
            try:
                print(resp)
                print(resp.text)
            except (UnicodeDecodeError, UnicodeDecodeError, UnicodeError):
                print('[WARNING] Unknow unicode error from response')
        return resp

    #------------------------------------------------------------------------------------
    # Function Zone
    #------------------------------------------------------------------------------------

    def get_cookieId(self):
        self.SESSION.headers.update({'referer': 'https://easytest.ncut.edu.tw/index.aspx'})
        resp = self.__request('get', 'index.aspx')
        cookieId = resp.cookies['ASP.NET_SessionId']
        return cookieId

    def login(self, account, password, cookieId=None):
        '''
        Active this cookieId for current login user
        '''
        self.SESSION.headers.update({'referer': 'https://easytest.ncut.edu.tw/index.aspx'})
        #self.SESSION.headers.update({'cookie': 'ASP.NET_SessionId={id}'.format(id=cookieId)})
        self.SESSION.headers.update({'content-type': 'application/x-www-form-urlencoded'})
        data = {
            '__VIEWSTATE': VIEWSTATE,
            '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': EVENTVALIDATION,
            'cust_id': account,
            'cust_pass': password,
            'send': '登入',
            'Action': 'MLogin'
        }
        resp = self.__request('post', 'index.aspx', data=data)
        html = etree.HTML(resp.text)
        checkText = html.xpath('//a/span[@class="glyphicon glyphicon-user"]/parent::a/text()[1]')
        return checkText

if __name__ == "__main__":
    lib = requestLib()
    lib.get_cookieId()
    print(lib.login('3A123456', '3A123456'))
