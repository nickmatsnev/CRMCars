import hashlib
import requests
import json
#не было инклюда
import datetime
from dateutil.parser import parse


# Получение скорингового балла
def get_score(parsers_data):
    YScore = 0

    if parsers_data['NBKIParserModule']['delay'] > 20000:
        YScore += 100 - 100*(parsers_data['NBKIParserModule']['delay'] - 20000)/80000
    else:
        YScore += 100
        
    if parsers_data['NBKIParserModule']['totalOverDue'] > 100000:
        YScore += 100 - 100*(parsers_data['NBKIParserModule']['totalOverDue'] - 100000)/200000
    else:
        YScore += 100

    if parsers_data['NBKIParserModule']['maxDelay'] > 100000:
        YScore += 100 - 100*(parsers_data['NBKIParserModule']['maxDelay'] - 100000)/200000
    else:
        YScore += 100

    YScore += 100 - 100*parsers_data['NBKIParserModule']['countdue30_60inopenedaccs']/5
    YScore += 100 - 100*parsers_data['NBKIParserModule']['countdue30_60inclosedaccs']/5
    YScore += 100 - 100*parsers_data['NBKIParserModule']['countdue60_90inopenedaccs']/5
    YScore += 100 - 100*parsers_data['NBKIParserModule']['countdue60_90inclosedaccs']/5

    if parsers_data['NBKIParserModule']['countdue90plusinopenedaccs'] > 3:
        YScore += 100 - 100*(parsers_data['NBKIParserModule']['countdue90plusinopenedaccs'] - 3)/8
    else:
        YScore += 100
        
    if parsers_data['NBKIParserModule']['countdue90plusinclosedaccs'] > 3:
        YScore += 100 - 100*(parsers_data['NBKIParserModule']['countdue90plusinclosedaccs'] - 3)/8
    else:
        YScore += 100
    
    result = YScore/9

    return result;



# Получение зависимостей от парсеров
def get_dependencies():
    return ['NBKIParserModule']


# Получение имени модуля
def get_module_name():
    return "NBKIOnlyScoring"
