#!/usr/bin/env python3
import sys
sys.path.append('../')


from lib.process import *
from lib.constants import *

import requests
import json

class ClientProcessor(BasicProcess):

    def __init__(self):
        super(ClientProcessor,self).__init__(constants.CLIENT_PROCESSOR_QUEUE,
                              {
                                constants.CLIENT_RAW_CREATED_MESSAGE:self.__process_raw_client
                             })

    def __process_raw_client(self, body):
        # try:
        url = "http://127.0.0.1:8002"
        headers = {"accept": "application/json",
                   "X-CSRFToken": "hDnSpAaGh1PBYRa4mLozhjdXUMKXVIeOsYXUbJpcGtGoJ5KxZKF9kmjpZj3hKJGD"}

        # дергаем сырок
        input_message = json.loads(body)
        raw_client_id = input_message['raw_client_id']
        response = requests.get(url=url + '/api/willz/{0}/'.format(raw_client_id), headers=headers)

        # парсим полученное
        raw_data = json.loads(response.content)
        raw_json = json.loads(raw_data['payload'])

        # делаем формат для Клиента, отправляем и получаем client_id
        raw_to_client = {'willz_id': raw_json['id'], 'created_at': raw_json['created_at']}
        response = requests.post(url=url + '/api/clients/', data=raw_to_client, headers=headers)
        if response == 415:
            return;
        raw_data = json.loads(response.content)
        client_id = raw_data['id']

        # ищем главную индивидуалку
        for drvr in raw_json['drivers']:
            # Ищем совпадения ID с вилзом и пихаем в первую очередь
            if drvr['id'] == raw_json['driver_id']:
                # делаем формат для Индивидуалки, отправляем и получаем individual_id для привязки паспорта и прав
                raw_to_individual = {'client': client_id, 'last_name': drvr['lastname']
                    , 'first_name': drvr['firstname'], 'middle_name': drvr['middlename'],
                                     'email': drvr['email']
                    , 'phone': drvr['phone'], 'gender': drvr['gender_id'],
                                     'birthday': drvr['birthday']}
                response = requests.post(url=url + '/api/individuals/', data=raw_to_individual, headers=headers)
                raw_data = json.loads(response.content)
                individual_id = raw_data['id']

                # формируем права
                raw_to_driving_license = {'individual': individual_id, 'number': drvr['driver_license']['number']
                    , 'issued_at': drvr['driver_license']['issued_at']}
                response = requests.post(url=url + '/api/driver_licenses/', data=raw_to_driving_license,
                                         headers=headers)
                raw_data = json.loads(response.content)
                driver_license_id = raw_data['id']

                # формируем фото для прав
                for img in range(1, 3):
                    new_img_txt = 'image{0}'.format(img)
                    raw_to_img = {'individual': individual_id, 'driver_license': driver_license_id,
                                  'title': drvr['passport'][new_img_txt],
                                  'url': drvr['passport'][new_img_txt + '_url']}
                    requests.post(url=url + '/api/images/', data=raw_to_img, headers=headers)

                # формируем паспорт
                raw_to_passport = {'individual': individual_id, 'number': drvr['passport']['number']
                    , 'issued_at': drvr['passport']['issued_at'], 'issued_by': drvr['passport']['issued_by']
                    , 'address_registration': drvr['passport']['address_registration']
                    , 'division_code': drvr['passport']['division_code'],
                                   'birthplace': drvr['passport']['birthplace']}
                response = requests.post(url=url + '/api/passports/', data=raw_to_passport, headers=headers)
                raw_data = json.loads(response.content)
                passport_id = raw_data['id']

                # формируем фото для паспорта
                for img in range(1, 5):
                    new_img_txt = 'image{0}'.format(img)
                    raw_to_img = {'individual': individual_id, 'passport': passport_id,
                                  'title': drvr['passport'][new_img_txt],
                                  'url': drvr['passport'][new_img_txt + '_url']}
                    requests.post(url=url + '/api/images/', data=raw_to_img, headers=headers)
                break

        # для всех индивидуалок
        for drvr in raw_json['drivers']:
            if drvr['id'] != raw_json['driver_id']:
                # делаем формат для Индивидуалки, отправляем и получаем individual_id для привязки паспорта и прав
                raw_to_individual = {'client': client_id, 'last_name': drvr['lastname']
                    , 'first_name': drvr['firstname'], 'middle_name': drvr['middlename'],
                                     'email': drvr['email']
                    , 'phone': drvr['phone'], 'gender': drvr['gender_id'],
                                     'birthday': drvr['birthday']}
                response = requests.post(url=url + '/api/individuals/', data=raw_to_individual, headers=headers)
                raw_data = json.loads(response.content)
                individual_id = raw_data['id']

                # формируем права
                raw_to_driving_license = {'individual': individual_id, 'number': drvr['driver_license']['number']
                    , 'issued_at': drvr['driver_license']['issued_at']}
                response = requests.post(url=url + '/api/driver_licenses/', data=raw_to_driving_license,
                                         headers=headers)
                raw_data = json.loads(response.content)
                driver_license_id = raw_data['id']

                # формируем фото для прав
                for img in range(1, 3):
                    new_img_txt = 'image{0}'.format(img)
                    raw_to_img = {'individual': individual_id, 'driver_license': driver_license_id,
                                  'title': drvr['passport'][new_img_txt],
                                  'url': drvr['passport'][new_img_txt + '_url']}
                    requests.post(url=url + '/api/images/', data=raw_to_img, headers=headers)

                # формируем паспорт
                raw_to_passport = {'individual': individual_id, 'number': drvr['passport']['number']
                    , 'issued_at': drvr['passport']['issued_at'], 'issued_by': drvr['passport']['issued_by']
                    , 'address_registration': drvr['passport']['address_registration']
                    , 'division_code': drvr['passport']['division_code'],
                                   'birthplace': drvr['passport']['birthplace']}
                response = requests.post(url=url + '/api/passports/', data=raw_to_passport, headers=headers)
                raw_data = json.loads(response.content)
                passport_id = raw_data['id']

                # формируем фото для паспорта
                for img in range(1, 5):
                    new_img_txt = 'image{0}'.format(img)
                    raw_to_img = {'individual': individual_id, 'passport': passport_id,
                                  'title': drvr['passport'][new_img_txt],
                                  'url': drvr['passport'][new_img_txt + '_url']}
                    requests.post(url=url + '/api/images/', data=raw_to_img, headers=headers)
        # except Exception as e:
        #   print(" Some error: {0}".format(e))

        # else:
        print(" client is processed")
        self._publish_message(CLIENT_PROCESSED_MESSAGE, "test_body")

proc = ClientProcessor()
proc.start()