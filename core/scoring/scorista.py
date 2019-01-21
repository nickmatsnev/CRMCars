import re
import json
import requests
import hashlib
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup


def make_check_map(name, type, val, info='', plan='', fact=''):
    return {'name': name,
            'type': type,
            'value': val,
            'info': info,
            'plan': plan,
            'fact': fact}


def make_reason_map(linked_check, description):
    return {'linked_check': linked_check,
            'description': description}


def total_debt(flist):
    '''
    Метод, суммирующий долг по всем судопроизводствам клиента

    :param flist: исходный html как строка.split("sprAnswer spr-question js_tooltip")
    :return: суммарный долг
    '''
    fl = flist[1]
    varslist2 = fl.split("<td class=\"legend\">")

    varSum = 0

    for vr in varslist2[1:]:
        varName = re.findall("(.*?)</td>", vr)[0]
        if varName == 'Долг':
            soup = BeautifulSoup(vr, 'lxml')
            vvv = soup.findAll('p')
            varVals = []
            for vv in vvv:
                varVals.append(vv.text)
            varSum = varSum + int(varVals[1:][0])

    return varSum


def get_scorista():
    username = 'dmitry@korishchenko.ru'
    nonce = hashlib.sha1()
    token = '4def557c4fa35791f07cc8d4faf7c3a5f7ae7c93'
    password = hashlib.sha1((nonce.hexdigest() + token).encode('utf-8'))

    url = 'https://api.scorista.ru/dossier/json'

    headers = {'Content-Type': 'application/json',
               'username': username,
               'nonce': nonce.hexdigest(),
               'password': password.hexdigest()}

    request = {"requestID": "agrid5c41aad42dbed"}

    r = requests.post(url, data=json.dumps(request), headers=headers)
    scorista_res = json.loads(r.text)
    return json.dumps(scorista_res, indent=4, ensure_ascii=True)


def get_checks(passport_user, license_user, scorista_json):
    res_list = []
    dictall = json.loads(scorista_json)
    fileall = dictall['data']['cronos']['html'].replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
    flist = fileall.split("sprAnswer spr-question js_tooltip")

    passport_sc = re.findall("Паспорт: (.*?)</p>", fileall)[0]
    passport_sc = re.sub('</?span>', '', passport_sc)
    passport_user, passport_sc = passport_user.replace(' ', ''), passport_sc.replace(' ', '')
    license_sc = re.findall("ПРАВА СЕРИЯ-НОМЕР: (.*?)</p>", fileall)[0]

    check_passport = passport_user == passport_sc
    res_list.append(
        make_check_map('check_passport', 'bool', check_passport, 'Проверка, есть ли у клиента указанный им паспорт',
                       passport_sc, passport_user))

    check_license = license_user == license_sc
    res_list.append(make_check_map('check_license', 'bool', check_license,
                                   'Проверка, есть ли у клиента указанное им водительское удостоверение', license_sc,
                                   license_user))

    license_exp_date = datetime.strptime(re.findall("ДАТА ВЫДАЧИ: (.*?)</p>", fileall)[0], '%d.%m.%Y').date()
    check_license_exp_date = license_exp_date + relativedelta(years=+10) > datetime.now().date()
    res_list.append(make_check_map('check_license_exp_date', 'bool', check_license_exp_date,
                                   'Проверка, не истекло ли водительское удостоверение', str(datetime.now().date()),
                                   str(license_exp_date)))

    check_drunk_drive = False if fileall.find('нетрезвом') != -1 else True
    res_list.append(make_check_map('check_drunk_drive', 'bool', check_drunk_drive,
                                   'Проверка, управлял ли клиент транспортным средством в нетрезвом виде'))

    check_bank_stoplist = False if fileall.find('СТОПЛИСТ') != -1 else True
    res_list.append(make_check_map('check_bank_stoplist', 'bool', check_bank_stoplist,
                                   'Проверка, находится ли клиент в стоплистах банков'))

    check_total_debt = total_debt(flist) < 100000
    res_list.append(make_check_map('check_total_debt', 'bool', check_total_debt,
                                   'Проверка, не превышает совокупный действующий долг по исполнительным производствам ФССП клиента суммы в 100000 рублей',
                                   '100000', str(total_debt(flist))))

    birth_date = re.findall("Дата рождения: (.*?)</p>", fileall)[0]
    birth_date = datetime.strptime(re.sub('</?span>', '', birth_date).split(' ')[0], '%d.%m.%Y').date()
    check_correct_birth = birth_date < datetime.now().date()
    res_list.append(make_check_map('check_correct_birth', 'bool', check_correct_birth,
                                   'Проверка корректности указанной даты рождения'))

    check_terrorism = True if dictall['data']['rosFinMonitoring']['result'] == 0 else False
    res_list.append(make_check_map('check_terrorism', 'bool', check_terrorism,
                                   'Проверка на присутствие в списке террористов и экстремистов'))

    check_fms_invalid_passport = True if dictall['data']['fms']['result'] == 0 else False
    res_list.append(make_check_map('check_fms_invalid_passport', 'bool', check_fms_invalid_passport,
                                   'Проверка на недействительность указанного паспорта по базе ФМС'))

    check_invalid_inn = True if dictall['data']['inn']['result'] == 0 else False
    res_list.append(make_check_map('check_invalid_inn', 'bool', check_invalid_inn, 'Проверка на наличие ИНН у клиента'))

    check_origin = True if len(passport_sc) == 10 else False
    res_list.append(make_check_map('check_origin', 'bool', check_origin,
                                   'Проверка, что клиент не является резидентом другого государства'))

    check_license_origin = True if len(license_sc) == 10 else False
    res_list.append(make_check_map('check_license_origin', 'bool', check_license_origin,
                                   'Проверка, что водительское удостоверение не выдано другим государством'))

    flist = fileall.split("РАБОТОДАТЕЛЬ: ")
    jobs = []
    for fl in flist[1:-1]:
        jobs.append(re.findall("(.*?)</p>", fl)[0])

    check_num_of_jobs = True if len(set(jobs)) <= 10 else False
    res_list.append(make_check_map('check_num_of_jobs', 'bool', check_num_of_jobs,
                                   'Проверка, что клиент не работал/работает более чем на 10 работах'))

    address = re.findall("Адрес: (.*?)</p>", fileall)[0]
    address = re.sub('</?span>', '', address)
    blacklist = ['Дагестан', 'Ингушетия', 'Северная Осетия-Алания', 'Чеченская республика']
    check_risk_regions = True
    for region in blacklist:
        if region in address:
            check_risk_regions = False
    res_list.append(make_check_map('check_risk_regions', 'bool', check_risk_regions,
                                   'Проверка, что клиент не имеет регистрации в рисковых регионах Дагестан; Ингушетия; Северная Осетия-Алания; Чеченская республика'))

    return {'checks': res_list}


def get_scoring(checks_json):
    scoring = 100
    dictall = json.loads(checks_json)
    reasons = []

    if not dictall['checks'][-4]['value']:
        scoring -= 20
        reasons.append(make_reason_map(dictall['checks'][-4]['name'], 'Клиент является резидентом другого государства'))

    if not dictall['checks'][-3]['value']:
        scoring -= 20
        reasons.append(
            make_reason_map(dictall['checks'][-3]['name'], 'Водительское удостоверение выдано другим государством'))

    if not dictall['checks'][-2]['value']:
        scoring -= 20
        reasons.append(
            make_reason_map(dictall['checks'][-2]['name'], 'Клиент не работал/работает более чем на 10 работах'))

    if not dictall['checks'][-1]['value']:
        scoring -= 20
        reasons.append(
            make_reason_map(dictall['checks'][-1]['name'],
                            'Регистрация в рисковых регионах Дагестан; Ингушетия; Северная Осетия-Алания; Чеченская республика'))

    return {'scoring': scoring, 'reasons': reasons}
