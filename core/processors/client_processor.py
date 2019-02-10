#!/usr/bin/env python3
import sys
import json

sys.path.append('..')

from lib import api_requestor
from lib import action_helper
from lib import basic_process
from lib.process import *
from lib.constants import *


class ClientProcessor(BasicProcess):

    def __init__(self):
        super(ClientProcessor, self).__init__(constants.CLIENT_PROCESSOR_QUEUE,
                                              {
                                                  constants.CLIENT_RAW_CREATED_MESSAGE: self.__process_raw_client
                                              })

    def __process_raw_client(self, body):
        try:
            # дергаем сырок
            input_message = json.loads(body)
            raw_client_id = input_message['raw_client_id']
            raw_data = api_requestor.request('/willz/{0}/'.format(raw_client_id))
            # парсим полученное
            raw_json = json.loads(raw_data['payload'])
            # делаем формат для Клиента, отправляем и получаем client_id
            raw_to_client = {'willz_id': raw_json['id'], 'created_at': raw_json['created_at']}
            raw_data = api_requestor.post_decode('/clients/new/', json.dumps(raw_to_client))
            client_id = raw_data['id']

            # для всех индивидуалок
            for drvr in raw_json['drivers']:
                # проверяем на главного
                if drvr['id'] == raw_json['driver_id']:
                    primary = True
                else:
                    primary = False
                # делаем формат для Индивидуалки, отправляем и получаем individual_id для привязки паспорта и прав
                raw_to_individual = {'client': client_id, 'primary': primary, 'last_name': drvr['lastname']
                    , 'first_name': drvr['firstname'], 'middle_name': drvr['middlename'],
                                     'email': drvr['email']
                    , 'phone': drvr['phone'], 'gender': drvr['gender_id'],
                                     'birthday': drvr['birthday']}
                raw_data = api_requestor.post_decode('/individuals/', json.dumps(raw_to_individual))
                individual_id = raw_data['id']

                action_helper.add_action(individual_id, 'new', basic_process.get_name(self))

                # формируем права
                lcn_number = drvr['driver_license']['number']
                if lcn_number == "":
                    lcn_number = 0
                raw_to_driving_license = {'individual': individual_id, 'number': lcn_number
                    , 'issued_at': drvr['driver_license']['issued_at']}
                raw_data = api_requestor.post_decode('/driver_licenses/', json.dumps(raw_to_driving_license))
                driver_license_id = raw_data['id']

                # формируем фото для прав
                for img in range(1, 3):
                    new_img_txt = 'image{0}'.format(img)
                    raw_to_img = {'individual': individual_id, 'driver_license': driver_license_id,
                                  'title': drvr['passport'][new_img_txt],
                                  'url': drvr['passport'][new_img_txt + '_url']}
                    api_requestor.post('/images/', json.dumps(raw_to_img))

                # формируем паспорт
                raw_to_passport = {'individual': individual_id, 'number': drvr['passport']['number']
                    , 'issued_at': drvr['passport']['issued_at'], 'issued_by': drvr['passport']['issued_by']
                    , 'address_registration': drvr['passport']['address_registration']
                    , 'division_code': drvr['passport']['division_code'],
                                   'birthplace': drvr['passport']['birthplace']}
                raw_data = api_requestor.post_decode('/passports/', json.dumps(raw_to_passport))
                passport_id = raw_data['id']

                # формируем фото для паспорта
                for img in range(1, 5):
                    new_img_txt = 'image{0}'.format(img)
                    raw_to_img = {'individual': individual_id, 'passport': passport_id,
                                  'title': drvr['passport'][new_img_txt],
                                  'url': drvr['passport'][new_img_txt + '_url']}
                    api_requestor.post('/images/', json.dumps(raw_to_img))
        except Exception as e:
            print(" Some error: {0}".format(e))

        else:
            print(" client is processed")
            self._publish_message(CLIENT_PROCESSED_MESSAGE, "test_body")


proc = ClientProcessor()
proc.start()
