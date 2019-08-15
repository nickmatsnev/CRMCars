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

    print(json.dumps(prepare_individual_for_scorista(individual_json)))

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


def prepare_individual_for_scorista(individual_json):
    personal_info = {}
    personal_info['personaID'] = individual_json['id']
    personal_info['lastName'] = individual_json['last_name']
    personal_info['firstName'] = individual_json['first_name']
    personal_info['patronimic'] = individual_json['middle_name']
    personal_info['gender'] = individual_json['gender']
    personal_info['birthDate'] = individual_json['birthday']
    personal_info['placeOfBirth'] = individual_json['passport']['birth_city']
    personal_info['passportSN'] = '{0} {1}'.format(individual_json['passport']['SN_serial'],individual_json['passport']['SN_number'])
    personal_info['issueDate'] = individual_json['passport']['issued_at']
    personal_info['subCode'] = individual_json['passport']['division_code']
    personal_info['issueAuthority'] = individual_json['passport']['issued_by']

    address_registration ={}
    address_registration['postIndex'] = individual_json['passport']['reg_index']
    address_registration['region'] = individual_json['passport']['reg_obl']
    address_registration['city'] = individual_json['passport']['reg_city']
    address_registration['street'] = individual_json['passport']['reg_street']
    address_registration['house'] = individual_json['passport']['reg_house']
    address_registration['building'] = individual_json['passport']['reg_building']
    address_registration['flat'] = individual_json['passport']['reg_flat']
    address_registration['kladrID'] = individual_json['passport']['reg_kladrID']

    contact_info = {}
    contact_info['cellular'] = individual_json['phone']

    persona = {}
    persona['personalInfo'] = personal_info
    persona['addressRegistration'] = address_registration
    persona['addressResidential'] = address_registration
    persona['contactInfo'] = contact_info
    persona['cronos'] = 0

    ret_json = {}
    ret_json['form'] = persona

    return ret_json

# {
# "form":
# {
# "persona":
# {
# "personalInfo":
# {
# "personaID": "personaID0",
# "lastName": "Пупкин",
# "firstName": "Василий",
# "patronimic": "Константинович",
# "gender": "2",
# "birthDate": "01.01.1950",
# "placeOfBirth": "Деревня",
# "passportSN": "0000 000000",
# "issueDate": "01.01.1970",
# "subCode": "000-000",
# "issueAuthority": "Такой-то отдел"
# },

# "addressRegistration":
# {
# "postIndex": "000000",
# "region": "Область",
# "city": "Город",
# "street": "Улица",
# "house": "1",
# "building": "А",
# "flat": "100",
# "kladrID": "100000000"
# },

# "addressResidential":
# {
# "postIndex": "000000",
# "region": "Область",
# "city": "Город",
# "street": "Улица",
# "house": "1",
# "building": "А",
# "flat": "100",
# "kladrID": "100000000"
# },

# "contactInfo":
# {
# "cellular": "89876543210"
# },

# "cronos": "0"
# }
# }
# }