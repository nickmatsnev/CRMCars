import re
import ast
import json
from datetime import datetime
from bs4 import BeautifulSoup
import pandas
from dateutil.relativedelta import relativedelta

MODULE_NAME = 'InfosferaParserModule'


def searchSocialNetwork(soup, SNfieldName, SNstring='Поиск в VK'):
    # 'Метод, выдергивающий какое-нибудь поле из какой-нибудь соцсети
    # 'По дефолту из VK. Формат для соцсети - так же, как у инфосферы (Поиск в ...)
    # 'Формат для поля - просто текстовая строка с именем поля. Возвращает всё, что нашёл

    outlist = []
    for aa in soup.findAll('title'):
        if aa.text == SNstring:
            for ch in aa.parent.descendants:
                if ch.string == SNfieldName:
                    for ch2 in ch.parent.find_all('fieldvalue'):
                        tmp = ch2.string
                        tmp = re.sub('\n', '', tmp)
                        outlist.append(tmp)
    return (list(set(outlist)))


def get_values(source_json):
    dictall = ast.literal_eval(source_json)
    file_xml = dictall['result']
    soup = BeautifulSoup(file_xml, 'lxml')
    inn = "NA"
    try:
        for aa in soup.findAll('fieldtitle'):
            if aa.text == "ИНН":
                inn = aa.parent.find('fieldvalue').text
    except:
        inn = "NA"

    fio = soup.find('paternal').text + " " + soup.find('first').text + " " + soup.find('middle').text

    passport_sc = soup.find('passport_series').text + soup.find('passport_number').text

    try:
        passportDate = soup.find('issuedate').text
    except:
        passportDate = "NA"

    stopWords = ["банкротство", "страховое мошенничество", "уголовное дело",
                 "уголовное нарушение", "ответчик", "нетрезвом", "невозвратный", "безнадежный", 'стоплист']

    stopWordIndicators = []
    stopWordWords = []
    stopWordChunks = []
    for wrd in stopWords:
        smth = re.findall(wrd, file_xml.lower())
        stopWordIndicators.append(len(smth))
        stopWordWords.append(wrd)
        smth = re.findall('(>((?!>).)*?' + wrd + '.*?<)', file_xml.lower())
        if len(smth) > 0:
            stopWordChunks.append(smth)

    stopWordChunks = [item for sublist in stopWordChunks for item in sublist]
    stopWordChunks = [item for sublist in stopWordChunks for item in sublist]
    stopWordChunks = list(filter(lambda x: x!= ' ', stopWordChunks))
    stopWordChunks = list(filter(lambda x: x!= '', stopWordChunks))
    
    stopWordDict = dict(zip(stopWordWords, stopWordIndicators))

    try:
        birth_date = soup.find('birthdt').text
    except:
        birth_date = "NA"
        
    birth_place = "NA"
    try:
        for aa in soup.findAll('fieldtitle'):
            if aa.text == "Место рождения":
                birth_place = aa.parent.find('fieldvalue').text
    except:
        birth_place = "NA"

    passport_origin = True if len(passport_sc) == 10 else False

    jobs = re.findall("(?s)Карьера(.*?)/FieldValue", file_xml)
    
    try:
        jobs = jobs[0].split("Место работы")
    except:
        jobs = "NA"

    smth = re.findall("(?s)Ответ №(.*?)</table>", file_xml)
    latePaymentInfo = []

    # Добавил сумму долгов по данным ФССП, она там у них оказывается есть
    currentDebts = ""
    try:
        currentDebts = dictall['data']['fssp']['sum']['result']
    except:
        currentDebts = "NA"
    
    # Ещё одни нашедшиеся данные - просрочки по кредитам! Тут отдельно считаются по уже закрытым и ещё активным
    try:
        latePaymentInClosedCredits = dictall['data']['creditRating']['rating']['count_due30_60_in_closed_accs']
        latePaymentInClosedCredits += dictall['data']['creditRating']['rating']['count_due60_90_in_closed_accs']
        latePaymentInClosedCredits += dictall['data']['creditRating']['rating']['count_due90plus_in_closed_accs']

        latePaymentInCurrentCredits = dictall['data']['creditRating']['rating']['count_due30_60_in_opened_accs']
        latePaymentInCurrentCredits += dictall['data']['creditRating']['rating']['count_due60_90_in_opened_accs']
        latePaymentInCurrentCredits += dictall['data']['creditRating']['rating']['count_due90plus_in_opened_accs']
    except:
        print("Error")

    try:
        for tmp in smth:
            checkDate = re.findall("(?s)Дата актуальности</td>\n<td>\n<p><span>(.*?)</span></p>", tmp)
            checkDate = re.findall("\d\d\.\d\d.\d\d\d\d", checkDate[0])
            latePayment = re.findall("(?s)Информация о кредитной истории</td>\n<td>\n<p><span>(.*?)</span></p>", tmp)
            if len(latePayment) > 0:
                latePaymentInfo.append((checkDate[0], latePayment[0]))
    except:
        print("error parsing credit story")

    flist = file_xml.split("РАБОТОДАТЕЛЬ: ")
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


    nRisky1 = 0
    try:
        for rr in riskyRegions:
            rr = rr.lower()
            tmp = re.findall(rr, smth)
            nRisky1 += (len(tmp))
    except:
        print("ERROR")

    nRisky2 = 0
    try:
        for rr in riskyRegions2:
            rr = rr.lower()
            tmp = re.findall(rr, smth)
            nRisky2 += (len(tmp))
    except:
        print("ERROR")

    risk_regions = True if nRisky1 > 0 else False
    risk_regions2 = True if nRisky2 > 0 else False

    VKGroups = searchSocialNetwork(soup, 'Группы')
    VKCareer = searchSocialNetwork(soup, 'Карьера')
    FBCareer = searchSocialNetwork(soup, 'Карьера', 'Поиск в Facebook')
    FBLife = searchSocialNetwork(soup, 'События из жизни', 'Поиск в Facebook')

    # Тут можно заменить пары name, value на просто ключ значение? имя:значение? а то в скоринге оно как раз и идет по имя - значение. Мне приходится конвертировать.
    return [{'name': 'Passport', 'value': passport_sc},
            {'name': 'PassportDate', 'value': passportDate},
            {'name': 'INN', 'value': inn},
            {'name': 'FIO', 'value': fio},
            {'name': 'BirthPlace', 'value': birth_place},
            {'name': 'StopWordIndicators', 'value': stopWordIndicators},
            {'name': 'StopWordWords', 'value': stopWordWords},
            {'name': 'StopWordDict', 'value': stopWordDict},
            {'name': 'StopWordChunks', 'value': stopWordChunks},
            {'name': 'BirthDate', 'value': birth_date},
            {'name': 'RiskRegion', 'value': risk_regions},
            {'name': 'RiskRegion2', 'value': risk_regions2},
            {'name': 'JobsNum', 'value': len(set(jobs))},
            {'name': 'VKGroups', 'value': VKGroups},
            {'name': 'VKCareer', 'value': VKCareer},
            {'name': 'FBCareer', 'value': FBCareer},
            {'name': 'FBLife', 'value': FBLife}
            ]


def validate(individual_json, source_json):
    scorista_res = pandas.DataFrame(get_values(source_json)).set_index('name')
    errors = []

    if scorista_res.loc['FIO'].value.lower().find(individual_json['last_name'].lower()) < 0:
        errors.append({'decription': 'Фамилия не совпадает с источником (Инфосфера)'})
    if scorista_res.loc['FIO'].value.lower().find(individual_json['first_name'].lower()) < 0:
        errors.append({'decription': 'Имя не совпадает с источником (Инфосфера)'})
    if scorista_res.loc['FIO'].value.lower().find(individual_json['middle_name'].lower()) < 0:
        errors.append({'decription': 'Отчество не совпадает с источником (Инфосфера)'})

    if individual_json['passport']['number'] != scorista_res.loc['Passport'].value:
        errors.append({'decription': 'Серия и номер паспорта не совпадают с источником (Инфосфера)'})
    brth = datetime.strptime(scorista_res.loc['BirthDate'].value, '%d.%m.%Y').date()
    if brth > datetime.now().date():
        errors.append({'decription': 'Некорректная дата рождения'})

    if individual_json['birthday'] != scorista_res.loc['BirthDate'].value:
        errors.append({'decription': 'Не совпадает дата рождения с источником (Инфосфера)'})

    if len(errors) == 0:
        return {'status': 'OK'}
    else:
        return {'status': 'Failed', 'errors': errors}


def stop_factors(individual_json, source_json):
    scorista_res = pandas.DataFrame(get_values(source_json)).set_index('name')
    errors = []
    brth = datetime.strptime(scorista_res.loc['BirthDate'].value, '%d.%m.%Y').date()
    if brth + relativedelta(years=+18) > datetime.now().date():
        errors.append({'decription': 'Заявителю нет 18 лет'})

    if sum(scorista_res.loc['StopWordIndicators'].value) > 0:
        errors.append({'decription': 'Наличие стоп-слов в характеристиках клиента по данным Инфосферы'})

    if len(errors) == 0:
        return {'status': 'OK'}
    else:
        return {'status': 'Failed', 'errors': errors}


def get_available_params():
    return [{'name': 'Passport', 'description': 'Серия и номер паспорта', 'type': 'int'},
            {'name': 'PassportDate', 'description': '', 'type': 'int'},
            {'name': 'INN', 'description': 'ИНН клиента', 'type': 'int'},
            {'name': 'FIO', 'description': 'ФИО клиента', 'type': 'string'},
            {'name': 'BirthPlace', 'description': 'Место рождения', 'type': 'string'},
            {'name': 'StopWordIndicators', 'description': 'Вектор индикаторов на наличие стоп-слов',
             'type': 'vector, int'},
            {'name': 'StopWordWords', 'description': 'Вектор обнаруженных стоп-слов',
             'type': 'vector, string'},
            {'name': 'StopWordDict', 'description': 'Словарь из обнаруженных стоп-слов с их частотой',
             'type': 'dictionary'},
            {'name': 'StopWordChunks', 'description': 'Вектор фрагментов текста со стоп-словами',
             'type': 'vector, string'},
            {'name': 'Jobs', 'description': 'Вектор (место работы, доход, год, ИНН работодателя)',
             'type': 'vector, string'},
            {'name': 'BirthDate', 'description': 'Дата рождения', 'type': 'date'},
            {'name': 'RiskRegion',
             'description': 'Факт регистрации в рисковых регионах Архангельская область; Башкортостан; Волгоградская область; Ивановская область; Кировская область; Краснодарский край; Мордовия; Мурманская область; Нижегородская область; Ростовская область; Саратовская область; Ставропольский край; Татарстан; Ульяновская область; Челябинская область; Дагестан; Ингушетия; Северная Осетия - Алания; Чеченская республика',
             'type': 'bool'},
            {'name': 'RiskRegion2',
             'description': 'Регистрация в  в рисковых регионах Дагестан; Ингушетия; Северная Осетия-Алания; Чеченская республика',
             'type': 'bool'},
            {'name': 'JobsNum', 'description': 'Число работ', 'type': 'int'},
            {'name': 'VKGroups', 'description': 'Группы из ВК', 'type': 'vector, string'},
            {'name': 'VKCareer', 'description': 'Карьера по ВК', 'type': 'vector, string'},
            {'name': 'FBCareer', 'description': 'Карьера по Facebook', 'type': 'vector, string'},
            {'name': 'FBLife', 'description': 'События из жизни по Facebook', 'type': 'vector, string'},
            ]


def get_module_source():
    return 'ISphere'


def get_module_name():
    return MODULE_NAME
