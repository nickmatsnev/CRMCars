# -*- coding: utf-8 -*-

import requests
import json


# Получение урла модуля
def get_module_url():
    return "https://www.i-sphere.ru/2.00/"


# импорт сырых данных, физ лицо тут нужно будет, чтобы учитывать параметры конкретного физика
def import_data(credentials_json, individual_json, parsers_data):
    username = 'willz-test'
    password = 'Q3*bNtXm'

    url = get_module_url()

    request = '''<Request>
            <UserID>{0}</UserID>
            <Password>{1}</Password>
        <sources>fms,fns,fssp,rossvyaz</sources>
        <recursive>0</recursive>
        <PersonReq>
            <first>{3}</first>
            <middle>{4}</middle>
            <paternal>{5}</paternal>
        <birthDt>{6}</birthDt>
        <passport_series>{7}</passport_series>
        <passport_number>{8}</passport_number>
        <issueDate>{9}</issueDate>
        </PersonReq>
        <PhoneReq>
        <phone>{10}</phone>
        </PhoneReq>
        <EmailReq>
        <email>{11}</email>
        </EmailReq>
        </Request>'''.format(username, password, password, individual_json["first_name"],
                             individual_json["middle_name"],
                             individual_json["last_name"], individual_json["birthday"],
                             individual_json["passport"]["number"][0:4],
                             individual_json["passport"]["number"][4:], individual_json["passport"]["issued_at"],
                             individual_json["phone"], individual_json["email"])

    r = requests.post(url, data=request.encode())
    sphere_res = {'result': r.text}
    return sphere_res


# Получение имени модуля
def get_module_name():
    return "ISphere"
