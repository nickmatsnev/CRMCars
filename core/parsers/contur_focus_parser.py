import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import pandas
import ast
from dateutil.relativedelta import relativedelta

MODULE_NAME = 'ConturFocusParserModule'


def get_values(source_json):
    dictall = json.loads(source_json)
    json1_str = str(dictall)
    json1_data = dictall

    stopWords = ["банкротство", "ликвидация"]

    stopWordIndicators = []
    for wrd in stopWords:
        smth = re.findall(wrd, json1_str.lower())
        stopWordIndicators.append(len(smth))

    riskWords = ["рекомендована дополнительная проверка"]

    riskWordIndicators = []
    for wrd in riskWords:
        smth = re.findall(wrd, json1_str.lower())
        riskWordIndicators.append(len(smth))

    inn = json1_data[0]['inn']
    ogrn = json1_data[0]['ogrn']

    try:
        adrCity = json1_data[0]['UL']['legalAddress']['parsedAddressRF']['city']['topoValue']
    except:
        adrCity = "NA"
    try:
        adrStreet = json1_data[0]['UL']['legalAddress']['parsedAddressRF']['street']['topoValue']
    except:
        adrStreet = "NA"
    try:
        adrHouse = json1_data[0]['UL']['legalAddress']['parsedAddressRF']['house']['topoValue']
    except:
        adrHouse = "NA"

    try:
        fioHead = json1_data[0]['UL']['heads'][0]['fio']
    except:
        fioHead = "NA"

    return [{'name': 'INN', 'value': inn},
            {'name': 'fioHead', 'value': fioHead},
            {'name': 'StopWordIndicators', 'value': stopWordIndicators},
            {'name': 'RiskWordIndicators', 'value': riskWordIndicators},
            {'name': 'OGRN', 'value': ogrn},
            {'name': 'adrCity', 'value': adrCity},
            {'name': 'adrStreet', 'value': adrStreet},
            {'name': 'adrHouse', 'value': adrHouse}
            ]


# Валидация не проводится

def stop_factors(individual_json, source_json):
    scorista_res = pandas.DataFrame(get_values(source_json)).set_index('name')
    errors = []

    if sum(scorista_res.loc['StopWordIndicators'].value) > 0:
        errors.append({'decription': 'Наличие стоп-слов в характеристиках клиента'})

    '''
    Для поиска данных по ФИО руководителей и адресу необходимы дополнительные списки
    Когда будет понятно как к ним обращаться и где их брать - будем дописывать
    '''

    if len(errors) == 0:
        return {'status': 'OK'}
    else:
        return {'status': 'Failed', 'errors': errors}


def validate(individual_json, source_json):
    errors = []

    if len(errors) == 0:
        return {'status': 'OK'}
    else:
        return {'status': 'Failed', 'errors': errors}


def get_available_params():
    return [{'name': 'INN', 'description': 'ИНН компании', 'type': 'int'},
            {'name': 'fioHead', 'description': 'ФИО руководителя компании', 'type': 'string'},
            {'name': 'StopWordIndicators', 'description': 'Вектор индикаторов на наличие стоп-слов',
             'type': 'vector, int'},
            {'name': 'RiskWordIndicators',
             'description': 'Вектор индикаторов на наличие подозрительных слов в описании', 'type': 'vector, int'},
            {'name': 'OGRN', 'description': 'ОГРН компании', 'type': 'int'},
            {'name': 'adrCity', 'description': 'Адрес компании (город)', 'type': 'string'},
            {'name': 'adrStreet', 'description': 'Адрес компании (улица)', 'type': 'string'},
            {'name': 'adrHouse', 'description': 'Адрес компании (дом)', 'type': 'string'}
            ]


def get_module_source():
    return 'ConturFocus'


def get_module_name():
    return MODULE_NAME