import hashlib
import requests
import json
# не было инклюда
import datetime
from dateutil.parser import parse


# Получение скорингового балла
def get_score(parsers_data):
    XScore = 0
    YScore = 0

    if parsers_data['ScoristaParserModule']['PassportOrigin']:
        XScore += 100

    if parsers_data['ScoristaParserModule']['LicenseOrigin']:
        XScore += 100

    if not parsers_data['ScoristaParserModule']['RiskRegion']:
        XScore += 100

    if not parsers_data['ScoristaParserModule']['RiskRegion2']:
        XScore += 100

    '''
        Вообще говоря, больше 10 работ - не то же самое, что руководитель более 10 организаций
        Но с руководителем сложно - число повторов "Генеральный директор" считать? Тоже не очень.
        '''

    if not parsers_data['ScoristaParserModule']['JobsNum'] > 10:
        XScore += 100

    latePaymentInfo = parsers_data['ScoristaParserModule']['LatePaymentInfo']
    nDelays = 0

    for pm in latePaymentInfo:
        try:
            tmp = datetime.strptime(pm[0], '%d.%m.%Y').date()
            if tmp + relativedelta(years=+2) > datetime.now().date():
                if pm[1].find("есть") > -1 or pm[1].find("были") > -1:
                    nDelays += 1
        except:
            continue

    if nDelays == 0:
        XScore += 100

    '''
        Считаем, что была работа, если работал в этом году или прошлом
        '''

    jobs = parsers_data['ScoristaParserModule']['Jobs']
    jobsRecent = False
    # тут было jb[2] а надо jb[2][0] + int
    for jb in jobs:
        job_year = 0
        try:
            job_year = int(jb[2][0])
        except:
            continue
        if job_year > (datetime.date.today().year - 2):
            jobsRecent = True

    if jobsRecent:
        XScore += 100

        if parsers_data['ScoristaParserModule']['currentDebts'] > 50000:
            YScore += 100 - 100 * (parsers_data['ScoristaParserModule']['TotalDebt'] - 50000) / 100000
        else:
            YScore += 100

    bd = parsers_data['ScoristaParserModule']['BirthDate']
    clientAge = datetime.date.today().year - parse(bd).year
    if clientAge < 25:
        YScore += 100 * (clientAge - 18) / 7
    else:
        YScore += 100

    YScore += 100 - 100 * (parsers_data['ScoristaParserModule']['RoadPoliceFinesNumber'] / 25)

    resultScorista = (XScore + YScore) / 10

    XScore = 150
    YScore = 150

    '''
        Вообще говоря, больше 10 работ - не то же самое, что руководитель более 10 организаций
        Но с руководителем сложно - число повторов "Генеральный директор" считать? Тоже не очень.
        '''
    if not sum(parsers_data['ConturFocusParserModule']['RiskWordIndicators']) > 0:
        XScore += 100

    resultConturFocus = (XScore + YScore) / 10

    XScore = 0
    YScore = 0

    #    if parsers_data['InfosferaParserModule']['PassportOrigin']:
    #       XScore += 100

    #  if parsers_data['InfosferaParserModule']['LicenseOrigin']:
    #     XScore += 100

    if not parsers_data['InfosferaParserModule']['RiskRegion']:
        XScore += 100

    if not parsers_data['InfosferaParserModule']['RiskRegion2']:
        XScore += 100

    if not parsers_data['InfosferaParserModule']['JobsNum'] > 10:
        XScore += 100

        '''
            Считаем, что была работа, если работал в этом году или прошлом
            '''

    bd = parsers_data['InfosferaParserModule']['BirthDate']
    clientAge = datetime.date.today().year - parse(bd).year
    if clientAge < 25:
        YScore += 100 * (clientAge - 18) / 7
    else:
        YScore += 100

    resultInfosfera = (XScore + YScore) / 6

    YScore = 0

    if parsers_data['NBKIParserModule']['delay'] > 20000:
        YScore += 100 - 100 * (parsers_data['NBKIParserModule']['delay'] - 20000) / 80000
    else:
        YScore += 100

    if parsers_data['NBKIParserModule']['totalOverDue'] > 100000:
        YScore += 100 - 100 * (parsers_data['NBKIParserModule']['totalOverDue'] - 100000) / 200000
    else:
        YScore += 100

    if parsers_data['NBKIParserModule']['maxDelay'] > 100000:
        YScore += 100 - 100 * (parsers_data['NBKIParserModule']['maxDelay'] - 100000) / 200000
    else:
        YScore += 100

    YScore += 100 - 100 * parsers_data['NBKIParserModule']['countdue30_60inopenedaccs'] / 5
    YScore += 100 - 100 * parsers_data['NBKIParserModule']['countdue30_60inclosedaccs'] / 5
    YScore += 100 - 100 * parsers_data['NBKIParserModule']['countdue60_90inopenedaccs'] / 5
    YScore += 100 - 100 * parsers_data['NBKIParserModule']['countdue60_90inclosedaccs'] / 5

    if parsers_data['NBKIParserModule']['countdue90plusinopenedaccs'] > 3:
        YScore += 100 - 100 * (parsers_data['NBKIParserModule']['countdue90plusinopenedaccs'] - 3) / 8
    else:
        YScore += 100

    if parsers_data['NBKIParserModule']['countdue90plusinclosedaccs'] > 3:
        YScore += 100 - 100 * (parsers_data['NBKIParserModule']['countdue90plusinclosedaccs'] - 3) / 8
    else:
        YScore += 100

    resultNBKI = YScore / 9

    result = (resultScorista + resultConturFocus + resultInfosfera + resultNBKI) / 4

    return result


# Получение зависимостей от парсеров
def get_dependencies():
    # return ['NBKIParserModule']
    return ['ScoristaParserModule', 'ConturFocusParserModule', 'InfosferaParserModule', 'NBKIParserModule']


# Получение имени модуля
def get_module_name():
    return "AllScoring"
