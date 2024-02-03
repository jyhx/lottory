import logging

from oppo_lottery.model import Person

# 初始化日志
logger = logging.getLogger('log')

mpId2Person = {}
mpFormatName2Id = {}
iCurLotteryIndex = 0


def getCurData():
    return {'mpId2Person': {key: value.jsonformat() for key, value in mpId2Person.items()}, 'mpFormatName2Id': mpFormatName2Id,
            'iCurLotteryIndex': iCurLotteryIndex}


def loadDataFromFile(strFile):
    with open(strFile, 'r', encoding='utf-8') as f:
        loadDataFromStr(f.read(), True)


def loadDataFromStr(strData, has_head=False):
    lines = strData.split('\n')
    for i in range(1 if has_head else 0, len(lines)):
        if len(lines[i]) <= 0:
            continue
        info = lines[i].split(',')
        index = int(info[0])
        name = info[1]
        seat1 = int(info[2]) if len(info) > 2 else 0
        seat2 = int(info[3]) if len(info) > 3 else 0
        auth = int(info[4]) if len(info) > 4 else 0
        check = int(info[5]) if len(info) > 5 else 0
        person = Person(index, name, seat1, seat2, auth, check)
        if index not in mpId2Person:
            mpId2Person[index] = person
        mpFormatName2Id[makeNameSafe(name)] = index


def resetByStr(strData):
    global mpId2Person, mpFormatName2Id, iCurLotteryIndex
    mpId2PersonTmp = mpId2Person
    mpFormatName2IdTmp = mpFormatName2Id
    iCurLotteryIndexTmp = iCurLotteryIndex
    try:
        mpId2Person = {}
        mpFormatName2Id = {}
        iCurLotteryIndex = 0
        loadDataFromStr(strData, False)
    except Exception as e:
        mpId2Person = mpId2PersonTmp
        mpFormatName2Id = mpFormatName2IdTmp
        iCurLotteryIndex = iCurLotteryIndexTmp
        print(e)


def makeNameSafe(strName):
    return ''.join(strName.split(' ')).lower()


def queryIdByName(strName):
    strName = makeNameSafe(strName)
    return mpFormatName2Id[strName] if strName in mpFormatName2Id else 0


def getPersonById(iId):
    return mpId2Person[iId] if iId in mpId2Person else None


def getAllWinner():
    return [p for p in mpId2Person.values() if len(p.reward) > 0]


def getAllPersonCanLottery(bRepeat):
    # return [p for p in mpId2Person.values() if p.auth > 0 and p.check > 0]
    if bRepeat:
        return [p for p in mpId2Person.values() if p.auth > 0 and p.check > 0]
    else:
        return [p for p in mpId2Person.values() if p.auth > 0 and p.check > 0 and len(p.reward) == 0]
