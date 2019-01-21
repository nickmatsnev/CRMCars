import re
import json
import requests
import hashlib
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup


def make_check_map(name, type, val, info=''):
    return {'name': name,
            'type': type,
            'value': val,
            'info': info}


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
    return json.dumps(scorista_res, indent=4, ensure_ascii=False)


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
    res_list.append(make_check_map('check_passport', 'bool', check_passport))

    check_license = license_user == license_sc
    res_list.append(make_check_map('check_license', 'bool', check_license))

    license_exp_date = datetime.strptime(re.findall("ДАТА ВЫДАЧИ: (.*?)</p>", fileall)[0], '%d.%m.%Y').date()
    check_license_exp_date = license_exp_date + relativedelta(years=+10) > datetime.now().date()
    res_list.append(make_check_map('check_license_exp_date', 'bool', check_license_exp_date))

    check_drunk_drive = False if fileall.find('нетрезвом') != -1 else True
    res_list.append(make_check_map('check_drunk_drive', 'bool', check_drunk_drive))

    check_bank_stoplist = False if fileall.find('СТОПЛИСТ') != -1 else True
    res_list.append(make_check_map('check_bank_stoplist', 'bool', check_bank_stoplist))

    check_total_debt = total_debt(flist) < 100000
    res_list.append(make_check_map('check_total_debt', 'bool', check_total_debt, str(total_debt(flist))))

    birth_date = re.findall("Дата рождения: (.*?)</p>", fileall)[0]
    birth_date = datetime.strptime(re.sub('</?span>', '', birth_date).split(' ')[0], '%d.%m.%Y').date()
    check_correct_birth = birth_date < datetime.now().date()
    res_list.append(make_check_map('check_correct_birth', 'bool', check_correct_birth))

    check_terrorism = True if dictall['data']['rosFinMonitoring']['result'] == 0 else False
    res_list.append(make_check_map('check_terrorism', 'bool', check_terrorism))

    check_fms_invalid_passport = True if dictall['data']['fms']['result'] == 0 else False
    res_list.append(make_check_map('check_fms_invalid_passport', 'bool', check_fms_invalid_passport,
                                   dictall['data']['fms']['textResult']))

    check_invalid_inn = True if dictall['data']['inn']['result'] == 0 else False
    res_list.append(make_check_map('check_invalid_inn', 'bool', check_invalid_inn,
                                   dictall['data']['inn']['textResult']))

    return res_list


def get_scoring(scorista_json):
    scoring = 100
    dictall = json.loads(scorista_json)
    fileall = dictall['data']['cronos']['html'].replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')

    license_sc = re.findall("ПРАВА СЕРИЯ-НОМЕР: (.*?)</p>", fileall)[0]
    if len(license_sc) != 10:
        scoring -= 20

    passport_sc = re.findall("Паспорт: (.*?)</p>", fileall)[0]
    passport_sc = re.sub('</?span>', '', passport_sc).replace(' ', '')
    if len(passport_sc) != 10:
        scoring -= 20

    flist = fileall.split("РАБОТОДАТЕЛЬ: ")
    jobs = []
    for fl in flist[1:-1]:
        jobs.append(re.findall("(.*?)</p>", fl)[0])

    if len(set(jobs)) > 10:
        scoring -= 20

    address = re.findall("Адрес: (.*?)</p>", fileall)[0]
    address = re.sub('</?span>', '', address)
    blacklist = ['Дагестан', 'Ингушетия', 'Северная Осетия-Алания', 'Чеченская республика']
    for region in blacklist:
        if region in address:
            scoring -= 20
            break

    return {'scoring': scoring}

#
# # For test purposes
# with open('checks.json', 'w') as outfile:
#     outfile.write(get_checks('4607 167793', '50КЕ066037', get_scorista()))
#
# with open('scoring.json', 'w') as outfile:
#     outfile.write(get_scoring(get_scorista()))
