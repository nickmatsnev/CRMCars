from datetime import datetime
from core.lib.constants import BASE_DATE


def datetime_converter(input):
    if input is None:
        ret = datetime.now()
    else:
        ret = datetime.strptime(input, '%Y-%m-%d %H:%M:%S')

    return ret.__str__()

def date_converter(input):
    if input is None:
        date = BASE_DATE
    else:
        date = input

    try:
        ret = datetime.strptime(date, '%Y-%m-%d').date()
    except:
        try:
            ret = datetime.strptime(date, '%d.%m.%Y').date()
        except:
            ret = datetime.strptime(input, '%Y-%m-%d %H:%M:%S')
    return ret.__str__()


