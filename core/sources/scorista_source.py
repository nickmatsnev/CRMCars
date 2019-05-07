import hashlib
import requests
import json
import sys

sys.path.append('../../')
#from core.lib import cached_requests


# Получение урла модуля
def get_module_url():
    return "https://api.scorista.ru/dossier/json"


# импорт сырых данных, физ лицо тут нужно будет, чтобы учитывать параметры конкретного физика
def import_data(credentials_json, individual_json, parsers_data):
    # credentials = json.loads(credentials_json)
    username = "dmitry@korishchenko.ru"
    nonce = hashlib.sha1()
    token = "4def557c4fa35791f07cc8d4faf7c3a5f7ae7c93"
    password = hashlib.sha1((nonce.hexdigest() + token).encode('utf-8'))

    url = get_module_url()

    headers = {'Content-Type': 'application/json',
               'username': username,
               'nonce': nonce.hexdigest(),
               'password': password.hexdigest()}

    request = {"requestID": "agrid5c41aad42dbed"}


    r = requests.post(url=url, data=json.dumps(request), headers=headers)
    #r = requests.post(url, data=json.dumps(request), headers=headers)
    scorista_res = json.loads(r.text)
    return json.dumps(scorista_res, indent=4, ensure_ascii=True)


# Получение имени модуля
def get_module_name():
    return "Scorista"
