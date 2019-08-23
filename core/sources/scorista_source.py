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
    res = prepare_individual_for_scorista(individual_json)
    print(prepare_individual_for_scorista(individual_json))

    username = "ek@datascoring.ru"
    nonce = hashlib.sha1()
    token = "f1ec72252e0395cb6406ac514b61b42fdab55252"
    password = hashlib.sha1((nonce.hexdigest() + token).encode('utf-8'))

    url = get_module_url()

    headers = {'Content-Type': 'application/json',
               'username': username,
               'nonce': nonce.hexdigest(),
               'password': password.hexdigest()}

    request = {"requestID": "agrid5d54488296171"}

    # r = requests.post(url=url, data=json.dumps(res,ensure_ascii=False).encode("utf-8"), headers=headers)
    r = requests.post(url, data=json.dumps(request), headers=headers)
    scorista_res = json.loads(r.text)
    return json.dumps(scorista_res, indent=4, ensure_ascii=True)


# Получение имени модуля
def get_module_name():
    return "Scorista"


def prepare_individual_for_scorista(individual_json):
    dadata_location = json.loads(json.loads(individual_json['dadata_raw']))
    dadata_birthplace = json.loads(json.loads(individual_json['dadata_birthplace_raw']))
    personal_info = {}
    personal_info['personaID'] = individual_json['id']
    personal_info['lastName'] = individual_json['last_name']
    personal_info['firstName'] = individual_json['first_name']
    personal_info['patronimic'] = individual_json['middle_name']
    personal_info['gender'] = individual_json['gender']
    personal_info['birthDate'] = individual_json['birthday']
    personal_info['placeOfBirth'] = dadata_birthplace[0]['result']
    personal_info['passportSN'] = '{0} {1}'.format(individual_json['passport']['SN_serial'],individual_json['passport']['SN_number'])
    personal_info['issueDate'] = individual_json['passport']['issued_at']
    personal_info['subCode'] = individual_json['passport']['division_code']

    personal_info['issueAuthority'] = individual_json['passport']['issued_by']

    city = ""
    if dadata_location[0]['city'] is None:
        city = dadata_location[0]['settlement_with_type']
    else:
        city = dadata_location[0]['city_with_type']

    street = "НЕТ"

    if dadata_location[0]['street'] is not None:
        street = dadata_location[0]['street_with_type']

    house = ""
    if dadata_location[0]['house'] is not None:
        house = dadata_location[0]['house']

    building = ""
    if dadata_location[0]['block'] is not None:
        building = dadata_location[0]['block']

    flat = ""

    if dadata_location[0]['flat'] is not None:
        flat = dadata_location[0]['flat']

    address_registration ={}
    address_registration['postIndex'] = dadata_location[0]['postal_code']
    address_registration['region'] = dadata_location[0]['region_with_type']
    address_registration['city'] = city
    address_registration['street'] = street
    address_registration['house'] = house
    address_registration['building'] = building
    address_registration['flat'] = flat
    address_registration['kladrID'] = dadata_location[0]['region_kladr_id']

    contact_info = {}
    contact_info['cellular'] = individual_json['phone']

    persona = {}
    persona['personalInfo'] = personal_info
    persona['addressRegistration'] = address_registration
    persona['addressResidential'] = address_registration
    persona['contactInfo'] = contact_info
    persona['cronos'] = 1

    form = {}
    form['persona'] = persona
    ret_json = {}
    ret_json['form'] = form

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