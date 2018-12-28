#!/usr/bin/env python3
import sys
sys.path.append('../')


from lib.process import *
from lib.constants import *
from rest_framework.test import APIRequestFactory

import json

class ClientProcessor(BasicProcess):

    def __init__(self):
        super(ClientProcessor,self).__init__(constants.CLIENT_PROCESSOR_QUEUE,
                              {
                                constants.CLIENT_RAW_CREATED_MESSAGE:self.__process_raw_client
                             })

    def __process_raw_client(self, body):
        factory = APIRequestFactory()

        #дергаем сырок
        input_message = json.loads(body)
        raw_client_id = input_message['raw_client_id']
        response = factory.get('/api/willz/{0}'.format(raw_client_id))

        #парсим полученное
        raw_data = json.loads(response)
        raw_json = raw_data['payload']

        #делаем формат для Клиента, отправляем и получаем client_id
        raw_to_client = json.load({'willz_id': raw_json['id'],'created_at': raw_json['created_at']})
        response = factory.post('/api/clients',json.dumps(raw_to_client), content_type='application/json')
        raw_data = json.loads(response)
        client_id = raw_data['id']

        #ищем главного индивидуала
        for drvr in raw_json['drivers']:
            if drvr['id'] == raw_json['driver_id']:
                # делаем формат для Индивидуала, отправляем и получаем individual_id для привязки паспорта и прав
                raw_to_individual = json.load({'client': client_id,'last_name': drvr['lastname']
                                                  , 'first_name': drvr['firstname'],'middle_name': drvr['middlename'],'email': drvr['email']
                                                  , 'phone': drvr['phone'],'gender': drvr['gender_id'],'birthday': drvr['birthday']})
                response = factory.post('/api/individuals', json.dumps(raw_to_individual),
                             content_type='application/json')
                raw_data = json.loads(response)
                individual_id = raw_data['id']

                # формируем права
                raw_to_driving_license = json.load({'individual': individual_id,'number': drvr['driver_license']['number']
                                                  , 'issued_at': drvr['driver_license']['issued_at']})
                response = factory.post('/api/driver_licenses', json.dumps(raw_to_driving_license),
                                        content_type='application/json')
                raw_data = json.loads(response)
                driver_license_id = raw_data['id']

                # формируем фото для прав
                for img in range(1, 3):
                    new_img_txt = 'image{0}'.format(img)
                    raw_to_img = json.load({'individual': individual_id,'driver_license': driver_license_id,
                                            'title': drvr['passport'][new_img_txt],'url': drvr['passport'][new_img_txt + '_url']})
                    factory.post('/api/images', json.dumps(raw_to_img),
                                 content_type='application/json')

                # формируем паспорт
                raw_to_passport = json.load(
                    {'individual': individual_id, 'number': drvr['passport']['number']
                        , 'issued_at': drvr['passport']['issued_at'], 'issued_by': drvr['passport']['issued_by']
                        , 'address_registration': drvr['passport']['address_registration']
                        , 'division_code': drvr['passport']['division_code'], 'birthplace': drvr['passport']['birthplace']})
                response = factory.post('/api/driver_licenses', json.dumps(raw_to_driving_license),
                                        content_type='application/json')
                raw_data = json.loads(response)
                passport_id = raw_data['id']

                # формируем фото для паспорта
                for img in range(1, 5):
                    new_img_txt = 'image{0}'.format(img)
                    raw_to_img = json.load({'individual': individual_id,'passport': passport_id,
                                            'title': drvr['passport'][new_img_txt],'url': drvr['passport'][new_img_txt + '_url']})
                    factory.post('/api/images', json.dumps(raw_to_img),
                                 content_type='application/json')
                break

        #для всех индивидуалов
        for drvr in raw_json['drivers']:
            if drvr['id'] != raw_json['driver_id']:
                # делаем формат для Индивидуала, отправляем и получаем individual_id для привязки паспорта и прав
                raw_to_individual = json.load({'client': client_id, 'last_name': drvr['lastname']
                                                  , 'first_name': drvr['firstname'], 'middle_name': drvr['middlename'],
                                               'email': drvr['email']
                                                  , 'phone': drvr['phone'], 'gender': drvr['gender_id'],
                                               'birthday': drvr['birthday']})
                response = factory.post('/api/individuals', json.dumps(raw_to_individual),
                                        content_type='application/json')
                raw_data = json.loads(response)
                individual_id = raw_data['id']

                # формируем права
                raw_to_driving_license = json.load(
                    {'individual': individual_id, 'number': drvr['driver_license']['number']
                        , 'issued_at': drvr['driver_license']['issued_at']})
                response = factory.post('/api/driver_licenses', json.dumps(raw_to_driving_license),
                                        content_type='application/json')
                raw_data = json.loads(response)
                driver_license_id = raw_data['id']

                # формируем фото для прав
                for img in range(1, 3):
                    new_img_txt = 'image{0}'.format(img)
                    raw_to_img = json.load({'individual': individual_id, 'driver_license': driver_license_id,
                                            'title': drvr['passport'][new_img_txt],
                                            'url': drvr['passport'][new_img_txt + '_url']})
                    factory.post('/api/images', json.dumps(raw_to_img),
                                 content_type='application/json')

                # формируем паспорт
                raw_to_passport = json.load(
                    {'individual': individual_id, 'number': drvr['passport']['number']
                        , 'issued_at': drvr['passport']['issued_at'], 'issued_by': drvr['passport']['issued_by']
                        , 'address_registration': drvr['passport']['address_registration']
                        , 'division_code': drvr['passport']['division_code'],
                     'birthplace': drvr['passport']['birthplace']})
                response = factory.post('/api/driver_licenses', json.dumps(raw_to_driving_license),
                                        content_type='application/json')
                raw_data = json.loads(response)
                passport_id = raw_data['id']

                # формируем фото для паспорта
                for img in range(1, 5):
                    new_img_txt = 'image{0}'.format(img)
                    raw_to_img = json.load({'individual': individual_id, 'passport': passport_id,
                                            'title': drvr['passport'][new_img_txt],
                                            'url': drvr['passport'][new_img_txt + '_url']})
                    factory.post('/api/images', json.dumps(raw_to_img),
                                 content_type='application/json')

        print("client is processed")
        self._publish_message(CLIENT_PROCESSED_MESSAGE,"test_body")




proc = ClientProcessor()
proc.start()
