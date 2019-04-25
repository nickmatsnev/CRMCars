import hashlib
import requests
import json


# Получение скорингового балла
def get_score(parsers_data):
    XScore = 150
    YScore = 150

    '''
    Вообще говоря, больше 10 работ - не то же самое, что руководитель более 10 организаций
    Но с руководителем сложно - число повторов "Генеральный директор" считать? Тоже не очень.
    '''
    if not sum(parsers_data['ConturFocusParserModule']['RiskWordIndicators']) > 0:
        XScore += 100

    result = (XScore + YScore) / 10

    return result;


# Получение зависимостей от парсеров
def get_dependencies():
    return ['ConturFocusParserModule']


# Получение имени модуля
def get_module_name():
    return "ConturFocusScoring"
