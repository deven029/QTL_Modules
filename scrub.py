import datetime
from flask import Flask,request
import xml.etree.ElementTree as ET
from pymongo import MongoClient
node =Flask(__name__)

@node.route('/', methods=['POST'])
def getData():
    global fromEntityGlobal
    global toUserGlobal
    global date
    date = datetime.datetime.now()
    xmlDict = request.data
    ETdata = ET.fromstring(xmlDict)
    fromEntity = ETdata.findall('APARTY')[0].text
    toUser = ETdata.findall('BPARTY')[0].text
    fromEntityGlobal = fromEntity
    toUserGlobal = toUser
    _finalStatus = getHeader()
    if(_finalStatus=='REL'):
        ETdata.findall('TYPE')[0].text = 'REL'
        return ET.tostring(ETdata, method='xml')
    else:
        ETdata.findall('TYPE')[0].text = 'CUE'
        return ET.tostring(ETdata, method='xml')


def getHeader():
    global entityRegID
    global db
    client = MongoClient('localhost', 27017)
    db = client['telecom']
    headers = db['headers']
    col = headers.find_one({'headerName':fromEntityGlobal})
    headerType = col['headerType']
    headerStatus = col['status']
    entityRegID = col['regId']
    if headerStatus== 1:
        if(headerType=='s'):
            _isUserConsent = getUserConsent(toUserGlobal,fromEntityGlobal)
            if _isUserConsent:
                return 'CUE'
            else:
                return 'REL'
        elif(headerType =='p'):
            _isuserPreference = getUserPreference(toUserGlobal)
            if _isuserPreference:
                return 'CUE'
            else:
                return 'REL'
        elif(headerType == 't'):
            return 'CUE'
    else:
        return 'REL'

def getUserConsent(toUser,fromEntity):

    consents = db['consents']
    consentValue = consents.find_one({'headerName':fromEntity,'subNo':toUser})
    if consentValue:
        status = consentValue['status']
        if status == '1':
            return True
        else:
            return False
    else:
        return False

def getUserPreference(toUser):

    preference = db['preference']
    preference_data = preference.find_one({'phone':toUser})
    blocked_category = preference_data['category']
    entity = db['entities']
    getentityType = entity.find_one({'regId':entityRegID})
    entitytype = getentityType['category']
    communicationMode = preference_data['communicationMode']

    # preference Check Block
    _Usertime_band = preference_data['dayTimeBand']
    _UserdayType = preference_data['dayType']
    liveDayCode,liveTimeCode = get_day_time_code()

    if('11' in communicationMode):
        return False
    elif ((liveTimeCode in _Usertime_band ) or (liveDayCode in _UserdayType)):
        return False
    elif(entitytype in blocked_category):
        return False
    else:
        return True

def get_day_time_code():
    global date
    date = datetime.datetime.now()
    day = datetime.date.today().strftime("%w")
    hour = date.hour
    dayCode = int(day) + 30
    timeCode = getTimeStatusCode(int(hour))
    return dayCode, timeCode

def getTimeStatusCode(time) :
    if (time>=0 and time<6) :
        return 21
    elif (time>=6 and time<8) :
        return 22
    elif (time>=8 and time<10) :
        return 23
    elif(time>=10 and time<12) :
        return 24
    elif (time>=12 and time<14) :
        return 25
    elif (time>=14 and time<16) :
        return 26
    elif (time>=16 and time<18) :
        return 27
    elif (time>=18 and time<21) :
        return 28
    elif (time>=21 and time<=24) :
        return 29

node.run(host= '172.17.208.98', port=9191)