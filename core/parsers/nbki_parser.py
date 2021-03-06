import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import pandas
import ast
from dateutil.relativedelta import relativedelta

MODULE_NAME = 'NBKIParserModule'


def get_values(source_json):
    dictall = ast.literal_eval(source_json)
    file_xml = dictall['result']
    soup = BeautifulSoup(file_xml, 'lxml')

    try:
        fio = soup.find('lastname').text + " " + soup.find('firstname').text + " " + soup.find('middlename').text
    except:
        fio = "NA"

    passport_sc = soup.find('series').text + " " + soup.find('number').text

    try:
        passportDate = soup.find('issuedate').text
    except:
        passportDate = "NA"

    try:
        birth_date = soup.find('datebirth').text
    except:
        birth_date = "NA"

    try:
        totalOverDue = int(soup.find('totaloverdue').text)
    except:
        totalOverDue = 0

    try:
        delay = int(soup.find('delay').text)
    except:
        delay = 0

    try:
        maxDelay = int(soup.find('maxdeleay').text)
    except:
        maxDelay = 0
    try:
        closednegative = soup.find('closednegative').text
    except:
        closednegative = "NA"
    try:
        countdue30_60inopenedaccs = int(soup.find('countdue30_60inopenedaccs').text)
    except:
        countdue30_60inopenedaccs = 0
    try:
        countdue30_60inclosedaccs = int(soup.find('countdue30_60inclosedaccs').text)
    except:
        countdue30_60inclosedaccs = 0

    try:
        countdue60_90inopenedaccs = int(soup.find('countdue60_90inopenedaccs').text)
    except:
        countdue60_90inopenedaccs = 0

    try:
        countdue60_90inclosedaccs = int(soup.find('countdue60_90inclosedaccs').text)
    except:
        countdue60_90inclosedaccs = 0

    try:
        countdue90plusinopenedaccs = int(soup.find('countdue90plusinopenedaccs').text)
    except:
        countdue90plusinopenedaccs = 0

    try:
        countdue90plusinclosedaccs = int(soup.find('countdue90plusinclosedaccs').text)
    except:
        countdue90plusinclosedaccs = 0
    fact_hasnewer = False
    try:
        hasnewer = soup.find('hasnewer').text

        if hasnewer == "Y":
            fact_newer = True
    except:
        hasnewer = "NA"

    fact_invalid = False
    try:
        invalid = soup.find('invalid').text
        if invalid == "Y":
            fact_invalid = True
    except:
        invalid = "NA"
    fact_wanted = False
    try:
        wanted = soup.find('wanted').text
        if wanted == "Y":
            fact_wanted = True
    except:
        wanted = "NA"

    # Тут можно заменить пары name, value на просто ключ значение? имя:значение? а то в скоринге оно как раз и идет по имя - значение. Мне приходится конвертировать.
    return [{'name': 'Passport', 'value': passport_sc},
            {'name': 'PassportDate', 'value': passportDate},
            {'name': 'FIO', 'value': fio},
            {'name': 'BirthDate', 'value': birth_date},
            {'name': 'totalOverDue', 'value': totalOverDue},
            {'name': 'delay', 'value': delay},
            {'name': 'maxDelay', 'value': maxDelay},
            {'name': 'closednegative', 'value': closednegative},
            {'name': 'countdue30_60inopenedaccs', 'value': countdue30_60inopenedaccs},
            {'name': 'countdue30_60inclosedaccs', 'value': countdue30_60inclosedaccs},
            {'name': 'countdue60_90inopenedaccs', 'value': countdue60_90inopenedaccs},
            {'name': 'countdue60_90inclosedaccs', 'value': countdue60_90inclosedaccs},
            {'name': 'countdue90plusinopenedaccs', 'value': countdue90plusinopenedaccs},
            {'name': 'countdue90plusinclosedaccs', 'value': countdue90plusinclosedaccs},
            {'name': 'hasnewer', 'value': hasnewer},
            {'name': 'invalid', 'value': invalid},
            {'name': 'wanted', 'value': wanted},
            {'name': 'fact_hasnewer', 'value': fact_hasnewer},
            {'name': 'fact_invalid', 'value': fact_invalid},
            {'name': 'fact_wanted', 'value': fact_wanted}
            ]


def validate(individual_json, source_json):
    # scorista_res = pandas.DataFrame(get_values(source_json)).set_index('name')
    errors = []

    # if scorista_res.loc['FIO'].value.lower().find(individual_json['last_name'].lower()) < 0:
    #     errors.append({'decription': 'Фамилия не совпадает с источником (НБКИ)'})
    # if scorista_res.loc['FIO'].value.lower().find(individual_json['first_name'].lower()) < 0:
    #     errors.append({'decription': 'Имя не совпадает с источником (НБКИ)'})
    # if scorista_res.loc['FIO'].value.lower().find(individual_json['middle_name'].lower()) < 0:
    #     errors.append({'decription': 'Отчество не совпадает с источником (НБКИ)'})
    #
    # if individual_json['passport']['number'] != scorista_res.loc['Passport'].value:
    #     errors.append({'decription': 'Серия и номер паспорта не совпадают с источником (НБКИ)'})
    # brth = datetime.strptime(scorista_res.loc['BirthDate'].value, '%d.%m.%Y').date()
    #
    # if brth > datetime.now().date():
    #     errors.append({'decription': 'Некорректная дата рождения'})
    #
    # if individual_json['birthday'] != scorista_res.loc['BirthDate'].value:
    #     errors.append({'decription': 'Не совпадает дата рождения с источником (НБКИ)'})

    if len(errors) == 0:
        return {'status': 'OK'}
    else:
        return {'status': 'Failed', 'errors': errors}


def stop_factors(individual_json, source_json):
    nbki_res = pandas.DataFrame(get_values(source_json)).set_index('name')
    errors = []
    brth = datetime.strptime(nbki_res.loc['BirthDate'].value, '%d.%m.%Y').date()

    if brth + relativedelta(years=+18) > datetime.now().date():
        errors.append({'decription': 'Заявителю нет 18 лет'})

    if int(nbki_res.loc['totalOverDue'].value) > 300000:
        errors.append(
            {'decription': 'Суммарная просроченная задолженность по данным НБКИ по всем активным счетам более 300000 рублей'})

    if int(nbki_res.loc['delay'].value) > 100000:
        errors.append({
                          'decription': 'Максимальная текущая просрочка по данным НБКИ по активным кредитам, по справочнику PMTPAT, более 100000 рублей'})

    if nbki_res.loc['maxDelay'].value > 300000:
        errors.append({
                          'decription': 'Максимальная историческая просрочка по данным НБКИ по активным кредитам, по справочнику PMTPAT более 300000 рублей'})

    if nbki_res.loc['closednegative'].value == "Y":
        errors.append({'decription': 'Наличие негатива в закрытых кредитах по данным НБКИ'})

    if nbki_res.loc['countdue30_60inopenedaccs'].value > 6:
        errors.append(
            {'decription': 'Количество просрочек 30 - 59 дней за последние 12 месяцев по открытым счетам более 6 по данным НБКИ'})

    if nbki_res.loc['countdue30_60inclosedaccs'].value > 6:
        errors.append(
            {'decription': 'Количество просрочек 30 - 59 дней за последние 12 месяцев по закрытым счетам более 6 по данным НБКИ'})

    if nbki_res.loc['countdue60_90inopenedaccs'].value > 6:
        errors.append(
            {'decription': 'Количество просрочек 60 - 89 дней за последние 12 месяцев по открытым счетам более 6 по данным НБКИ'})

    if nbki_res.loc['countdue60_90inclosedaccs'].value > 6:
        errors.append(
            {'decription': 'Количество просрочек 60 - 89 дней за последние 12 месяцев по закрытым счетам более 6 по данным НБКИ'})

    if nbki_res.loc['countdue90plusinopenedaccs'].value > 12:
        errors.append({'decription': 'Количество просрочек 90+ дней за все время по открытым счетам более 12 по данным НБКИ'})

    if nbki_res.loc['countdue90plusinclosedaccs'].value > 12:
        errors.append({'decription': 'Количество просрочек 90+ дней за все время по закрытым счетам более 12 по данным НБКИ'})

    if nbki_res.loc['hasnewer'].value == "Y":
        errors.append({'decription': 'Есть более свежий паспорт по данным НБКИ'})

    if nbki_res.loc['invalid'].value == "Y":
        errors.append({'decription': 'Признак недействительности паспорта по данным НБКИ'})

    if nbki_res.loc['wanted'].value == "Y":
        errors.append({'decription': 'Розыск по данным НБКИ'})

    if len(errors) == 0:
        return {'status': 'OK'}
    else:
        return {'status': 'Failed', 'errors': errors}


def get_available_params():
    return [{'name': 'Passport', 'description': 'Серия и номер паспорта', 'type': 'int'},
            {'name': 'PassportDate', 'description': 'Дата выдачи', 'type': 'int'},
            {'name': 'FIO', 'description': 'ФИО клиента', 'type': 'string'},
            {'name': 'BirthDate', 'description': 'Дата рождения', 'type': 'date'},
            {'name': 'totalOverDue', 'description': 'Суммарная просроченная задолженность по всем активным счетам',
             'type': 'int'},
            {'name': 'delay',
             'description': 'Максимальная текущая просрочка по активным кредитам по справочнику PMTPAT', 'type': 'int'},
            {'name': 'maxDelay',
             'description': 'Максимальная историческая просрочка по активным кредитам по справочнику PMTPAT',
             'type': 'int'},
            {'name': 'closednegative', 'description': 'Наличие негатива в закрытых кредитах', 'type': 'string'},
            {'name': 'countdue30_60inopenedaccs',
             'description': 'Количество просрочек 30 - 59 дней за последние 12 месяцев по открытым счетам',
             'type': 'int'},
            {'name': 'countdue30_60inclosedaccs',
             'description': 'Количество просрочек 30 - 59 дней за последние 12 месяцев по закрытым счетам',
             'type': 'int'},
            {'name': 'countdue60_90inopenedaccs',
             'description': 'Количество просрочек 60 - 89 дней за последние 12 месяцев по открытым счетам',
             'type': 'int'},
            {'name': 'countdue60_90inclosedaccs',
             'description': 'Количество просрочек 60 - 89 дней за последние 12 месяцев по закрытым счетам',
             'type': 'int'},
            {'name': 'countdue90plusinopenedaccs',
             'description': 'Количество просрочек 90+ дней за все время по открытым счетам', 'type': 'int'},
            {'name': 'countdue90plusinclosedaccs',
             'description': 'Количество просрочек 90+ дней за все время по закрытым счетам', 'type': 'int'},
            {'name': 'hasnewer', 'description': 'Есть более свежий паспорт', 'type': 'string'},
            {'name': 'invalid', 'description': 'Признак недействительности паспорта', 'type': 'string'},
            {'name': 'wanted', 'description': 'Розыск', 'type': 'string'},
            {'name': 'fact_hasnewer', 'description': 'Факт наличия более свежего паспорта', 'type': 'string'},
            {'name': 'fact_invalid', 'description': 'Факт недействительности паспорта', 'type': 'string'},
            {'name': 'fact_wanted', 'description': 'Факт наличия лица в розыске', 'type': 'string'}
            ]


def get_module_source():
    return 'NBKI'


def get_module_name():
    return MODULE_NAME
