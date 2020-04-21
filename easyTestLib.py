import requests
import json
import time
from lxml import etree
import re

DEBUG = False
VIEWSTATE = '/wEPDwUKLTM2OTg5MjUwNg9kFgRmDxYCHgtfIUl0ZW1Db3VudAIBFgJmD2QWAmYPFQcBMQQyMDE2ATgCMTBLRWFzeSB0ZXN057ea5LiK5a2457+S5ris6amX5bmz5Y+w5bey57aT5bu6572u5a6M5oiQ77yM5q2h6L+O6Li06LqN5L2/55So44CCATEQPHA+5aaC6aGM44CCPC9wPmQCAQ8WAh8AAgkWEmYPZBYCZg8VAyRDb3Vyc2VzL25ld190b2VpYy9zYW1wbGUuYXNweD90aWQ9MDABOxFUT0VJQ+aooeaTrOa4rOmpl2QCAQ9kFgJmDxUDJG9ubGluZV90ZXN0L2V0ZXN0L3NhbXBsZS5hc3B4P3RpZD0wMAE7GOWFqOawkeiLseaqouaooeaTrOa4rOmpl2QCAg9kFgJmDxUDDUNvdXJzZXMvdG9lZmwBOxVpQlTmiZjnpo/mqKHmk6zmuKzpqZdkAgMPZBYCZg8VAxBvbmxpbmVfdGVzdC9KTFBUATsQSkxQVOaooeaTrOa4rOmpl2QCBA9kFgJmDxUDEW9ubGluZV90ZXN0L2lvdmxzDGNvbG9yOmdyZWVuOxjoi7HmloflvbHpn7PkupLli5XoqrLnqItkAgUPZBYCZg8VAyNvbmxpbmVfdGVzdC93b3JkX2V4YW1pbmUvaW5kZXguYXNweAxjb2xvcjpncmVlbjsS5Zau5a2X5a2457+S57O757WxZAIGD2QWAmYPFQMXb25saW5lX3Rlc3QvamxwdF9jb3Vyc2UMY29sb3I6Z3JlZW47EuaXpeaWh+WtuOe/kuiqsueoi2QCBw9kFgJmDxUDEG9ubGluZV90ZXN0LzUwanAMY29sb3I6Z3JlZW47FeaXpeiqnuS6lOWNgemfs+iqsueoi2QCCA9kFgJmDxUDD2xlYXJuX21vcmUuYXNweAxjb2xvcjpncmVlbjsS5YW25LuW5a2457+S6LOH5rqQZGSx1S0XOJrB4vkGPlB3t7o6WMxeXgHdo15XaI9CihH18w=='
VIEWSTATEGENERATOR = '90059987'
EVENTVALIDATION = '/wEdAARQ6fCua7Qf37k3ap59rCnAvTa/V+SDY9mI55q1kXnays9ldyoHj2aNupFanuLi5LBMirLtENmb6ez0f81TBHESVgOaWvUDhC22tXuDDoa4fJC9V1V2db5peDTWecDXbKw='
onlineTestEndPoint = 'online_test/etest/'
TID = '81' # from 余詩芸-1082W190

# to get simulation page url
element_SimulationPageBtn = '//*[text()="模 擬 正 式 "]//parent::div//parent::div[@class="service clearfix btn"][@onclick]'
# to get tests qlevel when you need do this
element_StartTestBtns = '//a[@class="btn btn-block btn-info"][@href]'

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
    # Requests Zone
    #------------------------------------------------------------------------------------

    def get_cookieId(self):
        '''
        Enter the index page and get new cookie
        '''
        resp = self.__request('get', 'index.aspx')
        cookieId = resp.cookies['ASP.NET_SessionId']
        return cookieId

    def login(self, account, password, cookieId=None):
        '''
        Active this cookieId for current login user
        '''
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
        return checkText[0]

    def get_simulationPage(self, tid):
        '''
        Get simulation page html obj by tid(teacher id)
        '''
        params = {
            "tid": tid
        }
        resp = self.__request('get', onlineTestEndPoint + 'elective_simulation.aspx', params=params)
        html = etree.HTML(resp.text)
        return html

    def get_testsOverviewPage(self, pageName):
        '''
        Get tests overview page. You can find all qlevel of test on this page
        '''
        resp = self.__request('get', onlineTestEndPoint + pageName)
        html = etree.HTML(resp.text)
        return html


    #------------------------------------------------------------------------------------
    # Function Zone
    #------------------------------------------------------------------------------------


if __name__ == "__main__":
    client = requestLib()
    client.get_cookieId()
    account = input('Account:')
    password = input('Password:')
    loginCheck = client.login(account, password)
    if loginCheck == '登入':
        print('login FAIL as ' + loginCheck)
        exit()
    print('login PASS as ' + loginCheck)

    ## simulationPage
    page = client.get_simulationPage(TID)
    text = page.xpath(element_SimulationPageBtn + '/@onclick')[0]
    testsOverviewPageName = re.findall("location.href='(.*?)'", text)[0]
    ## testsOverviewPage
    page = client.get_testsOverviewPage(testsOverviewPageName)
    elements = page.xpath(element_StartTestBtns)
    qlevelList = list()
    for element in elements:
        text = element.xpath('@href')[0]
        qlevel = re.findall("javascript:set_level\((.*?)\);", text)[0]
        qlevelList.append(qlevel)
    print(qlevelList)

    # TO DO
    # for in qlevelList.
    # start test for qlevel
    # https://easytest.ncut.edu.tw/online_test/etest/elective_gept_exam.aspx?GeptSec=start&qlevel=1001&TestType=3
    # skip/continue all elective_gept_exam.aspx to go to answer page. And check elective_gept_exam.aspx scenario
    # get all question-answer key value dict from answer page
