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
    stopWordWords = []
    stopWordChunks = []
    for wrd in stopWords:
        smth = re.findall(wrd, json1_str.lower())
        stopWordIndicators.append(len(smth))
        stopWordWords.append(wrd)
        smth = re.findall('(>((?!>).)*?' + wrd + '.*?<)', fileall.lower())
        if len(smth) > 0:
            stopWordChunks.append(smth)

    stopWordChunks = [item for sublist in stopWordChunks for item in sublist]
    stopWordChunks = [item for sublist in stopWordChunks for item in sublist]
    stopWordChunks = list(filter(lambda x: x!= ' ', stopWordChunks))
    stopWordChunks = list(filter(lambda x: x!= '', stopWordChunks))

    stopWordDict = dict(zip(stopWordWords, stopWordIndicators))

    riskWords = ["рекомендована дополнительная проверка"]

    riskWordIndicators = []
    riskWordWords = []
    for wrd in riskWords:
        smth = re.findall(wrd, json1_str.lower())
        riskWordIndicators.append(len(smth))
        riskWordWords.append(wrd)

    inn = json1_data[0]['inn']
    ogrn = json1_data[0]['ogrn']

    companyNameList = []
    innList = []
    adrCityList = []
    adrStreetList = []
    adrHouseList = []
    fioHeadList = []
    redStatList = []
    yellowStatList = []
    
    for jjd in json1_data:
        try:
            innList.append(jjd['inn'])
        except:
            innList.append('NA')

        try:
            companyName = jjd['UL']['legalName']['short']
            companyNameList.append(companyName)
        except:
            companyNameList.append('NA')
        try:
            adrCity = jjd['UL']['legalAddress']['parsedAddressRF']['regionName']['topoValue']
            adrCityList.append(adrCity)
        except:
            adrCityList.append('NA')

        try:
            adrStreet = jjd['UL']['legalAddress']['parsedAddressRF']['street']['topoValue']
            adrStreetList.append(adrStreet)
        except:
            adrStreetList.append('NA')

        try:
            adrHouse = jjd['UL']['legalAddress']['parsedAddressRF']['house']['topoValue']
            adrHouseList.append(adrHouse)
        except:
            adrHouseList.append('NA')

        try:
            fioHead = jjd['UL']['heads'][0]['fio']
            fioHeadList.append(fioHead)
        except:
            fioHeadList.append('NA')

        try:
            redStat = jjd['UL']['briefReport']['summary']['redStatements']
            redStatList.append(redStat)
        except:
            redStatList.append('False')

        try:
            yStat = jjd['UL']['briefReport']['summary']['yellowStatements']
            yellowStatList.append(yStat)
        except:
            yellowStatList.append('False')


    innNumber = len(innList)


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
            {'name': 'StopWordWords', 'value': stopWordWords},
            {'name': 'StopWordDict', 'value': stopWordDict},
            {'name': 'StopWordChunks', 'value': stopWordChunks},
            {'name': 'RiskWordIndicators', 'value': riskWordIndicators},
            {'name': 'RiskWordWords', 'value': riskWordWords},
            {'name': 'OGRN', 'value': ogrn},
            {'name': 'adrCity', 'value': adrCity},
            {'name': 'adrStreet', 'value': adrStreet},
            {'name': 'adrHouse', 'value': adrHouse},
            {'name': 'innList', 'value': innList},
            {'name': 'companyNameList', 'value': companyNameList},
            {'name': 'adrCityList', 'value': adrCityList},
            {'name': 'adrStreetList', 'value': adrStreetList},
            {'name': 'adrHouseList', 'value': adrHouseList},
            {'name': 'fioHeadList', 'value': fioHeadList},
            {'name': 'innNumber', 'value': innNumber},
            {'name': 'redStatList', 'value': redStatList},
            {'name': 'yellowStatList', 'value': yellowStatList}
            ]


# Валидация не проводится

def stop_factors(individual_json, source_json):
    scorista_res = pandas.DataFrame(get_values(source_json)).set_index('name')
    errors = []

    if sum(scorista_res.loc['StopWordIndicators'].value) > 0:
        errors.append({'decription': 'Наличие стоп-слов в характеристиках клиента по данным Контур-Фокус'})

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
            {'name': 'StopWordWords', 'description': 'Вектор обнаруженных стоп-слов',
             'type': 'vector, string'},
            {'name': 'StopWordDict', 'description': 'Словарь из обнаруженных стоп-слов с их частотой',
             'type': 'dictionary'},
            {'name': 'StopWordChunks', 'description': 'Вектор фрагментов текста со стоп-словами',
             'type': 'vector, string'},
            {'name': 'RiskWordIndicators',
             'description': 'Вектор индикаторов на наличие подозрительных слов в описании', 'type': 'vector, int'},
            {'name': 'RiskWordWords', 'description': 'Вектор обнаруженных подозрительных слов',
             'type': 'vector, string'},
            {'name': 'OGRN', 'description': 'ОГРН компании', 'type': 'int'},
            {'name': 'adrCity', 'description': 'Адрес компании (город)', 'type': 'string'},
            {'name': 'adrStreet', 'description': 'Адрес компании (улица)', 'type': 'string'},
            {'name': 'adrHouse', 'description': 'Адрес компании (дом)', 'type': 'string'},
            {'name': 'innList', 'description': 'Лист ИНН аффилированных лиц', 'type': "vector, int"},
            {'name': 'companyNameList', 'description': 'Имя компании', 'type': 'vector,string'},
            {'name': 'adrCityList', 'description': 'Лист адресов (город) аффилированных лиц', 'type': "vector, string"},
            {'name': 'adrStreetList', 'description': 'Лист адресов (улица) аффилированных лиц', 'type': "vector, string"},
            {'name': 'adrHouseList', 'description': 'Лист адресов (номер дома) аффилированных лиц', 'type': "vector, string"},
            {'name': 'fioHeadList', 'description': 'Лист ФИО директоров аффилированных лиц', 'type': "vector, string"},
            {'name': 'redStatList', 'description': 'Ликвидация или банкротство компании', 'type': "vector, string"},
            {'name': 'yellowStatList', 'description': 'Подозрительная активность компании', 'type': "vector, string"},
            {'name': 'innNumber', 'description': 'Количество аффилированных лиц', 'type': "int"}
            ]


def get_module_source():
    return 'ConturFocus'


def get_module_name():
    return MODULE_NAME
