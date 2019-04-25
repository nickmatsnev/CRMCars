import hashlib
import requests
import json


# Получение урла модуля
def get_module_url():
    return "https://focus-api.kontur.ru/api3/personAffiliates/req"


# импорт сырых данных, физ лицо тут нужно будет, чтобы учитывать параметры конкретного физика
def import_data(credentials_json, individual_json, parsers_data):
    # credentials = json.loads(credentials_json)
    req_key = "?key=" + "3208d29d15c507395db770d0e65f3711e40374df"
    search_by = "&innfl="
    inn = "773173084809"
    url = get_module_url()

    request = url + req_key + search_by + inn + '&JSON'

    r = requests.get(request)
    scorista_res = json.loads(r.text)
    return json.dumps(scorista_res, indent=4, ensure_ascii=True)


# Получение имени модуля
def get_module_name():
    return "ConturFocus"
