import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import pandas
import ast
from dateutil.relativedelta import relativedelta

MODULE_NAME = 'ScoristaParserModule'


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


def get_values(source_json):
    # ТУТ обязательно ast, из за особенностей сохранения json  в базу
    dictall = json.loads(source_json)
    fileall = dictall['data']['cronos']['html'].replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
    flist = fileall.split("sprAnswer spr-question js_tooltip")

    smth = re.findall("(?s)>ИНН<(.*?)</p>", fileall)
    try:
        inn = smth[0]
        inn = re.sub("[^0-9]", "", inn)
    except:
        inn = "NA"

    smth = re.findall("(?s)<td class=\"legend\">ФИО</td>(.*?)</u></p>", fileall)
    fio = smth[0]
    fio = re.sub("[^А-Яа-я ]", "", fio)

    passport_sc = re.findall("Паспорт: (.*?)</p>", fileall)[0].replace(' ', '')
    passport_sc = re.sub('</?span>', '', passport_sc)

    # Добавил возможность вытащить все его паспорта
    try:
        smth = re.findall("(?s)<td class=\"legend\">Паспорт</td>(.*?)<td class=\"legend\">", fileall)
        allPassports = re.findall("<p><u>(.*?)</u></p>", smth[0])
    except:
        allPassports = passport_sc

    try:
        smth = re.findall("(?s)<td class=\"legend\">Документ</td>(.*?)<td class=\"legend\">", fileall)
        passportDate = smth[0]
        passportDate = re.findall("\d\d\.\d\d.\d\d\d\d", passportDate)
        passportDate = datetime.strptime(passportDate[0], '%d.%m.%Y').date()
    except:
        passportDate = "NA"

    try:
        license_sc = re.findall("ПРАВА СЕРИЯ-НОМЕР: (.*?)</p>", fileall)[0]
    except:
        try:
            license_sc = re.findall("ВОД. УД.: (.*?)</p>", fileall)[0]
        except:
            license_sc = "NA"

    try:
        license_exp_date = datetime.strptime(re.findall("ДАТА ВЫДАЧИ: (.*?)</p>", fileall)[0], '%d.%m.%Y').date()
    except:
        license_exp_date = "NA"

    try:
        smth = re.findall("(?s)<td class=\"legend\">Документ</td>(.*?)<td class=\"legend\">", fileall)
        passportIssuer = smth[0]
        passportIssuer = re.findall("\d\d\.\d\d.\d\d\d\d(.*?)[^А-Яа-я ]\d", passportIssuer)
    except:
        passportIssuer = "NA"

    smth = re.findall("(?s)<td class=\"legend\">Документ</td>(.*?)<td class=\"legend\">", fileall)
    try:
        passportIssuerCode = smth[0]
        passportIssuerCode = re.findall("\d\d\.\d\d.\d\d\d\d(.*?)</span></p>", passportIssuerCode)
        passportIssuerCode = re.sub("[^0-9]", "", passportIssuerCode[1])
    except:
        passportIssuerCode = "NA"

    smth = re.findall("(?s)<td class=\"legend\">Место рождения</td>(.*?)<td class=\"legend\">", fileall)
    birthPlace = "NA"
    try:
        for sm in smth:
            birthPlace = re.sub("[^А-Яа-я ]", "", sm)
    except:
        birthPlace = "NA"

    smth = re.findall("ПРИЧИНЫ ЗАМЕНЫ ПАСПОРТА", fileall)
    numberPassportChanges = (len(smth))

    stopWords = ["банкротство", "страховое мошенничество", "уголовное дело",
                 "уголовное нарушение", "ответчик", "нетрезвом", "невозвратный", "безнадежный", 'стоплист',
                 'наркотик']
    
    stopWordIndicators = []
    stopWordWords = []
    for wrd in stopWords:
        smth = re.findall(wrd, fileall.lower())
        stopWordIndicators.append(len(smth))
        stopWordWords.append(wrd)

    drunk_drive = False if fileall.find('нетрезвом') == -1 else True
    bank_stoplist = False if fileall.find('СТОПЛИСТ') == -1 else True

    tot_debt = total_debt(flist)

    try:
        birth_date = re.findall("Дата рождения: (.*?)</p>", fileall)[0]
        birth_date = datetime.strptime(re.sub('</?span>', '', birth_date).split(' ')[0], '%d.%m.%Y').date()
    except:
        birth_date = "NA"

    terrorism = False if dictall['data']['rosFinMonitoring']['result'] != 0 else True
    fms_invalid_passport = False if dictall['data']['fms']['result'] != 0 else True
    invalid_inn = False if dictall['data']['inn']['result'] != 0 else True

    try:
        license_origin = True if len(license_sc) == 10 else False
    except:
        license_origin = False

    smth = re.findall("Штраф ГИБДД", fileall)
    smth2 = re.findall("НАРУШЕНИЕ ПДД", fileall)
    roadPoliceFinesNumber = max(len(smth), len(smth2))

    soup = BeautifulSoup(fileall, 'lxml')
    carsList = []
    ss = soup.findAll('p')
    for sa in ss:
        if sa.text.find('VIN') >= 0:
            tmp = sa.parent.text
            tmp = re.sub(' АМТС', '', tmp)
            carVendor = re.findall("МАРКА(.*?)\n", tmp)
            carModel = re.findall("МОДЕЛЬ(.*?)\n", tmp)
            if len(carVendor) == 0:
                carVendor = re.findall("МАРКА:(.*?):", tmp)
            if len(carModel) == 0:
                carModel = re.findall("МОДЕЛЬ:(.*?):", tmp)
            try:
                carVendor = re.sub('МОДЕЛЬ', '', carVendor)
                carModel = re.sub('МОДЕЛЬ', '', carModel)
                carVendor = (' '.join(list(carVendor[0])))
                carModel = (' '.join(list(carModel[0])))
            except:
                adummy = 2
            carsList.append((carVendor, carModel))

    smth = re.findall("(?s)Ответ №(.*?)</table>", fileall)
    latePaymentInfo = []

    # Добавил сумму долгов по данным ФССП, она там у них оказывается есть
    currentDebts = dictall['data']['fssp']['sum']['result']

    # Ещё одни нашедшиеся данные - просрочки по кредитам! Тут отдельно считаются по уже закрытым и ещё активным
    latePaymentInClosedCredits = dictall['data']['creditRating']['rating']['count_due30_60_in_closed_accs']
    latePaymentInClosedCredits += dictall['data']['creditRating']['rating']['count_due60_90_in_closed_accs']
    latePaymentInClosedCredits += dictall['data']['creditRating']['rating']['count_due90plus_in_closed_accs']

    latePaymentInCurrentCredits = dictall['data']['creditRating']['rating']['count_due30_60_in_opened_accs']
    latePaymentInCurrentCredits += dictall['data']['creditRating']['rating']['count_due60_90_in_opened_accs']
    latePaymentInCurrentCredits += dictall['data']['creditRating']['rating']['count_due90plus_in_opened_accs']

    try:
        for tmp in smth:
            checkDate = re.findall("(?s)Дата актуальности</td>\n<td>\n<p><span>(.*?)</span></p>", tmp)
            checkDate = re.findall("\d\d\.\d\d.\d\d\d\d", checkDate[0])
            latePayment = re.findall("(?s)Информация о кредитной истории</td>\n<td>\n<p><span>(.*?)</span></p>", tmp)
            if len(latePayment) > 0:
                latePaymentInfo.append((checkDate[0], latePayment[0]))
    except:
        print("error parsing credit story")

    flist = fileall.split("РАБОТОДАТЕЛЬ: ")
    jobs = []
    for fl in flist[1:]:
        smthName = re.findall("(.*?)</p>", fl)[0]
        smthVar = re.findall("ДОХОД: (.*?)</p>", fl)
        smthDate = re.findall("ГОД ДОХОДА: (.*?)</p>", fl)
        smthINN = re.findall("ИНН РАБОТОДАТЕЛЯ: (.*?)</p>", fl)
        jobs.append((smthName, smthVar, smthDate, smthINN))

    jobsAll = jobs

    jobs = []
    for fl in flist[1:-1]:
        jobs.append(re.findall("(.*?)</p>", fl)[0])

    riskyRegions = ["Архангельская", "Башкортостан", "Волгоградская", "Ивановская",
                    "Кировская", "Краснодарский", "Мордовия", "Мурманская", "Нижегородская",
                    "Ростовская", "Саратовская", "Ставропольский", "Татарстан", "Ульяновская",
                    "Челябинская", "Дагестан", "Ингушетия", "Алания", "Чеченская", "Чечня"]

    riskyRegions2 = ["Дагестан", "Ингушетия", "Алания", "Чеченская", "Чечня"]

    smth = fileall
    nRisky1 = 0
    nRisky2 = 0

    if len(smth) > 0:
        smth = smth.lower()
        for rr in riskyRegions:
            rr = rr.lower()
            tmp = re.findall(rr, smth)
            nRisky1 += (len(tmp))
        for rr in riskyRegions2:
            rr = rr.lower()
            tmp = re.findall(rr, smth)
            nRisky2 += (len(tmp))

    risk_regions = True if nRisky1 > 0 else False
    risk_regions2 = True if nRisky2 > 0 else False

    # Тут можно заменить пары name, value на просто ключ значение? имя:значение? а то в скоринге оно как раз и идет по имя - значение. Мне приходится конвертировать.
    return [{'name': 'Passport', 'value': passport_sc},
            {'name': 'PassportDate', 'value': passportDate},
            {'name': 'INN', 'value': inn},
            {'name': 'FIO', 'value': fio},
            {'name': 'PassportIssuer', 'value': passportIssuer},
            {'name': 'PassportIssuerCode', 'value': passportIssuerCode},
            {'name': 'BirthPlace', 'value': birthPlace},
            {'name': 'NumberPassportChanges', 'value': numberPassportChanges},
            {'name': 'License', 'value': license_sc},
            {'name': 'LicenseExpDate', 'value': license_exp_date},
            {'name': 'StopWordIndicators', 'value': stopWordIndicators},
            {'name': 'StopWordWords', 'value': stopWordWords},
            {'name': 'BankStopList', 'value': bank_stoplist},
            {'name': 'DrunkDrive', 'value': drunk_drive},
            {'name': 'TotalDebt', 'value': tot_debt},
            {'name': 'BirthDate', 'value': birth_date},
            {'name': 'Terrorism', 'value': terrorism},
            {'name': 'FMSInvalidPassport', 'value': fms_invalid_passport},
            {'name': 'InvalidINN', 'value': invalid_inn},
            {'name': 'PassportOrigin', 'value': ""},
            {'name': 'LicenseOrigin', 'value': license_origin},
            {'name': 'RiskRegion', 'value': risk_regions},
            {'name': 'RiskRegion2', 'value': risk_regions2},
            {'name': 'RoadPoliceFinesNumber', 'value': roadPoliceFinesNumber},
            {'name': 'CarsList', 'value': carsList},
            {'name': 'LatePaymentInfo', 'value': latePaymentInfo},
            {'name': 'Jobs', 'value': jobsAll},
            {'name': 'JobsNum', 'value': len(set(jobs))},
            {'name': 'allPassports', 'value': allPassports},
            {'name': 'currentDebts', 'value': currentDebts},
            {'name': 'latePaymentInClosedCredits', 'value': latePaymentInClosedCredits},
            {'name': 'latePaymentInCurrentCredits', 'value': latePaymentInCurrentCredits}

            ]


def validate(individual_json, source_json):
    scorista_res = pandas.DataFrame(get_values(source_json)).set_index('name')
    errors = []

    if scorista_res.loc['FIO'].value.lower().find(individual_json['last_name'].lower()) < 0:
        errors.append({'decription': 'Фамилия не совпадает с источником (Скориста)'})
    if scorista_res.loc['FIO'].value.lower().find(individual_json['first_name'].lower()) < 0:
        errors.append({'decription': 'Имя не совпадает с источником (Скориста)'})
    if scorista_res.loc['FIO'].value.lower().find(individual_json['middle_name'].lower()) < 0:
        errors.append({'decription': 'Отчество не совпадает с источником (Скориста)'})

    if individual_json['passport']['number'] != scorista_res.loc['Passport'].value:
        errors.append({'decription': 'Серия и номер паспорта не совпадают с источником (Скориста)'})
    if individual_json['driver_license']['number'] != scorista_res.loc['License'].value:
        errors.append({'decription': 'Серия и номер ВУ не совпадают с источником (Скориста)'})
    '''
    if scorista_res.loc['BirthDate'].value > datetime.now().date():
        errors.append({'decription': 'Некорректная дата рождения'})

    if individual_json['birthday'] != scorista_res.loc['BirthDate'].value:
        errors.append({'decription': 'Не совпадает дата рождения с источником (Скориста)'})

    Мне не нравится эта проверка, потому что сложно написать её так, чтобы она корректно учла все возможные различия в написании
    По этой же причине проверку подразделения, выдавшего паспорт, я пока не писал: там совсем разброд и шатание
    
    -- можно взять векторный способ - сколько букв или слов совпадает.
    '''

    if not scorista_res.loc['FMSInvalidPassport'].value:
        errors.append({'decription': 'Недействительность паспорта в базе ФМС по данным Скористы'})
    if not scorista_res.loc['InvalidINN'].value:
        errors.append({'decription': 'У клиента недействительный ИНН по данным Скористы'})

    if len(errors) == 0:
        return {'status': 'OK'}
    else:
        return {'status': 'Failed', 'errors': errors}


def stop_factors(individual_json, source_json):
    scorista_res = pandas.DataFrame(get_values(source_json)).set_index('name')
    errors = []

    if scorista_res.loc['BirthDate'].value + relativedelta(years=+18) > datetime.now().date():
        errors.append({'decription': 'Заявителю нет 18 лет'})
    if scorista_res.loc['NumberPassportChanges'].value > 5:
        errors.append({'decription': 'Паспорт менялся больше 5 раз'})
    if scorista_res.loc['LicenseExpDate'].value + relativedelta(years=+10) < datetime.now().date():
        errors.append({'decription': 'Истёк срок действия водительского удостоверения'})

    if sum(scorista_res.loc['StopWordIndicators'].value) > 0:
        errors.append({'decription': 'Наличие стоп-слов в характеристиках клиента по описанию Скористы'})

    if scorista_res.loc['RoadPoliceFinesNumber'].value > 25:
        errors.append({'decription': 'Критически большое количество штрафов за нарушение ПДД по данным Скористы'})

    '''
    Пока непонятно, в каком формате будут поступать данные по тому, какую машину человек хочет взять.
    В примере individual_json этого нет.
    Соответствующую группу стоп-факторов надо будет дописать
    '''
    latePaymentInfo = scorista_res.loc['LatePaymentInfo']
    # здесь падает, т..кк. в latePaymentInfo нет данных ()
    nDelays = 0
    try:
        for pm in latePaymentInfo:
            tmp = datetime.strptime(pm[0], '%d.%m.%Y').date()
            if tmp + relativedelta(years=+2) > datetime.now().date():
                if pm[1].find("есть") > -1 or pm[1].find("были") > -1:
                    nDelays += 1
    except:
        nDelays = 0

    nDClosed = scorista_res.loc['latePaymentInClosedCredits']
    nDCurrent = scorista_res.loc['latePaymentInCurrentCredits']

    if nDelays > 1:
        errors.append({'decription': 'Наличие двух и более просрочек в течение последних двух лет по данным Скористы'})
    if nDClosed.size > 2:
        errors.append({'decription': 'Наличие трёх и более просрочек по кредитам по данным Скористы'})
    if nDCurrent.size > 0:
        errors.append({'decription': 'В настоящий момент есть просрочка по кредиту по данным Скористы'})

    if scorista_res.loc['BankStopList'].value:
        errors.append({'decription': 'Клиент присутствует в стоп-листах банков по данным Скористы'})
    if scorista_res.loc['DrunkDrive'].value:
        errors.append({'decription': 'Судопроизводства за нетрезвое вождение по данным Скористы'})

    if scorista_res.loc['TotalDebt'].value > 150000:
        errors.append({'decription': 'Задолженность по судопроизводствам более 150000 по данным Скористы'})

    if scorista_res.loc['currentDebts'].value > 150000:
        errors.append({'decription': 'Задолженность по судопроизводствам более 150000 по данным Скористы'})

    if len(errors) == 0:
        return {'status': 'OK'}
    else:
        return {'status': 'Failed', 'errors': errors}


def get_available_params():
    return [{'name': 'Passport', 'description': 'Серия и номер паспорта', 'type': 'int'},
            {'name': 'PassportDate', 'description': '', 'type': 'int'},
            {'name': 'INN', 'description': 'ИНН клиента', 'type': 'int'},
            {'name': 'FIO', 'description': 'ФИО клиента', 'type': 'string'},
            {'name': 'PassportIssuer', 'description': 'Подразделение, выдавшее паспорт', 'type': 'string'},
            {'name': 'PassportIssuerCode', 'description': 'Код подразделения, выдавшего паспорт', 'type': 'int'},
            {'name': 'BirthPlace', 'description': 'Место рождения', 'type': 'string'},
            {'name': 'NumberPassportChanges', 'description': 'Число замен паспорта', 'type': 'int'},
            {'name': 'StopWordIndicators', 'description': 'Вектор индикаторов на наличие стоп-слов',
             'type': 'vector, int'},
            {'name': 'StopWordWords', 'description': 'Вектор обнаруженных стоп-слов',
             'type': 'vector, string'},
            {'name': 'RoadPoliceFinesNumber', 'description': 'Количество штрафов ГИБДД', 'type': 'int'},
            {'name': 'CarsList', 'description': 'Вектор автомобилей (марка, модель)', 'type': 'vector, string'},
            {'name': 'LatePaymentInfo', 'description': 'Вектор (дата проверки, результат по наличию просрочек)',
             'type': 'vector, string'},
            {'name': 'Jobs', 'description': 'Вектор (место работы, доход, год, ИНН работодателя)',
             'type': 'vector, string'},
            {'name': 'License', 'description': 'Серия и номер паспорта ВУ', 'type': 'int'},
            {'name': 'LicenseExpDate', 'description': 'Срок действия ВУ', 'type': 'date'},
            {'name': 'BankStopList', 'description': 'Присутствие в стоп листах банков', 'type': 'bool'},
            {'name': 'DrunkDrive', 'description': 'Отметки о езде в нетрезвом виде', 'type': 'bool'},
            {'name': 'TotalDebt', 'description': 'Суммарный долг по судопроизводствам', 'type': 'float'},
            {'name': 'BirthDate', 'description': 'Дата рождения', 'type': 'date'},
            {'name': 'Terrorism', 'description': 'Присутствие в перечне террористов/экстремистов', 'type': 'bool'},
            {'name': 'FMSInvalidPassport', 'description': 'Недействительность паспорта в базе ФМС', 'type': 'bool'},
            {'name': 'InvalidINN', 'description': 'Недействительный ИНН', 'type': 'bool'},
            {'name': 'PassportOrigin', 'description': 'Паспорт выдан в России', 'type': 'bool'},
            {'name': 'LicenseOrigin', 'description': 'ВУ выдано в России', 'type': 'bool'},
            {'name': 'RiskRegion',
             'description': 'Регистрация в  в рисковых регионах Дагестан; Ингушетия; Северная Осетия-Алания; Чеченская республика',
             'type': 'bool'},
            {'name': 'RiskRegion2',
             'description': 'Регистрация в  в рисковых регионах Дагестан; Ингушетия; Северная Осетия-Алания; Чеченская республика',
             'type': 'bool'},
            {'name': 'JobsNum', 'description': 'Число работ', 'type': 'int'},
            {'name': 'allPassports', 'description': 'Список паспортов', 'type': 'vector, int'},
            {'name': 'currentDebts', 'description': 'Объем текущих долгов по базе данных ФССП', 'type': 'float'},
            {'name': 'latePaymentInClosedCredits',
             'description': 'Количество просроченных более, чем на 30 дней кредитов', 'type': 'int'},
            {'name': 'latePaymentInCurrentCredits',
             'description': 'Количество текущих просроченных более, чем на 30 дней кредитов', 'type': 'int'}
            ]


def get_module_source():
    return 'Scorista'


def get_module_name():
    return MODULE_NAME
